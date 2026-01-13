import torch
import torch.nn as nn
import numpy as np
from typing import List, Union, Any

class XORNeuron(nn.Module):
    """
    Explicit node representing an XOR operation between variables.
    Computes: A XOR B XOR ...
    Logic:
      Continuous: a + b - 2ab (applied sequentially)
      Boolean: (a + b) % 2 (but we use the continuous approximation for differentiability)
    """
    def __init__(self, variable_indices: List[int], n_vars: int, use_continuous: bool = True):
        super().__init__()
        self.variable_indices = variable_indices
        self.n_vars = n_vars
        self.use_continuous = use_continuous
        # In this architecture, inputs are fixed by connection, not weights
        
    def forward(self, x):
        # x is the full Z-input vector (Batch, n_vars)
        
        # Gather inputs involved in this XOR
        # We process them sequentially: Res = v1; Res = Res XOR v2; ...
        
        val = None
        
        for var_idx in self.variable_indices:
            # Map variable index to Z-index (assuming indices passed here are already mapped or raw)
            # The simplified structure returns indices. We need to map them to Z-space.
            # Passed indices are integer IDs.
            # Z-index mapping logic from utils/LogicLayer:
            # z_idx = n_vars - 1 - (var_num // 2)
            
            z_idx = self.n_vars - 1 - (var_idx // 2)
            
            if 0 <= z_idx < self.n_vars:
                current_input = x[:, z_idx:z_idx+1]
            else:
                current_input = torch.zeros((x.shape[0], 1), device=x.device, dtype=x.dtype)
            
            if val is None:
                val = current_input
            else:
                if self.use_continuous:
                    # A + B - 2AB
                    val = val + current_input - 2.0 * val * current_input
                else:
                    # Strict Boolean Logic in a differentiable way? 
                    # If inputs are 0/1, (a-b)^2 or abs(a-b) works for XOR
                    # But sticking to the algebraic form is safest for gradients usually
                    val = val + current_input - 2.0 * val * current_input
                    
        return val

class TermNeuron(nn.Module):
    """
    Explicit node representing a Product Term (AND).
    Inputs:
        - Direct Z variables
        - Outputs from XORNeurons
    """
    def __init__(self, term_structure: List[Any], n_vars: int, use_continuous: bool = True):
        super().__init__()
        self.n_vars = n_vars
        self.use_continuous = use_continuous
        self.xor_neurons = nn.ModuleList()
        # Store metadata (is_negated) separately. 
        # Since nn.ModuleList is ordered, we can map by index.
        self.xor_metadata = [] 
        self.direct_inputs = [] # List of tuples (z_idx, negated)
        
        # Parse structure
        for element in term_structure:
            # element is int (Direct Var) or list[int] (XOR Group)
            element_list = element if isinstance(element, list) else [element]
            
            first_num = element_list[0]
            is_group_negated = (first_num % 2 == 0)
            
            # Adjustment for logic
            # If negated (Even number), we essentially want NOT(Variable)
            # In utils logic: var_num = num + (1 if negated else 0)
            
            if len(element_list) > 1:
                # Create XOR Node
                # We pass raw numbers; XOR Neuron handles z-mapping internally?
                # Actually, let's keep it consistent.
                # If group is negated: NOT(XOR(v1, v2...))
                # We add an XOR neuron for the vars. Negation is handled at aggregation.
                xor_node = XORNeuron(element_list, n_vars, use_continuous)
                self.xor_neurons.append(xor_node)
                self.xor_metadata.append({'negated': is_group_negated})
            else:
                # Direct Variable
                num = element_list[0]
                adjustment = 1 if is_group_negated else 0
                var_num = num + adjustment
                z_idx = n_vars - 1 - (var_num // 2)
                self.direct_inputs.append({'z_idx': z_idx, 'negated': is_group_negated})

    def forward(self, x):
        factors = []
        
        # 1. Collect Direct Inputs
        for item in self.direct_inputs:
            z_idx = item['z_idx']
            is_negated = item['negated']
            
            if 0 <= z_idx < self.n_vars:
                val = x[:, z_idx:z_idx+1]
            else:
                val = torch.zeros((x.shape[0], 1), device=x.device, dtype=x.dtype)
                
            if is_negated:
                val = 1.0 - val
            factors.append(val)
            
        # 2. Collect XOR Inputs
        for i, node in enumerate(self.xor_neurons):
            is_negated = self.xor_metadata[i]['negated']
            
            val = node(x)
            if is_negated:
                val = 1.0 - val
            factors.append(val)
            
        # 3. AND Operation (Product)
        if not factors:
            # TRUE (1)
            return torch.ones((x.shape[0], 1), device=x.device, dtype=x.dtype)
            
        result = factors[0]
        for f in factors[1:]:
            result = result * f
            
        return result

    def get_structure_description(self):
        parts = []
        for item in self.direct_inputs:
            z = f"z{item['z_idx']}"
            if item['negated']:
                parts.append(f"NOT({z})")
            else:
                parts.append(z)
                
        for i, node in enumerate(self.xor_neurons):
            indices = node.variable_indices
            vars = [f"z{node.n_vars - 1 - (v//2)}" for v in indices]
            xor_str = " XOR ".join(vars)
            s = f"({xor_str})"
            if self.xor_metadata[i]['negated']:
                s = f"NOT{s}"
            parts.append(s)
            
        return " AND ".join(parts) if parts else "TRUE"


class LogicGuidedNN(nn.Module):
    def __init__(self, feature_expander: Any):
        super(LogicGuidedNN, self).__init__()
        
        if feature_expander.structure is None:
            raise ValueError("FeatureExpander must be fitted and have a valid structure.")
            
        self.n_vars = len(feature_expander.variables)
        self.structure = feature_expander.structure
        self.use_continuous = feature_expander.use_continuous_relaxation
        
        # Hidden Layer 1: Structural Terms
        # We use a ModuleList to hold distinct TermNeurons
        self.term_neurons = nn.ModuleList()
        
        for term_structure in self.structure:
            if not term_structure:
                 # Logic 1 (Bias/Intercept term essentially)
                 # We can handle this by a TermNeuron that returns 1, or just skip and let Regressor bias handle it?
                 # Better to have it explicit if we want isomorphism.
                 # An empty AND is TRUE (1).
                 pass
            
            term_node = TermNeuron(term_structure, self.n_vars, self.use_continuous)
            self.term_neurons.append(term_node)
            
        self.n_terms = len(self.term_neurons)
        
        # 2. Linear Output (Regressor)
        self.regressor = nn.Linear(self.n_terms, 1)
        
    def forward(self, x):
        # 1. Evaluate all term nodes
        term_outputs = [node(x) for node in self.term_neurons]
        
        if not term_outputs:
             # Should return bias?
             return self.regressor(torch.zeros((x.shape[0], 0), device=x.device))
             
        # Concatenate outputs: (Batch, n_terms)
        logic_layer_out = torch.cat(term_outputs, dim=1)
        
        # 2. Regression
        return self.regressor(logic_layer_out)
        
    def explain_structure(self):
        """
        Prints the hierarchical logical structure.
        """
        print("\n=== Logic-Guided NN Structure ===")
        print(f"Input Variables: {self.n_vars} (z0..z{self.n_vars-1})")
        print("\nHidden Layer (Logic terms):")
        for i, node in enumerate(self.term_neurons):
            desc = node.get_structure_description()
            print(f"  Neuron {i}: {desc}")
        print("\nOutput Layer:")
        print("  Linear Combination of neurons -> Prediction")
        print("=================================\n")


def build_logic_guided_model(feature_expander):
    """Factory function to build a model (just initializes the class in PyTorch)."""
    return LogicGuidedNN(feature_expander)
