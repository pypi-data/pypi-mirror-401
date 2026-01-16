from pyPhases import Phase
from glob import glob
import os
import re
import pandas as pd
from pathlib import Path
import json
import sys
from pyPhasesML import Scorer


class LogCleanup(Phase):
    def loadConfig(self, json_path):
        with open(json_path, "r") as file:
            config = json.load(file)
        return config

    def parse_checkpoint_filename(self, filename):
        """Parse checkpoint filename to extract epoch and metrics."""
        # Extract base filename without path
        base_filename = os.path.basename(filename)
        
        # Regular expression to match the checkpoint pattern
        pattern = r"checkpointModel_(\d+)_(.+)\.pkl"
        match = re.match(pattern, base_filename)
        
        if not match:
            return None
        
        epoch = int(match.group(1))
        metrics_str = match.group(2)
        metrics = [float(m) for m in metrics_str.split('_')]
        
        return {
            'epoch': epoch,
            'metrics': metrics,
            'filename': filename
        }

    def get_metric_directions(self, log_folder):
        """Get the direction (bigger is better or not) for each metric."""
        # Try to load config to get metric names
        config_path = os.path.join(log_folder, "project.config")
        metric_directions = []
        
        try:
            if os.path.exists(config_path):
                config = self.loadConfig(config_path)
                if "trainingParameter" in config and "validationMetrics" in config["trainingParameter"]:
                    metrics = config["trainingParameter"]["validationMetrics"]
                    # Flatten metrics if they're nested
                    flat_metrics = []
                    for m in metrics:
                        if isinstance(m, list):
                            flat_metrics.extend(m)
                        else:
                            flat_metrics.append(m)
                    
                    # Get direction for each metric
                    scorer = Scorer()
                    for metric in flat_metrics:
                        _, _, bigger_is_better = scorer.getMetricDefinition(metric)
                        metric_directions.append(bigger_is_better)
        except Exception as e:
            print(f"  Warning: Could not determine metric directions from config: {e}")
        
        # If we couldn't determine directions, assume all metrics are "bigger is better"
        if not metric_directions:
            # Try to infer from checkpoint filenames
            checkpoint_files = glob(os.path.join(log_folder, "checkpointModel_*.pkl"))
            if checkpoint_files:
                first_checkpoint = self.parse_checkpoint_filename(checkpoint_files[0])
                if first_checkpoint:
                    metric_count = len(first_checkpoint['metrics'])
                    metric_directions = [True] * metric_count
        
        return metric_directions

    def is_dominated(self, checkpoint, other_checkpoints, metric_directions):
        """Check if a checkpoint is dominated by any other checkpoint, considering metric directions."""
        if not metric_directions:
            # Default to all metrics being "bigger is better"
            metric_directions = [True] * len(checkpoint['metrics'])
        
        for other in other_checkpoints:
            if other['filename'] == checkpoint['filename']:
                continue
            
            # Check if all metrics in other checkpoint are better than or equal to this checkpoint
            all_metrics_better_or_equal = True
            
            for i, (checkpoint_metric, other_metric) in enumerate(zip(checkpoint['metrics'], other['metrics'])):
                bigger_is_better = metric_directions[i] if i < len(metric_directions) else True
                
                if bigger_is_better:
                    if other_metric < checkpoint_metric:
                        all_metrics_better_or_equal = False
                        break
                else:  # Smaller is better
                    if other_metric > checkpoint_metric:
                        all_metrics_better_or_equal = False
                        break
            
            # If other checkpoint has higher epoch and all metrics are better or equal, this checkpoint is dominated
            if other['epoch'] > checkpoint['epoch'] and all_metrics_better_or_equal:
                return True
                
            # Check if all metrics are strictly better regardless of epoch
            all_metrics_strictly_better = True
            for i, (checkpoint_metric, other_metric) in enumerate(zip(checkpoint['metrics'], other['metrics'])):
                bigger_is_better = metric_directions[i] if i < len(metric_directions) else True
                
                if bigger_is_better:
                    if other_metric <= checkpoint_metric:
                        all_metrics_strictly_better = False
                        break
                else:  # Smaller is better
                    if other_metric >= checkpoint_metric:
                        all_metrics_strictly_better = False
                        break
            
            if all_metrics_strictly_better:
                return True
                
        return False

    def main(self):
        log_directory = "logs/"
        
        # Check if "all" option is provided
        confirm_all = "all" in self.getConfig("cleanup.options", [])
        
        # Get all log folders
        log_folders = glob(log_directory + "/*")
        
        for folder in log_folders:
            if not os.path.isdir(folder):
                continue
                
            print(f"\nAnalyzing log folder: {folder}")
            
            # Get all checkpoint files
            checkpoint_files = glob(os.path.join(folder, "checkpointModel_*.pkl"))
            resume_files = glob(os.path.join(folder, ".resume*"))
            
            # Parse checkpoint information
            checkpoints = []
            for file in checkpoint_files:
                parsed = self.parse_checkpoint_filename(file)
                if parsed:
                    checkpoints.append(parsed)
            
            # If no checkpoints found, check if folder should be deleted
            if not checkpoints:
                all_files = os.listdir(folder)
                if len(all_files) <= 2 and all(f in all_files for f in ["project.config", "model.config"]):
                    print(f"  Folder {folder} contains only config files and no checkpoints. Deleting folder.")
                    for file in all_files:
                        os.remove(os.path.join(folder, file))
                    os.rmdir(folder)
                    print(f"  Deleted folder {folder}")
                    continue
            
            # Get metric directions (bigger is better or not)
            metric_directions = self.get_metric_directions(folder)
            
            # Identify obsolete checkpoints
            obsolete_checkpoints = []
            keep_checkpoints = []
            
            for checkpoint in checkpoints:
                if self.is_dominated(checkpoint, checkpoints, metric_directions):
                    obsolete_checkpoints.append(checkpoint)
                else:
                    keep_checkpoints.append(checkpoint)
            
            # Print summary and ask for confirmation if needed
            if obsolete_checkpoints or resume_files:
                print(f"  Found {len(obsolete_checkpoints)} obsolete checkpoints and {len(resume_files)} resume files.")
                print("  Checkpoints to keep:")
                for cp in keep_checkpoints:
                    print(f"    - Epoch {cp['epoch']}, Metrics: {cp['metrics']}")
                
                print("  Checkpoints to delete:")
                for cp in obsolete_checkpoints:
                    print(f"    - Epoch {cp['epoch']}, Metrics: {cp['metrics']}")
                
                if resume_files:
                    print("  Resume files to delete:")
                    for file in resume_files:
                        print(f"    - {os.path.basename(file)}")
                
                proceed = confirm_all
                if not proceed:
                    confirm = input("  Proceed with deletion? (y/n/all): ")
                    proceed = confirm.lower() == 'y' or confirm.lower() == 'all'
                    confirm_all = confirm.lower() == 'all'
                
                if proceed:
                    # Delete obsolete checkpoints
                    for cp in obsolete_checkpoints:
                        os.remove(cp['filename'])
                        print(f"  Deleted: {os.path.basename(cp['filename'])}")
                    
                    # Delete resume files
                    for file in resume_files:
                        os.remove(file)
                        print(f"  Deleted: {os.path.basename(file)}")
                else:
                    print("  Deletion cancelled.")
            else:
                print("  No obsolete checkpoints or resume files found.")
                
        print("\nLog cleanup completed.")
