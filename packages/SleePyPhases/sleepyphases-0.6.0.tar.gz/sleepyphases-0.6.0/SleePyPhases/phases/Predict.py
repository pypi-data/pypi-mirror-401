import json
from pathlib import Path
from typing import Optional, Dict, List

import numpy as np
from pyPhases import Phase
from pyPhasesML import Model, ModelManager
from pyPhasesRecordloader import RecordLoader
from pyPhasesRecordloader.RecordLoader import ChannelsNotPresent

from SleePyPhases.DataManipulation import DataManipulation
from SleePyPhases.FeatureExtraction import FeatureExtraction
from SleePyPhases.PreManipulation import PreManipulation
from SleePyPhases.PSGEventManager import PSGEventManager
from SleePyPhases.SignalPreprocessing import SignalPreprocessing
from SleePyPhases.phases.Extract import RecordProcessor


class Predict(Phase):
    """
    Execute the trained model on a given EDF file for prediction.
    
    Configuration options:
    - predict.inputFile: Path to the input EDF file (required)
    - predict.weights: Path to custom model weights (optional, uses trained weights by default)
    - predict.recordLoader: Name of the RecordLoader class to use (default: EDFRecordLoader)
    - predict.channelMapping: Dict mapping expected channels to actual channels in the file
    - predict.lastChannelMappingPath: Path to save/load last channel mapping (default: lastchannelmapping.json)
    """
    
    CHANNEL_MAPPING_FILE = "lastchannelmapping.json"
    
    def getModel(self, weightsPath: Optional[str] = None) -> Model:
        """Load the model with optional custom weights."""
        if weightsPath:
            # Load custom weights from specified path
            model = ModelManager.getModel(True)
            model.build()
            model.load(weightsPath)
        else:
            # Use default trained model state
            modelState = self.project.getData("modelState", Model, generate=False)
            model = ModelManager.getModel(True)
            model.build()
            model.loadState(modelState)
        return model
    
    def loadChannelMapping(self) -> Dict[str, str]:
        """Load the last used channel mapping from file."""
        mappingPath = self.getConfig("predict.lastChannelMappingPath", self.CHANNEL_MAPPING_FILE)
        if Path(mappingPath).exists():
            with open(mappingPath, 'r') as f:
                return json.load(f)
        return {}
    
    def saveChannelMapping(self, mapping: Dict[str, str]):
        """Save the channel mapping to file."""
        mappingPath = self.getConfig("predict.lastChannelMappingPath", self.CHANNEL_MAPPING_FILE)
        with open(mappingPath, 'w') as f:
            json.dump(mapping, f, indent=2)
    
    def promptChannelMapping(self, missingChannels: List[str], availableChannels: List[str], 
                              defaultMapping: Dict[str, str]) -> Dict[str, str]:
        """Interactively prompt user to map missing channels."""
        print("\n=== Channel Mapping Required ===")
        print(f"Available channels in file: {availableChannels}")
        print(f"Missing expected channels: {missingChannels}")
        print()
        
        mapping = {}
        for channel in missingChannels:
            default = defaultMapping.get(channel, "")
            if default:
                prompt = f"Map '{channel}' to (default: {default}): "
            else:
                prompt = f"Map '{channel}' to: "
            
            userInput = input(prompt).strip()
            if userInput == "" and default:
                mapping[channel] = default
            elif userInput:
                mapping[channel] = userInput
            else:
                print(f"Warning: No mapping provided for '{channel}', skipping...")
        
        return mapping
    
    def getSignalFromFile(self, inputFile: str, channelMapping: Optional[Dict[str, str]] = None):
        """Load and preprocess the signal from the input file."""
        loaderName = self.getConfig("predict.recordLoader", False)
        if loaderName:
            self.setConfig("loader.recordLoader", loaderName)
        
        recordLoader = RecordLoader.get()
        
        # Get preprocessing configuration
        targetChannels = self.getConfig("preprocessing.targetChannels", [])
        expectedChannels = [ch[0] if isinstance(ch, list) else ch for ch in targetChannels]
        
        # Apply channel mapping if provided
        if channelMapping:
            recordLoader.chanelNameAliasMap = {v: k for k, v in channelMapping.items()}
        
        try:
            recordSignal = recordLoader.loadSignal(inputFile)
        except ChannelsNotPresent as e:
            # Handle missing channels with interactive mapping
            missingChannels = e.channels if hasattr(e, 'channels') else []
            availableChannels = recordSignal.signalNames
            
            # Load default mapping from config or last saved mapping
            defaultMapping = self.getConfig("predict.channelMapping", {})
            savedMapping = self.loadChannelMapping()
            defaultMapping.update(savedMapping)
            
            # Prompt user for mapping
            newMapping = self.promptChannelMapping(missingChannels, availableChannels, defaultMapping)
            
            if newMapping:
                # Save the mapping for future use
                fullMapping = {**defaultMapping, **newMapping}
                self.saveChannelMapping(fullMapping)
                
                # Retry with new mapping
                recordLoader.chanelNameAliasMap = {v: k for k, v in fullMapping.items()}
                recordSignal, events = recordLoader.loadRecord(inputFile)
            else:
                raise
        
        return recordSignal
    
    def preprocessSignal(self, recordSignal):
        """Preprocess the signal for model input."""
        preprocessingConfig = self.getConfig("preprocessing")
        targetFrequency = preprocessingConfig["targetFrequency"]
        targetSignals = preprocessingConfig["targetChannels"]
        featureChannels = preprocessingConfig.get("featureChannels", [])
        
        recordSignal.targetFrequency = targetFrequency
        
        # Get signal names
        signalNames = [recordSignal.getFirstSignalName(s) for s in targetSignals]
        recordSignal = recordSignal[signalNames]
        
        # Apply preprocessing
        signalProcessing = SignalPreprocessing.getInstance(preprocessingConfig)
        signalProcessing.preprocessingSignal(recordSignal)
        
        # Apply pre-manipulation
        preDataManipulation = PreManipulation.getInstance(preprocessingConfig.get("manipulationSteps", []))
        recordSignal, _ = preDataManipulation(recordSignal, [])

        # Extract features if configured
        if featureChannels:
            featureExtraction = FeatureExtraction.getInstance(self.project)
            featureExtraction.extractChannelsByConfig(recordSignal, featureChannels)

        processedSignal = recordSignal.getSignalArray(targetSignals)
        return processedSignal

    def predict(self, inputFile: str) -> np.ndarray:
        """Run prediction on the input file."""
        # Get channel mapping from config
        channelMapping = self.getConfig("predict.channelMapping", None)

        # Load and preprocess the signal
        recordSignal = self.getSignalFromFile(inputFile, channelMapping)
        processedSignal = self.preprocessSignal(recordSignal)

        # Prepare input for model
        if len(processedSignal.shape) == 2:
            processedSignal = processedSignal.reshape([1] + list(processedSignal.shape))

        # Apply segment manipulation for evaluation
        manipulationSteps = self.getConfig("segmentManipulationEval", [])
        da = DataManipulation.getInstance(manipulationSteps, "test", self.project.config)
        processedSignal, _ = da((processedSignal, np.zeros(1)))  # Dummy label

        # Load model with optional custom weights
        weightsPath = self.getConfig("predict.weights", None)
        model = self.getModel(weightsPath)

        # Run prediction
        prediction = model.predict(processedSignal, returnNumpy=True)

        # Apply post-prediction manipulation if configured
        manipulationAfterPredict = self.getConfig("manipulationAfterPredict", False)
        if manipulationAfterPredict:
            threshold = self.getConfig("fixedThreshold", False)
            threshold = threshold or self.getData("threshold", list, generate=False)
            da = DataManipulation.getInstance(manipulationAfterPredict, "test", self.project.config, threshold=threshold)
            prediction, _ = da((prediction, np.zeros(1)))

        return prediction

    def generateData(self, name):
        if name == "prediction":
            inputFile = self.getConfig("predict.inputFile")
            if not inputFile:
                raise ValueError("predict.inputFile must be specified in config")

            prediction = self.predict(inputFile)
            self.registerData("prediction", prediction)
            return prediction

    def main(self):
        inputFile = self.getConfig("predict.inputFile")
        if not inputFile:
            self.logError("predict.inputFile must be specified in config")
            return

        if not Path(inputFile).exists():
            self.logError(f"Input file not found: {inputFile}")
            return

        self.logSuccess(f"Running prediction on: {inputFile}")

        prediction = self.predict(inputFile)

        # Get label names for output
        labelNames = self.getConfig("classification.labelNames", ["prediction"])
        classNames = self.getConfig("classification.classNames", [])

        self.logSuccess(f"Prediction complete. Output shape: {prediction.shape}")

        # Display summary of predictions
        for i, labelName in enumerate(labelNames):
            if isinstance(prediction, list):
                pred = prediction[i]
            elif len(prediction.shape) > 1 and prediction.shape[-1] > 1:
                pred = prediction[..., i] if i < prediction.shape[-1] else prediction
            else:
                pred = prediction

            if len(classNames) > i:
                classes = classNames[i]
                if len(pred.shape) > 1:
                    pred_classes = np.argmax(pred, axis=-1)
                else:
                    pred_classes = pred
                unique, counts = np.unique(pred_classes, return_counts=True)
                self.logSuccess(f"{labelName} distribution:")
                for u, c in zip(unique, counts):
                    className = classes[int(u)] if int(u) < len(classes) else f"class_{u}"
                    self.logSuccess(f"  {className}: {c} samples ({100*c/len(pred_classes):.1f}%)")

        return prediction

