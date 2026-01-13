"""
Unit tests for LinearModelBooster
"""

import pytest
import numpy as np
import pandas as pd
from featureexpand import LinearModelBooster


class TestLinearModelBooster:
    """Tests for LinearModelBooster class"""
    
    def test_initialization(self):
        """Test basic initialization"""
        booster = LinearModelBooster()
        assert booster.poly_degrees == [2]
        assert booster.logic_depths == [1, 2]
        assert booster.cv == 3
        assert booster.scoring == 'r2'
    
    def test_initialization_with_params(self):
        """Test initialization with custom parameters"""
        booster = LinearModelBooster(
            poly_degrees=[2, 3, 4],
            logic_depths=[1],
            cv=5,
            scoring='accuracy',
            random_state=123
        )
        assert booster.poly_degrees == [2, 3, 4]
        assert booster.logic_depths == [1]
        assert booster.cv == 5
        assert booster.scoring == 'accuracy'
        assert booster.random_state == 123
    
    def test_fit_basic(self):
        """Test basic fit functionality"""
        np.random.seed(42)
        X = np.random.rand(100, 3)
        y = 2 * X[:, 0] + 3 * X[:, 1] + np.random.randn(100) * 0.1
        
        booster = LinearModelBooster(
            token="test_token",
            poly_degrees=[2],
            logic_depths=[],  # Skip logic to avoid API call
            cv=3,
            environment="DEV"
        )
        
        booster.fit(X, y)
        
        # Check that results were stored
        assert len(booster.results_) > 0
        assert booster.best_estimator_ is not None
        assert booster.best_model_name_ is not None
        assert booster.best_score_ != -np.inf
    
    def test_predict_not_fitted(self):
        """Test that predict raises error when not fitted"""
        booster = LinearModelBooster()
        X = np.array([[0.1, 0.2, 0.3]])
        
        with pytest.raises(RuntimeError, match="Refit the model"):
            booster.predict(X)
    
    def test_fit_predict(self):
        """Test fit and predict workflow"""
        np.random.seed(42)
        X_train = np.random.rand(100, 3)
        y_train = 2 * X_train[:, 0] + 3 * X_train[:, 1]
        X_test = np.random.rand(20, 3)
        
        booster = LinearModelBooster(
            poly_degrees=[2],
            logic_depths=[],  # Skip logic models
            cv=3
        )
        
        booster.fit(X_train, y_train)
        predictions = booster.predict(X_test)
        
        assert predictions.shape == (20,)
        assert np.all(np.isfinite(predictions))
    
    def test_summary(self):
        """Test summary method"""
        np.random.seed(42)
        X = np.random.rand(50, 2)
        y = X[:, 0] + X[:, 1]
        
        booster = LinearModelBooster(
            poly_degrees=[2],
            logic_depths=[],
            cv=3
        )
        booster.fit(X, y)
        
        # Summary should not raise errors
        booster.summary()
    
    def test_dataframe_input(self):
        """Test with DataFrame input"""
        np.random.seed(42)
        X = pd.DataFrame({
            'feature1': np.random.rand(50),
            'feature2': np.random.rand(50),
        })
        y = X['feature1'] + 2 * X['feature2']
        
        booster = LinearModelBooster(
            poly_degrees=[2],
            logic_depths=[],
            cv=3
        )
        booster.fit(X, y)
        
        assert booster.best_estimator_ is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
