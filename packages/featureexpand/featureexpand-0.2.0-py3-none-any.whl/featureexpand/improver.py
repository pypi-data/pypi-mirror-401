import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin, clone
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, KFold
from .feature_expander import FeatureExpander
import warnings

class LinearModelBooster(BaseEstimator, RegressorMixin):
    """
    Automatically selects the best model among:
    1. Standard Linear Regression
    2. Polynomial Regression (tunable degrees)
    3. Logic-Expanded Regression (tunable depth, via Exactor API)
    
    It handles API failures gracefully (falling back to other models) and performs 
    internal cross-validation to pick the robust winner.
    """
    def __init__(self, 
                 token=None, 
                 environment="DEV",
                 poly_degrees=[2], 
                 logic_depths=[1, 2],
                 cv=3,
                 scoring='r2', # Default to R2
                 random_state=42):
        self.token = token
        self.environment = environment
        self.poly_degrees = poly_degrees
        self.logic_depths = logic_depths
        self.cv = cv
        self.scoring = scoring
        self.random_state = random_state
        
        # Results storage
        self.results_ = []
        self.best_estimator_ = None
        self.best_model_name_ = None
        self.best_score_ = -np.inf

    def fit(self, X, y):
        """
        Fits candidate models and selects the best one based on CV score.
        """
        self.results_ = []
        cv = KFold(n_splits=self.cv, shuffle=True, random_state=self.random_state)
        
        # Resolve Scorer
        if self.scoring == 'accuracy':
            from sklearn.metrics import accuracy_score, make_scorer
            # Custom scorer: Threshold regression output at 0.5
            scorer = make_scorer(lambda y_true, y_pred: accuracy_score(y_true, y_pred > 0.5))
        else:
            scorer = self.scoring

        # 1. Baseline: Linear Regression (Ridge)
        self._evaluate_candidate(
            "Linear Regression (Ridge)",
            Ridge(alpha=1.0),
            X, y, cv, scorer
        )
        
        # 2. Polynomial Regression
        for degree in self.poly_degrees:
            model = make_pipeline(
                PolynomialFeatures(degree=degree, include_bias=False),
                Ridge(alpha=1.0)
            )
            self._evaluate_candidate(
                f"Polynomial (deg={degree})",
                model,
                X, y, cv, scorer
            )
            
        # 3. Logic-Expanded Regression
        for deep in self.logic_depths:
            try:
                expander = FeatureExpander(
                    token=self.token, 
                    deep=deep, 
                    environment=self.environment
                )
                model = make_pipeline(
                    expander,
                    Ridge(alpha=1.0)
                )
                
                self._evaluate_candidate(
                    f"Logic-Guided (deep={deep})",
                    model,
                    X, y, cv, scorer,
                    allow_failure=True
                )
            except Exception as e:
                 self.results_.append({
                    "name": f"Logic-Guided (deep={deep})",
                    "score": -np.inf,
                    "status": f"Failed Setup: {str(e)}"
                })

        # Select Best and Refit (with Fallback)
        self.results_.sort(key=lambda x: x['score'], reverse=True)
        
        for i, candidate in enumerate(self.results_):
            try:
                print(f"🔄 Attempting to refit winner: {candidate['name']} (Score: {candidate['score']:.4f})...")
                estimator = clone(candidate['model'])
                estimator.fit(X, y)
                
                # If success:
                self.best_estimator_ = estimator
                self.best_score_ = candidate['score']
                self.best_model_name_ = candidate['name']
                print(f"✅ Final Model Verified: {self.best_model_name_}")
                return self
                
            except Exception as e:
                print(f"❌ Refit failed for {candidate['name']}: {e}")
                print("   Trying next best model...")
        
        raise RuntimeError("All candidate models failed to fit! Check data or configuration.")

    def _evaluate_candidate(self, name, model, X, y, cv, scorer, allow_failure=False):
        try:
            # Use the provided scorer
            scores = cross_val_score(model, X, y, cv=cv, scoring=scorer, n_jobs=1)
            mean_score = np.mean(scores)
            self.results_.append({
                "name": name,
                "model": model,
                "score": mean_score,
                "status": "OK"
            })
        except Exception as e:
            msg = str(e)
            if allow_failure:
                # Likely API error or similar
                print(f"⚠️ candidate '{name}' failed: {msg}")
            else:
                warnings.warn(f"Candidate '{name}' failed unexpectedly: {msg}")
                
            self.results_.append({
                "name": name,
                "model": model,
                "score": -np.inf,
                "status": f"Error: {msg}"
            })

    def predict(self, X):
        if self.best_estimator_ is None:
            raise RuntimeError("Refit the model before predicting.")
        return self.best_estimator_.predict(X)

    def summary(self):
        """Returns a DataFrame-like summary of the competition."""
        print("-" * 60)
        print(f"{'Model Name':<30} | {'CV Score':<10} | {'Status'}")
        print("-" * 60)
        for res in self.results_:
            score_str = f"{res['score']:.4f}" if res['score'] != -np.inf else "N/A"
            status = res['status']
            if len(status) > 15:
                status = status[:12] + "..."
            print(f"{res['name']:<30} | {score_str:<10} | {status}")
        print("-" * 60)
