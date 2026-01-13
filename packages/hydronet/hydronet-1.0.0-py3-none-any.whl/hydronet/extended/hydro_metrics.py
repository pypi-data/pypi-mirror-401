"""
Hydrological Network Metrics Calculator
"""

import numpy as np

# Get PARAMETERS from parent
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Core_Package.hydronet import PARAMETERS

class HydroMetrics:
    """Calculate hydrological network metrics"""
    
    def __init__(self, n_parameters=12):
        self.n_params = n_parameters
        self.parameters = PARAMETERS
        
    def calculate_entropy(self, data):
        """Calculate Shannon entropy"""
        if len(data) == 0:
            return 0
        data_normalized = data / np.sum(data)
        data_normalized = data_normalized[data_normalized > 0]
        if len(data_normalized) == 0:
            return 0
        entropy = -np.sum(data_normalized * np.log2(data_normalized))
        return entropy
    
    def transfer_entropy(self, source, target, k=3):
        """Calculate transfer entropy (simplified version)"""
        n = len(source)
        if n < k + 1:
            return 0.0
        
        # Simplified TE calculation
        # In production, use JIDT library
        source_std = np.std(source) if np.std(source) > 0 else 1
        target_std = np.std(target) if np.std(target) > 0 else 1
        
        # Correlation-based approximation
        corr = np.corrcoef(source[:n-1], target[1:])[0, 1]
        te = abs(corr) * 0.5  # Simplified
        
        return max(0.0, te)
    
    def network_density(self, adjacency_matrix):
        """Calculate network density"""
        n = len(adjacency_matrix)
        if n <= 1:
            return 0
        max_edges = n * (n - 1)
        actual_edges = np.sum(adjacency_matrix > 0)
        return actual_edges / max_edges
    
    def calculate_svi(self, metrics_dict):
        """Calculate System Vulnerability Index"""
        weights = {
            'entropy': 0.2,
            'density': 0.2,
            'centrality': 0.3,
            'clustering': 0.15,
            'path_length': 0.15
        }
        
        svi = 0
        for metric, weight in weights.items():
            if metric in metrics_dict:
                svi += metrics_dict[metric] * weight
        
        return float(np.clip(svi, 0.0, 1.0))
