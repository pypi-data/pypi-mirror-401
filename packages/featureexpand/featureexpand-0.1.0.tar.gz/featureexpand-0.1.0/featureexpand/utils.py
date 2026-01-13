import numpy as np
import re
from typing import List, Union

def generate_variable_map(variables: List[str]) -> List[str]:
    """
    Generates a variable map by appending an apostrophe to each variable name.
    """
    if not isinstance(variables, list) or len(variables) == 0:
        raise ValueError("Variables must be a non-empty list")
    return [f"{variable}'" for variable in variables]

def number_to_variable(number: int, variable_map: List[str]) -> str:
    """
    Converts a number to a variable name using the variable map.
    """
    if number < 0 or number >= len(variable_map):
        raise ValueError(f"Index {number} is out of range for the variable map")
    return variable_map[number]

def number_to_variable_str(num: int, variables_count: int) -> str:
    """
    Maps an integer to a variable string zN based on Exactor LPU logic.
    """
    if variables_count > 0:
        mapped_idx = variables_count - 1 - (num // 2)
    else:
        mapped_idx = num // 2
    return f"z{mapped_idx}"

def list_to_xor_expression(term: Union[int, List[int]], variables_count: int) -> str:
    """
    Converts a term (single int or list of ints) into an XOR expression string.
    """
    numbers = term if isinstance(term, list) else [term]
    if not numbers:
        return "1"

    is_negated = False
    adjustment = 1
    
    # Logic to determine negation and adjustment (from logic.ts)
    if numbers[0] % 2 != 0:
        is_negated = False
        adjustment = 0
    else:
        is_negated = True
        adjustment = 1
        
    parts = []
    for num in numbers:
        var_num = num + adjustment
        # Map to z variable
        parts.append(number_to_variable_str(var_num, variables_count))
        
    # Simplify (XOR property: A ^ A = 0)
    counts = {}
    for p in parts:
        counts[p] = counts.get(p, 0) + 1
        
    simplified_parts = [p for p in set(parts) if counts[p] % 2 != 0]
    
    if not simplified_parts:
        return "1" if is_negated else "0"
        
    joined = " XOR ".join(simplified_parts)
    
    if len(simplified_parts) == 1:
        expr = simplified_parts[0]
        if is_negated:
             return f"(not {expr})"
        return expr
        
    if is_negated:
        return f"not ({joined})"
    return f"({joined})"

def convert_hardware_result_to_formula(representation: List[any], variables_count: int) -> str:
    """
    Converts the raw hardware result (list of lists) into a boolean formula string.
    """
    if not isinstance(representation, list):
         return "Error"
    if not representation:
         return "0"
         
    product_terms = []
    for term in representation:
        if not isinstance(term, list):
             continue
        if not term:
             return "1"
             
        factors = []
        for element in term:
            xor_part = list_to_xor_expression(element, variables_count)
            factors.append(xor_part)
            
        if factors:
            product_terms.append(f"({' and '.join(factors)})")
            
    if not product_terms:
         return "0"
         
    return " or ".join(product_terms)

def get_boolean_terms(representation: List[any], variables_count: int) -> List[str]:
    """
    Returns a list of boolean formula strings, one for each product term.
    """
    if not isinstance(representation, list) or not representation:
         return []
         
    terms_list = []
    for term in representation:
        if not isinstance(term, list):
             continue
        if not term:
             terms_list.append("1")
             continue
             
        factors = []
        for element in term:
            xor_part = list_to_xor_expression(element, variables_count)
            factors.append(xor_part)
            
        if factors:
            terms_list.append(f"({' and '.join(factors)})")
            
    return terms_list

def list_to_continuous_xor_string(term: Union[int, List[int]], variables_count: int) -> str:
    """
    Converts a term into an arithmetic XOR expression: A + B - 2*A*B.
    Multi-term XOR(a, b, c) -> XOR(XOR(a, b), c).
    """
    numbers = term if isinstance(term, list) else [term]
    if not numbers:
        return "1"

    is_negated = False
    adjustment = 1
    
    if numbers[0] % 2 != 0:
        is_negated = False
        adjustment = 0
    else:
        is_negated = True
        adjustment = 1
        
    parts = []
    for num in numbers:
        var_num = num + adjustment
        v_str = number_to_variable_str(var_num, variables_count)
        parts.append(v_str)

    if not parts:
        return "1" if is_negated else "0"

    # Iterative binary XOR: res = a + b - 2*a*b
    current_expr = parts[0]
    for i in range(1, len(parts)):
        next_part = parts[i]
        # Parentheses for safety
        current_expr = f"({current_expr} + {next_part} - 2 * {current_expr} * {next_part})"
        
    if is_negated:
        return f"(1 - {current_expr})"
    return current_expr

def convert_to_continuous_formula(representation: List[any], variables_count: int) -> str:
    """
    Converts hardware result to continuous formula using:
    AND -> *
    OR -> 1 - (1-P1)*(1-P2)...
    XOR -> A+B-2AB
    """
    if not isinstance(representation, list):
         return "Error"
    if not representation:
         return "0"
         
    product_terms = []
    for term in representation:
        if not isinstance(term, list):
             continue
        if not term:
             # Empty term usually implies 1 (TRUE)?
             product_terms.append("1")
             continue
             
        factors = []
        for element in term:
            xor_part = list_to_continuous_xor_string(element, variables_count)
            factors.append(xor_part)
            
        if factors:
            # AND is multiplication
            product_terms.append(f"({' * '.join(factors)})")
            
    if not product_terms:
         return "0"
    
    # OR is Probabilistic Sum: 1 - (1-A)*(1-B)...
    if len(product_terms) == 1:
        return product_terms[0]
        
    neg_prod_str = " * ".join([f"(1 - {t})" for t in product_terms])
    return f"1 - ({neg_prod_str})"

def get_continuous_terms(representation: List[any], variables_count: int) -> List[str]:
    """
    Returns a list of continuous formula strings, one for each product term.
    """
    if not isinstance(representation, list) or not representation:
         return []
         
    terms_list = []
    for term in representation:
        if not isinstance(term, list):
             continue
        if not term:
             terms_list.append("1")
             continue
             
        factors = []
        for element in term:
            xor_part = list_to_continuous_xor_string(element, variables_count)
            factors.append(xor_part)
            
        if factors:
            terms_list.append(f"({' * '.join(factors)})")
            
    return terms_list

def encode(numero: float, n: int) -> List[int]:
    """
    Encodes a number into a binary vector of length n.
    """
    if numero < 0:
        raise ValueError("Value cannot be negative")

    resto = numero
    digitos = []
    limite = 0.5
    for i in range(n):
        if resto > limite:
            resto = resto - limite
            digitos.append(1)
        else:
            digitos.append(0)
        limite = limite * 0.5
    return digitos

def encode_continuous(numero: float, n: int) -> List[float]:
    """
    Encodes a number into a continuous 'soft bit' vector of length n.
    """
    if numero < 0:
        raise ValueError("Value cannot be negative")

    resto = numero
    digitos = []
    limite = 0.5
    for i in range(n):
        if resto >= limite:
            digitos.append(1.0)
            resto = resto - limite
        else:
            val = resto / limite
            digitos.append(val)
            resto = 0 # Fully consumed
        limite = limite * 0.5
    return digitos

def _vectorized_encode(values: np.ndarray, n: int) -> np.ndarray:
    """
    Vectorized version of encode.
    """
    resto = values.copy()
    bits_cols = []
    limite = 0.5
    for i in range(n):
        mask = resto > limite
        bits_cols.append(mask.astype(int))
        resto = np.where(mask, resto - limite, resto)
        limite = limite * 0.5
    return np.column_stack(bits_cols)

def _vectorized_encode_continuous(values: np.ndarray, n: int) -> np.ndarray:
    """
    Vectorized version of encode_continuous.
    """
    resto = values.astype(float).copy()
    bits_cols = []
    limite = 0.5
    for i in range(n):
        mask = resto >= limite
        val_if_false = resto / limite
        current_bit = np.where(mask, 1.0, val_if_false)
        bits_cols.append(current_bit)
        resto = np.where(mask, resto - limite, 0.0)
        limite = limite * 0.5
    return np.column_stack(bits_cols)

def migrate_with_string(values: List[List[float]], 
           nvariables: int, 
           formula_string: str = None,
           formula_legacy: List[List[int]] = None,
           use_continuous_relaxation: bool = False,
           formula_list: List[str] = None,
           return_only_new_features: bool = False
           ) -> List[List[float]]:
    """
    Transforms feature vectors using logical formula string.
    Optimized to use Vectorized NumPy operations.
    
    Args:
        return_only_new_features (bool): If True, returns only the generated features. 
                                         If False (default), returns original features + generated features.
    """
    try:
        X_arr = np.array(values, dtype=float)
    except Exception:
        X_arr = np.array(values)

    n_samples, n_features = X_arr.shape
    
    # Expand features
    all_z_cols = []
    for f_idx in range(n_features):
        col_values = X_arr[:, f_idx]
        if use_continuous_relaxation:
            encoded_matrix = _vectorized_encode_continuous(col_values, nvariables)
        else:
            encoded_matrix = _vectorized_encode(col_values, nvariables)
        
        for b_idx in range(nvariables):
            all_z_cols.append(encoded_matrix[:, b_idx])
            
    # Prepare Context
    context = {}
    if use_continuous_relaxation:
        for idx, col in enumerate(all_z_cols):
            context[f"z{idx}"] = col
    else:
        for idx, col in enumerate(all_z_cols):
            context[f"z{idx}"] = (col == 1) # Boolean array

    # Prepare Formulas
    target_formulas = []
    if formula_list:
        target_formulas = formula_list
    elif formula_string:
        target_formulas = [formula_string]
    
    generated_features = []
    
    for f_str in target_formulas:
        # Normalize XOR
        expr = f_str.replace(" XOR ", " ^ ")
        
        if not use_continuous_relaxation:
            # Replace logical with bitwise for Vectorized Boolean
            # Use regex to effectively handle boundaries (start of string, parens)
            expr = re.sub(r'\bnot\b', '~', expr)
            expr = re.sub(r'\band\b', '&', expr)
            expr = re.sub(r'\bor\b', '|', expr)
            
        try:
            if expr.strip() == "1":
                res = np.ones(n_samples, dtype=float)
            elif expr.strip() == "0":
                res = np.zeros(n_samples, dtype=float)
            else:
                res = eval(expr, {"__builtins__": None}, context)
            
            generated_features.append(res.astype(float))
                
        except Exception as e:
            print(f"Error optimizing formula '{f_str}': {e}")
            generated_features.append(np.zeros(n_samples))

    if generated_features:
        new_feats = np.column_stack(generated_features)
    else:
         new_feats = np.zeros((n_samples, 0))

    if return_only_new_features:
        return new_feats.tolist()

    final_matrix = np.hstack((X_arr, new_feats))
    
    return final_matrix.tolist()
