"""
Test file for HydroNet package using pytest
"""

import sys
import os
import numpy as np
import pytest

# Add to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_import():
    """Test importing the package"""
    from Core_Package.hydronet import PARAMETERS
    from Core_Package.hydronet.extended.hydro_metrics import HydroMetrics
    from Core_Package.hydronet.extended.predictor import HydroPredictor
    
    assert len(PARAMETERS) == 12
    assert isinstance(PARAMETERS, list)
    assert "precipitation" in PARAMETERS

def test_hydrometrics():
    """Test HydroMetrics class"""
    from Core_Package.hydronet.extended.hydro_metrics import HydroMetrics
    
    metrics = HydroMetrics()
    
    # Test entropy
    data = np.array([0.1, 0.2, 0.3, 0.4])
    entropy = metrics.calculate_entropy(data)
    assert entropy > 0
    
    # Test network density
    adj_matrix = np.array([
        [0, 0.5, 0.3],
        [0.5, 0, 0.2],
        [0.3, 0.2, 0]
    ])
    density = metrics.network_density(adj_matrix)
    assert 0 <= density <= 1
    
    # Test SVI
    test_metrics = {
        'entropy': 0.5,
        'density': 0.3,
        'centrality': 0.7,
        'clustering': 0.4,
        'path_length': 0.6
    }
    svi = metrics.calculate_svi(test_metrics)
    assert 0 <= svi <= 1

def test_predictor():
    """Test HydroPredictor"""
    from Core_Package.hydronet.extended.predictor import HydroPredictor
    
    predictor = HydroPredictor(threshold=0.6)
    
    # Create test data
    test_data = {}
    params = [
        "precipitation", "evapotranspiration", "atmospheric_pressure",
        "streamflow", "lake_levels", "reservoir_storage",
        "groundwater_levels", "groundwater_quality",
        "soil_moisture", "land_subsidence",
        "water_extraction", "land_use_change"
    ]
    
    for param in params:
        test_data[param] = np.random.normal(0, 1, 30)
    
    # Test
    result = predictor.predict_collapse_risk(test_data)
    
    assert 'svi' in result
    assert 'risk_level' in result
    assert 'warning' in result
    assert 0 <= result['svi'] <= 1
    assert result['risk_level'] in ["CRITICAL", "HIGH", "LOW"]
    assert result['parameters_analyzed'] <= 12

def test_te_calculation():
    """Test transfer entropy calculation"""
    from Core_Package.hydronet.extended.hydro_metrics import HydroMetrics
    
    metrics = HydroMetrics()
    
    # Create correlated time series
    source = np.random.normal(0, 1, 100)
    target = 0.5 * source + 0.5 * np.random.normal(0, 1, 100)
    
    te = metrics.transfer_entropy(source, target)
    
    # TE should be non-negative
    assert te >= 0
    assert isinstance(te, float)

if __name__ == "__main__":
    # Allow running as script
    pytest.main([__file__, "-v"])
