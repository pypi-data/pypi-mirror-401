import numpy as np
from pyPhases import Phase
from pyPhasesML import Model, ModelManager
from tqdm import tqdm

from SleePyPhases.DataManipulation import DataManipulation
from pyPhasesML import Scorer
from SleePyPhases.EventScorer import EventScorer
from SleePyPhases.MultiScorer import MultiScorer


class ThresholdOptimisation(Phase):
    allowTraining = False
    storeValidationPrediction = True

    def getModel(self) -> Model:
        modelState = self.project.getData("modelState", Model, generate=self.allowTraining)
        model = ModelManager.getModel(True)
        model.build()
        model.loadState(modelState)
        return model

    def calculateValidationData(self):
        model = self.getModel()
        useTrainValForOptimisation = self.getConfig("optimizeOn", "validation")
        assert useTrainValForOptimisation in ["validation", "training", "trainval"]
        validationData = self.project.generateData(f"dataset-{useTrainValForOptimisation}")

        daSteps = self.getConfig("eventEval.augmentationCountThatShouldNotBeOptimized", 0)
        manipulationAfterPredict = self.getConfig("eventEval.manipulationAfterPredict", False)
        manipulationAfterPredict = manipulationAfterPredict[0:daSteps]
        da = DataManipulation.getInstance(manipulationAfterPredict, "test", self.project.config)

        prediction = []
        truth = []
        for i in tqdm(range(0, len(validationData))):
            x, t = validationData[i]
            p = model.predict(x, get_likelihood=True, returnNumpy=False)
            p, t = da((p, t))
            [prediction.append(x) for x in p]
            [truth.append(x) for x in t]

        return prediction, truth

    def calculateThreshold(self):
        import scipy
        
        # optimize threshold for given metric
        thresholdMetrics = self.getConfig("thresholdMetric", None)
        thresholdMetrics = thresholdMetrics if isinstance(thresholdMetrics, list) else [thresholdMetrics] 

        classNums = self.getConfig("model.multiclassificationSize", [2])
        labelNames = self.getConfig("classification.labelNames")
        ignoreIndex = self.getConfig("classification.ignoreIndex", -1)
        optimizeThresholdFor = self.getConfig("optimizeThresholdFor", None)
        startThresholds = self.getConfig("startThresholdsAt", [0.5 for _ in range(len(thresholdMetrics))])
        scorerTypes = [(EventScorer if sc == "event" else Scorer) for sc in self.getConfig("classification.scorerTypes")]

        scorer = MultiScorer(classNums, thresholdMetrics, scorerNames=labelNames, ignoreClasses=[ignoreIndex], scorerClasses=scorerTypes)
        for s in scorer.scorer.values():
            s.majorityVote = self.getConfig("eventEval.tpStrat", "overlap") == "majority"
            s.noTN = self.getConfig("eventEval.tnStrat", "eventcount") == "noTN"
            s.trace = True


        manipulationAfterPredict = self.getConfig("eventEval.manipulationAfterPredict", False)
        daSteps = self.getConfig("eventEval.augmentationCountThatShouldNotBeOptimized", 0)
        da = DataManipulation.getInstance(manipulationAfterPredict, "test", self.project.config, threshold=0.5)

        # get Validation data
        if self.storeValidationPrediction:
            # Calculate validation data fresh for each optimization (not stored)
            prediction, truth = self.calculateValidationData()
        else:
            # Use stored validation data
            prediction, truth = self.getData("validationResult", tuple)

        def score(threshold, p, t, scorerIndex, scorerName, optimizeMetric):
            biggerIsBetter = scorer.getMetricDefinition(optimizeMetric)[2]
            if threshold >= 1 or threshold <= 0:
                return np.inf

            negate = -1 if biggerIsBetter else 1
            da.threshold = threshold[0]
            config = manipulationAfterPredict[scorerIndex] if isinstance(manipulationAfterPredict[0], list) else manipulationAfterPredict
            config = config[daSteps:]
            p, t = da((p.copy(), t.copy()), config)
            scorer.scorer[scorerName].threshold = threshold[0]
            r = scorer.scoreSingle(scorerIndex, t, p)

            self.log(f"Optimizing threshold by {optimizeMetric}: t = {threshold} => {r[optimizeMetric]} ")

            return r[optimizeMetric] * negate
        
        thresholds = []
        for scorerIndex, (scorerName, thresholdMetric) in enumerate(zip(labelNames, thresholdMetrics)):
            if optimizeThresholdFor is not None and scorerName not in optimizeThresholdFor:
                thresholds.append(None)
                continue
            self.log(f"Optimize threshold for {scorerName} {thresholdMetric}")
            startAt = startThresholds[scorerIndex]
            t = scipy.optimize.fmin(score, args=(prediction, truth, scorerIndex, scorerName, thresholdMetric), x0=startAt, xtol=0.001, ftol=0.001)
            self.logSuccess(f"Optimized threshold for {scorerName} {thresholdMetric}: {t}")
            thresholds.append(t)

        return thresholds

    def generateData(self, name):
        if name == "validationResult":
            valData = self.calculateValidationData()
            self.registerData("validationResult", valData)
        if name == "threshold":
            thresholdMetric = self.getConfig("thresholdMetric", None)

            if thresholdMetric is not None:
                threshold = self.calculateThreshold()
            else:
                threshold = 0.5
            self.registerData("threshold", threshold)

    def main(self):
        self.getData("threshold", list)
