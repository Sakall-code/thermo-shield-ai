# STUB: replace with LightGBM inference from ml_pipeline/saved_models/downscaler_lightgbm.pkl in full build.
"""
Microclimate downscaling service (prototype).
"""

def apply_downscaling(t_regional: float, ndvi: float, ndbi: float) -> float:
    """
    Applies a simple linear approximation to downscale regional temperature
    to a ward-specific temperature using remote sensing indices.
    
    Parameters
    ----------
    t_regional : float
        The regional background temperature (°C).
    ndvi : float
        Normalized Difference Vegetation Index (0 to 1).
    ndbi : float
        Normalized Difference Built-up Index (0 to 1).
        
    Returns
    -------
    float
        The ward-specific downscaled temperature (°C).
    """
    t_ward = t_regional + (ndbi * 4.0) - (ndvi * 2.0)
    return round(t_ward, 2)
