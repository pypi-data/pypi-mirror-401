"""
Unit tests for FeatureExpander
"""

import pytest
import numpy as np
import pandas as pd
from featureexpand import FeatureExpander


class TestFeatureExpander:
    """Tests for FeatureExpander class"""
    
    def test_initialization(self):
        """Test basic initialization"""
        expander = FeatureExpander(deep=2, environment="DEV")
        assert expander.deep == 2
        assert expander.environment == "DEV"
        assert expander.response == "x1"
    
    def test_initialization_with_params(self):
        """Test initialization with custom parameters"""
        expander = FeatureExpander(
            deep=3,
            response="target",
            use_continuous_relaxation=True,
            only_new_features=True
        )
        assert expander.deep == 3
        assert expander.response == "target"
        assert expander.use_continuous_relaxation is True
        assert expander.only_new_features is True
    
    def test_fit_requires_token(self):
        """Test that fit raises error without token"""
        expander = FeatureExpander(environment="DEV")
        X = np.array([[0.1, 0.2], [0.3, 0.4]])
        y = np.array([0, 1])
        
        with pytest.raises(ValueError, match="API Token is missing"):
            expander.fit(X, y)
    
    def test_input_validation(self):
        """Test input validation in fit"""
        expander = FeatureExpander(token="test_token", environment="DEV")
        
        # Valid numpy array input
        X = np.array([[0.1, 0.2], [0.3, 0.4]])
        y = np.array([0, 1])
        
        # This will fail at API call, but input validation should pass
        # We're just testing that check_X_y works
        try:
            expander.fit(X, y)
        except (ConnectionError, RuntimeError):
            pass  # Expected - no actual API connection
    
    def test_dataframe_input(self):
        """Test that DataFrame input is handled correctly"""
        expander = FeatureExpander(token="test_token", environment="DEV")
        
        X = pd.DataFrame({'a': [0.1, 0.2], 'b': [0.3, 0.4]})
        y = pd.Series([0, 1])
        
        try:
            expander.fit(X, y)
        except (ConnectionError, RuntimeError):
            pass  # Expected - no actual API connection
        
        # Check that feature names were captured
        assert hasattr(expander, 'feature_names_in_')
        assert expander.feature_names_in_ == ['a', 'b']
    
    def test_transform_not_fitted(self):
        """Test that transform raises error when not fitted"""
        expander = FeatureExpander(token="test_token")
        X = np.array([[0.1, 0.2]])
        
        with pytest.raises(Exception):  # sklearn raises NotFittedError
            expander.transform(X)
    
    def test_properties(self):
        """Test property accessors"""
        expander = FeatureExpander(deep=2)
        
        # Check properties exist
        assert hasattr(expander, 'formula_string')
        assert hasattr(expander, 'api_response')
        assert hasattr(expander, 'variables')
        assert hasattr(expander, 'structure')
    
    def test_cache_key_generation(self):
        """Test cache key generation is deterministic"""
        expander = FeatureExpander(deep=2)
        
        minterms1 = [1, 2, 3, 4]
        minterms2 = [1, 2, 3, 4]
        minterms3 = [1, 2, 3, 5]
        
        # Initialize cache and variables
        expander._cache = {}
        expander.variables_ = ['z0', 'z1', 'z2', 'z3']
        
        key1 = expander._get_cache_key(minterms1)
        key2 = expander._get_cache_key(minterms2)
        key3 = expander._get_cache_key(minterms3)
        
        assert key1 == key2
        assert key1 != key3


class TestFeatureExpanderEncoding:
    """Tests for encoding functionality"""
    
    def test_minterms_extraction(self):
        """Test that minterms are extracted correctly"""
        # This is an integration-style test that would need API
        # Placeholder for future implementation
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
