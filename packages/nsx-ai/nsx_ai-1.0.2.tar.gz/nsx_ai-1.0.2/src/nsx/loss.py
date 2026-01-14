import torch
import torch.nn as nn
from typing import List, Dict, Any

from .config import conf
from .core.tnorms import get_logic_engine
from .core.symbols import Variable
from .core.logic import Rule

# NEW: Import the compiler
from .core.compiler import compile_expression

class SemanticLoss(nn.Module):
    """
    Optimized Semantic Loss using Graph Compilation.
    """
    def __init__(self, concept_map: Dict[str, Any], logic: str = None):
        super().__init__()
        logic_type = logic if logic else conf.logic
        self.tnorm = get_logic_engine(logic_type)
        self.concept_map = concept_map
        
        # Cache for compiled rules
        # Dictionary mapping { rule_object_id : CompiledModule }
        self.compiled_rules = nn.ModuleDict() 

    def forward(self, rules: List[Rule], data_binding: Dict[Variable, torch.Tensor]) -> torch.Tensor:
        total_loss = torch.tensor(0.0, device=next(iter(data_binding.values())).device)
        logic_type = self.tnorm.__class__.__name__

        # Handle Input Conversion (Auto-Log)
        # If using LogLogic, ensure inputs are Logs.
        # This is a bit hacky but effective: 
        # We assume data_binding contains Probs (0-1). If logic is LogProduct, we convert them.
        if isinstance(self.tnorm, type(get_logic_engine("log_product"))):
            # Create a shallow copy so we don't modify original binding outside
            # Note: This works for simple Variables.
            log_binding = {}
            for k, v in data_binding.items():
                # Avoid log(0) error by clamping
                log_binding[k] = torch.log(torch.clamp(v, min=1e-7, max=1.0))
            active_binding = log_binding
        else:
            active_binding = data_binding

        # ... (Compiler logic from Phase 6.1 same here) ...
        # Ensure compiled modules use the *current* active_binding
        
        for i, rule in enumerate(rules):
            rule_key = str(id(rule))
            if rule_key not in self.compiled_rules:
                compiled_module = compile_expression(rule, self.concept_map, self.tnorm)
                device = next(iter(data_binding.values())).device
                compiled_module.to(device)
                self.compiled_rules[rule_key] = compiled_module
            
            evaluator = self.compiled_rules[rule_key]
            
            # Run Evaluator
            rule_output = evaluator(active_binding)
            
            # LOSS CALCULATION CHANGE
            if isinstance(self.tnorm, type(get_logic_engine("log_product"))):
                # In Log Space, Truth = 0.0 (because log(1) = 0). 
                # Output is a negative number (e.g., -0.5).
                # We want to maximize truth (make it closer to 0).
                # So Loss = -1 * output (Minimize the negative log probability)
                violation = -1.0 * rule_output
            else:
                # Standard Space (0 to 1)
                # We want Truth = 1.0
                violation = 1.0 - rule_output
            
            total_loss += violation.mean()
            
        return total_loss / len(rules)