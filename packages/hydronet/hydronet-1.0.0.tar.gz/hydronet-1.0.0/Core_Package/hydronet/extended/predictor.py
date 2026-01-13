"""
Hydrological Collapse Predictor
Predicts system collapse using network metrics
"""

import numpy as np
from .hydro_metrics import HydroMetrics

class HydroPredictor:
    """Predict hydrological system collapse"""
    
    def __init__(self, threshold=0.6):
        self.metrics_calculator = HydroMetrics()
        self.threshold = threshold  # SVI threshold for warning
        
    def preprocess_data(self, data_dict):
        """Preprocess 12-parameter data"""
        processed = {}
        for param in self.metrics_calculator.parameters:
            if param in data_dict:
                # Normalize data
                data = np.array(data_dict[param])
                processed[param] = (data - np.mean(data)) / np.std(data)
        return processed
    
    def build_network(self, data_dict):
        """Build adjacency matrix using transfer entropy"""
        n_params = len(self.metrics_calculator.parameters)
        adjacency = np.zeros((n_params, n_params))
        
        # Calculate pairwise transfer entropy
        for i, source_param in enumerate(self.metrics_calculator.parameters):
            for j, target_param in enumerate(self.metrics_calculator.parameters):
                if i != j and source_param in data_dict and target_param in data_dict:
                    te = self.metrics_calculator.transfer_entropy(
                        data_dict[source_param],
                        data_dict[target_param]
                    )
                    adjacency[i, j] = te
        
        return adjacency
    
    def predict_collapse_risk(self, data_dict, window_days=30):
        """
        Predict hydrological collapse risk
        
        Parameters:
        -----------
        data_dict : dict
            Dictionary with 12-parameter time series
        window_days : int
            Time window for analysis
        
        Returns:
        --------
        result : dict
            Dictionary with prediction results
        """
        # Preprocess data
        processed_data = self.preprocess_data(data_dict)
        
        # Build network
        adjacency = self.build_network(processed_data)
        
        # Calculate metrics
        density = self.metrics_calculator.network_density(adjacency)
        
        # Calculate SVI
        metrics = {
            'density': density,
            'entropy': 0.5,  # Placeholder
            'centrality': 0.6,  # Placeholder
            'clustering': 0.4,  # Placeholder
            'path_length': 0.7  # Placeholder
        }
        
        svi = self.metrics_calculator.calculate_svi(metrics)
        
        # Determine risk level
        if svi > 0.8:
            risk_level = "CRITICAL"
            warning = "Immediate action required"
        elif svi > self.threshold:
            risk_level = "HIGH"
            warning = "Increased monitoring needed"
        else:
            risk_level = "LOW"
            warning = "System stable"
        
        return {
            'svi': float(svi),
            'risk_level': risk_level,
            'warning': warning,
            'density': float(density),
            'parameters_analyzed': len(processed_data)
        }
