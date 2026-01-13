"""
HydroNet: AI-Driven Hydrological Network Analysis
12-Parameter Model
"""

__version__ = "3.0.0"
__author__ = "Samir Baladi"
__email__ = "emerladcompass@gmail.com"

# 12 Core Parameters
PARAMETERS = [
    # Atmospheric (3)
    "precipitation",
    "evapotranspiration", 
    "atmospheric_pressure",
    
    # Surface Water (3)
    "streamflow",
    "lake_levels",
    "reservoir_storage",
    
    # Groundwater (2)
    "groundwater_levels",
    "groundwater_quality",
    
    # Soil & Land (2)
    "soil_moisture",
    "land_subsidence",
    
    # Human Impact (2)
    "water_extraction",
    "land_use_change"
]

__all__ = ["PARAMETERS"]
