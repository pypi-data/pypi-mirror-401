"""
FeatureExpand - Automatic Feature Engineering Library

A powerful Python library for automatic feature engineering using logical formula 
simplification via the Exactor API.
"""

__version__ = "0.1.0"
__author__ = "Juan Carlos Lopez Gonzalez"
__email__ = "jlopez1967@gmail.com"

from .feature_expander import FeatureExpander
from .improver import LinearModelBooster

__all__ = ["FeatureExpander", "LinearModelBooster", "__version__"]
