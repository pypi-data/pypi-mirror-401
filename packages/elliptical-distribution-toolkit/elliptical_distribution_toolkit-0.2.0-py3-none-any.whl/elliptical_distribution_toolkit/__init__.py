"""
-------------------------------------------------------------------------------

`elliptical_distribution_toolkit` package top-level import

-------------------------------------------------------------------------------
"""

# AUTO-GENERATED version
__version__ = "0.2.0"

# Import the toolkit functions
from .toolkit import (
    covariance_to_correlation,
    infer_data_dimension,
    mahal_estimated,
    mahal_explicit,
    minimum_sample_count_for_statistical_variance_bounds,
    mv_studentt_elliptical_fit,
    point_weights_tdist_parametric,
    studentt_to_gaussian_conversion,
    t_distribution_samplecount_loss_factor,
    uv_studentt_centered_fit,
    z_score,
)
