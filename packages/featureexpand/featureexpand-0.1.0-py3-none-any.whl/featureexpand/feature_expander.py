import requests
import pandas as pd
import numpy as np
import json
import os
import uuid
import hashlib
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.preprocessing import MinMaxScaler
from typing import List, Optional, Union, Dict, Callable, Any

# Import helper functions from utils
from .utils import (
    encode,
    convert_hardware_result_to_formula, 
    get_boolean_terms,
    convert_to_continuous_formula,
    get_continuous_terms,
    migrate_with_string
)

class FeatureExpander(BaseEstimator, TransformerMixin):
    """
    A Scikit-Learn compatible transformer to expand features using logical formulas 
    simplified by the Exactor API.
    """

    def __init__(self, token: Optional[str] = None, deep: int = 1, response: str = "x1", 
                 environment: str = "PROD", use_continuous_relaxation: bool = False,
                 target_discretizer: Optional[Callable[[Any], bool]] = None,
                 only_new_features: bool = False):
        """
        Args:
            token (str, optional): Token for API authentication.
            deep (int): Precision for encoding (bits per feature). Default is 1.
            response (str): Response variable label (e.g., "x1"). Default is "x1".
            environment (str): Environment ('DEV' or 'PROD'). Default is "PROD".
            use_continuous_relaxation (bool): If True, generates continuous features. Default is False.
            target_discretizer (Callable, optional): Function to convert y values to boolean (True -> response).
            only_new_features (bool): If True, transform returns only the generated features. Default is False.
        """
        self.token = token
        self.deep = deep
        self.response = response
        self.environment = environment
        self.use_continuous_relaxation = use_continuous_relaxation
        self.target_discretizer = target_discretizer
        self.only_new_features = only_new_features

    def fit(self, X, y):
        """
        Fits the model to the input data by sending it to exactor-cloud-service for simplification.
        
        Args:
            X (array-like of shape (n_samples, n_features)): Input features.
            y (array-like of shape (n_samples,)): Target labels.
        
        Returns:
            self: Returns the instance itself.
        """
        # 0. Precondition Checks
        self._check_preconditions()

        # 1. Validation and Conversion (Sklearn standard)
        # Capture raw columns if DataFrame specifically for later use, before check_X_y converts to numpy
        if isinstance(X, pd.DataFrame):
            self.feature_names_in_ = list(X.columns)
        
        X, y = check_X_y(X, y, accept_sparse=False, dtype=None)
        
        # Store n_features
        self.n_features_in_ = X.shape[1]
        
        # If feature names weren't captured (e.g. numpy input), generate default ones
        if not hasattr(self, 'feature_names_in_'):
            self.feature_names_in_ = [f"x{i}" for i in range(self.n_features_in_)]

        # --- NEW: SCALING (Fix for ValueError: Value cannot be negative) ---
        self.scaler_ = MinMaxScaler(feature_range=(0, 1))
        X_scaled = self.scaler_.fit_transform(X)

        # Ensure strict [0, 1] bounds even for training data (guard against float errors)
        X_scaled = np.clip(X_scaled, 0.0, 1.0)

        # 2. Apply Discretizer or Auto-Detect Continuous Target
        # y is now a numpy array due to check_X_y
        if self.target_discretizer:
            # Vectorize the discretizer for efficiency
            v_discretize = np.vectorize(lambda v: self.response if self.target_discretizer(v) else "x0")
            y_transformed = v_discretize(y)
        else:
            # Check for continuous regression target (float or many unique values)
            # If so, auto-discretize at mean to extract "High Value" logic
            unique_vals = np.unique(y)
            if np.issubdtype(y.dtype, np.floating) and len(unique_vals) > 2:
                 threshold = np.mean(y)
                 # Map > mean to response ("x1"), else "x0"
                 y_transformed = np.where(y > threshold, self.response, "x0")
            else:
                 y_transformed = y

        # 3. Prepare Data for Minterm Extraction
        # We need X as list of lists, y as list
        X_vals = X_scaled.tolist() # Use SCALED values
        y_vals = y_transformed.tolist() if isinstance(y_transformed, np.ndarray) else list(y_transformed)
        
        # 4. Determine Total Variables
        total_bits = self.n_features_in_ * self.deep
        
        # Variable names: z0, z1, ..., zN (Reversed for Exactor LSB logic)
        self.variables_ = [f"z{total_bits - 1 - i}" for i in range(total_bits)]
        
        # 5. Extract Minterms (Binary Encoding)
        minterms = []
        for i in range(len(X_vals)):
            # Check if this row is a positive instance
            target_val = y_vals[i]
            
            # --- NEW: FLEXIBLE TARGET CHECK (Fix for Numeric Y) ---
            # Flexible check: Match response exactly, OR match 1 if response is default "x1" (standard boolean case)
            is_positive = (target_val == self.response) or \
                          (self.response == "x1" and (target_val == 1 or target_val == 1.0))
            
            if is_positive:
                # Encode features
                row_bits = []
                for val in X_vals[i]:
                    row_bits.extend(encode(val, self.deep))
                
                # Convert bits to integer (Big Endian logic for migrate compatibility)
                m_val = 0
                for bit_idx, bit in enumerate(row_bits):
                    if bit == 1:
                        m_val |= (1 << (total_bits - 1 - bit_idx))
                
                minterms.append(m_val)
        
        # Remove duplicates and sort for deterministic caching
        minterms = sorted(list(set(minterms)))
        self.minterms_ = minterms # Store as fitted attribute
        
        # Guard: Empty minterms -> No formula
        if not minterms:
             self.formula_string_ = "0"
             self.formula_list_ = []
             self.structure_ = None
             return self
        
        # 6. Check Cache
        if not hasattr(self, '_cache'):
            self._cache = {}
            
        cache_key = self._get_cache_key(minterms)
        if cache_key in self._cache:
            self._apply_api_result(self._cache[cache_key])
            return self

        # 7. Send to API
        payload = {
            "variables": self.variables_,
            "minterms": minterms,
            "dont_cares": []
        }
        
        try:
            result = self._send_data_to_api(payload)
            
            # Handle 413 Fallback (None result)
            if result is None:
                self.formula_string_ = "0"
                self.formula_list_ = []
                self.structure_ = None
                return self

            # Cache and Apply
            self._cache[cache_key] = result
            self._apply_api_result(result)
        except Exception as e:
            raise RuntimeError(f"Exactor API optimization failed: {e}")
        
        return self

    def transform(self, X):
        """
        Expands the features of the input data using the learnt formula.

        Args:
            X (array-like): Input data.

        Returns:
            np.ndarray: Expanded feature vectors.
        """
        # Check is fitted
        check_is_fitted(self, ['formula_string_', 'n_features_in_', 'scaler_'])
        
        # Input validation
        X = check_array(X, accept_sparse=False, dtype=None)
        
        # Check input shape
        if X.shape[1] != self.n_features_in_:
            raise ValueError(f"X has {X.shape[1]} features, but FeatureExpander is expecting {self.n_features_in_} features as input.")
        
        # --- NEW: SCALING ---
        # Transform using fitted scaler
        X_scaled = self.scaler_.transform(X)
        
        # --- NEW: ROBUST NORMALIZATION ---
        # Clip values to [0, 1] to handle out-of-bounds inputs (e.g. test data > train max)
        # This prevents negative values or values > 1 from reaching the binary encoder
        X_scaled = np.clip(X_scaled, 0.0, 1.0)
        
        # Convert to list for migration util
        data = X_scaled.tolist()
        
        # Call optimized migration utility
        result = migrate_with_string(
            values=data,
            nvariables=self.deep,
            formula_string=self.formula_string_,
            use_continuous_relaxation=self.use_continuous_relaxation,
            formula_list=self.formula_list_,
            return_only_new_features=self.only_new_features
        )
        
        # Return as numpy array for consistency with sklearn
        return np.array(result)

    def fit_transform(self, X, y=None, **fit_params):
        return self.fit(X, y, **fit_params).transform(X)

    def _check_preconditions(self):
        """Validates that API token is present and backend is reachable."""
        # 1. Check Token
        token = self.token or os.environ.get("EXACTOR_API_TOKEN")
        if not token:
            raise ValueError(
                "API Token is missing! Please provide `token` in init or set `EXACTOR_API_TOKEN` environment variable. "
                "You can get a token from https://www.booloptimizer.com or your local admin."
            )
        
        # 2. Check Connectivity (Ping/Health check)
        if self.environment == "PROD": 
            base_url = 'https://www.booloptimizer.com'
        else:
            port = os.environ.get("EXACTOR_API_PORT", "8080")
            base_url = f'http://localhost:{port}'
        
        # We skip actual ping to avoid slowdown, relying on failure in fit.
        pass

    def _get_cache_key(self, minterms: List[int]) -> str:
        """Generates a variation-invariant cache key."""
        data_str = json.dumps({
            "minterms": minterms,
            "deep": self.deep,
            "vars": len(self.variables_), # Use fitted variables_
            "continuous": self.use_continuous_relaxation
        }, sort_keys=True)
        return hashlib.md5(data_str.encode('utf-8')).hexdigest()

    def _send_data_to_api(self, json_data: Dict) -> Dict:
        """Sends data to exactor-cloud-service API with retries."""
        if self.environment == "PROD": 
            url = 'https://www.booloptimizer.com/api/simplify'
        else:
            port = os.environ.get("EXACTOR_API_PORT", "8080")
            url = f'http://localhost:{port}/api/simplify'
        
        token = self.token or os.environ.get("EXACTOR_API_TOKEN")
        
        headers = {
            'Content-Type': 'application/json',
            'X-Exactor-Job-Id': str(uuid.uuid4())
        }
        if token:
            headers['Authorization'] = f'Bearer {token}'
        
        session = requests.Session()
        retries = requests.adapters.HTTPAdapter(max_retries=3)
        session.mount('http://', retries)
        session.mount('https://', retries)

        try:
            response = session.post(url, headers=headers, json=json_data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Check for 413 Payload Too Large specifically
            if e.response is not None:
                if e.response.status_code == 413:
                    print(f"Warning: 413 Payload Too Large (Size: {len(json.dumps(json_data))} bytes). Skipping optimization.")
                    return None
                if e.response.status_code == 409:
                    print(f"Warning: 409 Conflict - Complexity Limit or Duplicate Job. Skipping optimization.")
                    return None
                if e.response.status_code == 500:
                    print(f"Warning: 500 Internal Server Error (Backend Failure). Skipping optimization.")
                    return None
            
            # Re-raise others
            raise ConnectionError(f"Failed to connect to Exactor API at {url}. Cause: {e}")

    def _apply_api_result(self, result: Dict):
        """Parses API result and updates state."""
        self.api_response_ = result # Fitted attribute
        simplified_expression = result.get("espresso")
        
        if simplified_expression:
            self.formula_string_ = simplified_expression 
            
            # Legacy/JSON Parsing if needed (Exactor LPU format)
            if simplified_expression.strip().startswith("{"):
                try:
                    debug_json = json.loads(simplified_expression)
                    res_str = debug_json.get("result")
                    if isinstance(res_str, str):
                        terms_data = json.loads(res_str)
                        total_vars = len(self.variables_)
                        
                        if self.use_continuous_relaxation:
                            self.formula_string_ = convert_to_continuous_formula(terms_data, total_vars)
                            self.formula_list_ = get_continuous_terms(terms_data, total_vars)
                            self.structure_ = terms_data # Expose raw structure
                        else:
                            self.formula_string_ = convert_hardware_result_to_formula(terms_data, total_vars)
                            self.formula_list_ = get_boolean_terms(terms_data, total_vars)
                            self.structure_ = terms_data 
                except Exception as e:
                    print(f"Warning: Failed to parse detailed JSON formula: {e}")
            else:
                # Default text formula
                self.formula_list_ = [] # Should parse text to list if we want full compat, but mostly for migration util
                self.structure_ = None
        else:
            self.formula_string_ = "0"
            self.formula_list_ = []
            self.structure_ = None
            
    # Compatibility properties for legacy code accessing non-underscore attrs
    @property
    def formula_string(self):
        return getattr(self, 'formula_string_', None)
        
    @property
    def api_response(self):
        return getattr(self, 'api_response_', None)
        
    @property
    def deep_val(self): # Rename collision check? No.
        return self.deep

    @property
    def variables(self):
        return getattr(self, 'variables_', None)
    
    @property
    def structure(self):
        return getattr(self, 'structure_', None)
