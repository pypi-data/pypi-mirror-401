from pyPhases import Phase
from glob import glob
import json
from pathlib import Path
import pickle
import pandas as pd
from pyPhases import pdict
import fnmatch


class LogOverview(Phase):
    def loadConfig(self, json_path):
        with open(json_path, "r") as file:
            config = json.load(file)
        return config

    def flatten_with_index(self, lis, names):
        for i, sublist in enumerate(lis):
            if isinstance(sublist, list):
                for item in sublist:
                    yield f"{item}_{names[i]}"
            else:
                yield sublist

    def findBestResults(self, logFolderPath, config):
        # load from log.csv if its exists or from checkpoint-files inside the folder
        logFile = "log.csv"
        csvPath = Path(logFolderPath) / logFile
        metrics = config["trainingParameter"]["validationMetrics"]
        labelNames = config["classification"]["labelNames"]
        labelNames += self.getConfig("overview.addLabelnames", [])
        
        # Add last modified date of log file
        results = {}
        if csvPath.exists():
            # Get last modified time of log file
            last_modified = csvPath.stat().st_mtime
            results["last_modified"] = pd.to_datetime(last_modified, unit='s')
            
            prefix = "val_"
            # read Header and select best "auprc"-col
            df = pd.read_csv(str(csvPath))
            if self.useEpoch:
                results.update({
                    m: df[m].iloc[:self.useEpoch].max()
                    for m in df.columns if m.startswith(prefix)
                })
            else:
                results.update({
                    m: df[m].max()
                    for m in df.columns
                })
            results["epochs"] = len(df)
        else:
            flattened_metrics = list(self.flatten_with_index(metrics[0 : len(labelNames)], labelNames))

            results = {m: 0 for m in flattened_metrics}
            maxEpoch = 0
            for checkPointFile in glob(logFolderPath + "/checkpoint*"):
                split = ".".join(checkPointFile.split("/")[-1].split(".")[:-1]).split("_")
                epoch = split[1]
                epochResults = split[2:]
                results = {m: max(results[m], float(epochResults[i])) for i, m in enumerate(flattened_metrics)}
                maxEpoch = max(maxEpoch, int(epoch))
                results["epochs"] = maxEpoch
                
                # Get last modified time of the latest checkpoint file
                checkpoint_path = Path(checkPointFile)
                if checkpoint_path.exists():
                    last_modified = checkpoint_path.stat().st_mtime
                    results["last_modified"] = pd.to_datetime(last_modified, unit='s')
                
        return results


    def findSegmentResults(self, evalFolder, prefix):
        dataId = evalFolder.split("/")[-1]
        dataIdSegments = "-".join(dataId.split("-")[:-2])
        evalResults = list(glob(f"data/evalResults{dataIdSegments}*"))
        results = {}
        if len(evalResults) > 1:
            raise Exception("there should only be one results")
        if len(evalResults) == 1:
            with open(evalResults[0], "rb") as f:
                data = pickle.load(f)
                results = {
                    prefix + "auprc_seg": data[1]["auprc"],
                    prefix + "f1_seg": data[1]["f1"],
                }
        return results

    def findEvalResults(self, evalFolder):
        resultFile = "recordResultsEvents.csv"
        csvPath = evalFolder + "/" + resultFile
        prefix = "eval"
        results = {}

        if Path(csvPath).exists():
            df = pd.read_csv(str(csvPath))
            values = list(df.columns)
            exampleRecordId = df.iloc[1, 0]
            if exampleRecordId.startswith("acq_"):
                prefix = "tsm_"
            elif exampleRecordId.startswith("shhs1"):
                prefix = "shhs1"
            elif exampleRecordId.startswith("mros"):
                prefix = "mros"
            elif exampleRecordId.startswith("mesa"):
                prefix = "mesa"
            if "examples" in values:
                values.remove("examples")

            df["f1"].mean()

            meanValues = ["f1"]
            suffix = "_mean"
            results = {f"{prefix}_{m}_{suffix}": df[m].mean() for m in meanValues}
            hasIndex = "indexArousal-prediction" in values
            medValues = ["eventCountDiff"]
            if "countArousal-software" in values:
                df["arCount-diff"] = df["countArousal-prediction"] - df["countArousal-software"]

                if hasIndex:
                    df["arI-diff"] = df["indexArousal-prediction"] - df["indexArousal-software"]
            elif "countArousal-prediction" in values:
                df["arCount-diff"] = df["countArousal-prediction"] - df["countArousal-truth"]
                if hasIndex:
                    df["arI-diff"] = df["indexArousal-prediction"] - df["indexArousal-truth"]
                medValues.append("arCount-diff")

            if hasIndex:
                medValues.append("arI-diff")

            suffix = "_med"
            results |= {f"{prefix}_{m}_{suffix}": df[m].median() for m in medValues}

        segmentResults = self.findSegmentResults(evalFolder, prefix)
        results |= segmentResults

        return results

    def find_different_keys(self, dict1, dict2, parent_key="", different_keys=None):
        if different_keys is None:
            different_keys = []

        for key in dict1.keys():
            value1 = dict1[key]
            value2 = dict2.get(key)

            if isinstance(value1, dict) and value2 and isinstance(value2, dict):
                self.find_different_keys(value1, value2, parent_key + "." + key, different_keys)
            elif value1 != value2:
                different_keys.append(parent_key + "." + key)

        return different_keys

    def getNestedKeys(self, myPdict, path=""):
        keys = []

        for k, value in myPdict.items():
            if isinstance(value, dict):
                keys += self.getNestedKeys(value, path=path + "." + k)
            else:
                keys.append(path + "." + k)
        if path == "":
            keys = [k[1:] for k in keys]
        return keys

    def shouldIgnoreValue(self, key, value, ignoreValues):
        """Check if a key-value pair should be ignored based on ignoreValues config"""
        for ignorePattern in ignoreValues:
            if isinstance(ignorePattern, dict):
                for ignoreKey, ignoreVal in ignorePattern.items():
                    # Support wildcard matching for keys
                    if fnmatch.fnmatch(key, ignoreKey):
                        # Convert value to string for comparison if it's a list
                        compareValue = str(value) if isinstance(value, list) else value
                        # Support wildcard matching for values
                        if isinstance(ignoreVal, str) and fnmatch.fnmatch(str(compareValue), ignoreVal):
                            return True
                        elif compareValue == ignoreVal:
                            return True
            elif isinstance(ignorePattern, str):
                # Support legacy format: "key:value"
                if ":" in ignorePattern:
                    ignoreKey, ignoreVal = ignorePattern.split(":", 1)
                    if fnmatch.fnmatch(key, ignoreKey.strip()):
                        compareValue = str(value) if isinstance(value, list) else value
                        if fnmatch.fnmatch(str(compareValue), ignoreVal.strip()):
                            return True
        return False

    def calculateDistinctKeys(self, logResults, ignoreKeys, ignoreValues):
        """Calculate distinct key values from the filtered log results"""
        distinctKeyValues = {}
      
        # First pass: collect all possible keys
        allKeys = set()
        for config, results in logResults:
            keys = self.getNestedKeys(config)
            for key in keys:
                if not any(fnmatch.fnmatch(key, pattern) for pattern in ignoreKeys):
                    allKeys.add(key)
      
        # Second pass: collect values for all keys, including None for missing keys
        for config, results in logResults:
            for key in allKeys:
                try:
                    value = config[key.split(".")]
                    if isinstance(value, dict):
                        continue
                    # Skip key-value pairs that should be ignored
                    if self.shouldIgnoreValue(key, value, ignoreValues):
                        continue
                    if isinstance(value, list):
                        value = str(value)
                except:
                    value = None
              
                if key not in distinctKeyValues:
                    distinctKeyValues[key] = set()
                distinctKeyValues[key].add(value)
      
        return distinctKeyValues

    def convert_to_categories(self, df):
        """Convert all columns to appropriate types for correlation analysis"""
        df_converted = df.copy()
        
        for col in df_converted.columns:
            # Skip if column is already numeric
            if pd.api.types.is_numeric_dtype(df_converted[col]):
                continue
                
            # Handle None/NaN values
            if df_converted[col].isna().all():
                # If all values are NaN, convert to numeric with NaN
                df_converted[col] = pd.to_numeric(df_converted[col], errors='coerce')
                continue
            
            # Get unique non-null values
            # unique_values = df_converted[col].to(str).dropna().unique()
            
            # Try to convert to numeric first
            numeric_series = pd.to_numeric(df_converted[col], errors='coerce')
            
            # If conversion was successful (not all NaN after conversion)
            if not numeric_series.isna().all() and not (numeric_series.isna() & df_converted[col].notna()).any():
                df_converted[col] = numeric_series
            else:
                # Convert to categorical with numeric codes
                # First, convert to string to handle mixed types
                df_converted[col] = df_converted[col].astype(str)
                # Replace 'nan' string back to actual NaN
                df_converted[col] = df_converted[col].replace('nan', pd.NA)
                # Convert to category
                df_converted[col] = df_converted[col].astype('category')
                # Get category codes (this creates numeric representation)
                df_converted[col] = df_converted[col].cat.codes
                # Replace -1 (which represents NaN in category codes) with actual NaN
                df_converted[col] = df_converted[col].replace(-1, pd.NA)
                # Convert to float to handle NaN properly
                df_converted[col] = df_converted[col].astype('float64')
        
        return df_converted

    def apply_value_replacements(self, df, replace_config):
        """Apply value replacements based on the replaceValue configuration"""
        if not replace_config:
            return df
        
        df_replaced = df.copy()
        
        for column, replacements in replace_config.items():
            if column in df_replaced.columns:
                # Handle regular value replacements
                df_replaced[column] = df_replaced[column].replace(replacements)
                
                # Handle "default" value for None/null values
                if "default" in replacements:
                    default_value = replacements["default"]
                    df_replaced[column] = df_replaced[column].fillna(default_value)
            else:
                print(f"Warning: Column '{column}' not found in dataframe for value replacement")
        
        return df_replaced


    def main(self):
        logDirectory = self.getConfig("overview.logDirectory", "results/")
        evalFolder = self.getConfig("overview.evalFolder", "eval/")
        configName = self.getConfig("overview.configName", "project.config")
        minEpochs = self.getConfig("overview.minEpochs", 10)
        ignoreKeys = self.getConfig("overview.ignore", [])
        ignoreValues = self.getConfig("overview.ignoreValues", [])
        queryFilter = self.getConfig("overview.query", False)
        dropColumns = self.getConfig("overview.dropColumns", [])
        replaceValues = self.getConfig("overview.replaceValues", {})
        self.useEpoch = self.getConfig("overview.useEpoch", -1)
        minEpochs = max(self.useEpoch, minEpochs)

        logResults = []
        # iterate over all log folders
        for folder in glob(logDirectory + "/*"):
            # get Config
            modelConfig = folder + "/" + configName
            if not Path(modelConfig).exists():
                subFiles = list(glob(folder + "/*"))
                if len(subFiles) > 0:
                    print("no config found for %s: " % folder)
                    print("files: %s" % (subFiles))
                continue
            config = {"log-path": folder}
            config |= self.loadConfig(modelConfig)

            # read best results
            bestResults = self.findBestResults(folder, config)
            modelStateId = folder[len(logDirectory) :]
            config["modelStateId"] = modelStateId
            evalFolders = list(glob(f"{evalFolder}*{modelStateId}*"))
            config["evalFolders"] = evalFolders
            for f in evalFolders:
                bestResults |= self.findEvalResults(f)

            logResults.append((pdict(config), bestResults))

        def resultFilter(configResult):
            return (
                "epochs" in configResult[1] and configResult[1]["epochs"] is not None and configResult[1]["epochs"] > minEpochs
            )

        logResults = list(filter(resultFilter, logResults))

        # Apply query filter if specified
        if queryFilter:
            # First, create a temporary dataframe with all keys to apply the query
            tempDistinctKeyValues = self.calculateDistinctKeys(logResults, [], [])  # No ignores for temp calculation
            tempRows = []
            for config, results in logResults:
                tempRelevantConfig = {
                    k: config[k.split(".")] if k.split(".") in config else None for k in tempDistinctKeyValues.keys()
                }
                tempRow = tempRelevantConfig | results
                tempRows.append(tempRow)

            tempDf = pd.DataFrame(tempRows)

            # Apply the query filter
            filteredDf = tempDf.query(queryFilter.replace("\n", ""))

            # Get the indices of rows that passed the filter
            filteredIndices = filteredDf.index.tolist()

            # Filter logResults based on the query results
            logResults = [logResults[i] for i in filteredIndices]

            print(f"Query '{queryFilter}' filtered {len(tempDf)} rows down to {len(logResults)} rows")


        # Recalculate distinct keys after filtering
        distinctKeyValues = self.calculateDistinctKeys(logResults, ignoreKeys, ignoreValues)

        # Build final dataframe
        rows = []
        for config, results in logResults:
            relevantConfig = {k: config[k.split(".")] if k.split(".") in config else None for k, values in distinctKeyValues.items() if len(values) > 1}
            row = relevantConfig | results
            rows.append(row)
        df = pd.DataFrame(rows)

        # Apply value replacements
        df = self.apply_value_replacements(df, replaceValues)

        df = df.drop(columns=dropColumns, errors="ignore")
        
        
        # Convert all columns to numeric/categorical for correlation analysis
        df_converted = self.convert_to_categories(df)
        
        # Save both original and converted dataframes
        df.to_csv(logDirectory + "/logOverview.csv", index=False)
        df_converted.to_csv(logDirectory + "/logOverview_categorical.csv", index=False)
        
        # Now you can compute correlations on df_converted
        correlation_matrix = df_converted.corr()
        correlation_matrix.to_csv(logDirectory + "/correlation_matrix.csv")
        
        print(f"Saved original data to: {logDirectory}/logOverview.csv")
        print(f"Saved categorical data to: {logDirectory}/logOverview_categorical.csv")
        print(f"Saved correlation matrix to: {logDirectory}/correlation_matrix.csv")

