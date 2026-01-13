"""
Extended HydroNet Package
Advanced hydrological network analysis
"""

# Import from parent package
from .. import PARAMETERS

__all__ = ['PARAMETERS']

# Lazy imports to avoid circular dependencies
def import_hydro_metrics():
    from .hydro_metrics import HydroMetrics
    return HydroMetrics

def import_predictor():
    from .predictor import HydroPredictor
    return HydroPredictor

def import_monitor():
    from .monitor import HydroMonitor
    return HydroMonitor
