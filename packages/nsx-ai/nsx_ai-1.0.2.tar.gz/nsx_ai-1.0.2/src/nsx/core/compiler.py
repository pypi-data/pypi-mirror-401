import torch
import torch.nn as nn
from typing import Dict, Any

from .logic import Rule, Atom, And, Or, Not, LogicExpression
from .tnorms import TNorm
from .symbols import Variable


class LogicModule(nn.Module):
    """Base class for all compiled logic operations."""
    def __init__(self, tnorm: TNorm):
        super().__init__()
        self.tnorm = tnorm

    def forward(self, data_binding: Dict[Variable, torch.Tensor]) -> torch.Tensor:
        raise NotImplementedError

class AtomModule(LogicModule):
    def __init__(self, atom: Atom, concept_map: Dict[str, Any], tnorm: TNorm):
        super().__init__(tnorm)
        self.predicate_name = atom.predicate.name
        self.terms = atom.terms
        
        if self.predicate_name not in concept_map:
            raise ValueError(f"Predicate '{self.predicate_name}' has no registered Neural Model.")
        
        self.concept = concept_map[self.predicate_name]

    def forward(self, data_binding):
        # 1. Resolve All Inputs
        input_tensors = []
        for term in self.terms:
            if isinstance(term, Variable):
                if term not in data_binding:
                    raise ValueError(f"Variable '{term}' bound to data.")
                input_tensors.append(data_binding[term])
            else:
                # Future: Support Constants
                raise NotImplementedError("Constants not supported in compiler yet.")
            
        # 2. Forward Pass with Unpacked Arguments
        # The NeuralConcept.forward takes *args
        return self.concept(*input_tensors)

class AndModule(LogicModule):
    def __init__(self, expression: And, concept_map, tnorm):
        super().__init__(tnorm)
        self.left = compile_expression(expression.left, concept_map, tnorm)
        self.right = compile_expression(expression.right, concept_map, tnorm)

    def forward(self, data_binding):
        return self.tnorm.and_op(
            self.left(data_binding), 
            self.right(data_binding)
        )

class OrModule(LogicModule):
    def __init__(self, expression: Or, concept_map, tnorm):
        super().__init__(tnorm)
        self.left = compile_expression(expression.left, concept_map, tnorm)
        self.right = compile_expression(expression.right, concept_map, tnorm)

    def forward(self, data_binding):
        return self.tnorm.or_op(
            self.left(data_binding), 
            self.right(data_binding)
        )

class NotModule(LogicModule):
    def __init__(self, expression: Not, concept_map, tnorm):
        super().__init__(tnorm)
        self.sub_module = compile_expression(expression.expression, concept_map, tnorm)

    def forward(self, data_binding):
        return self.tnorm.not_op(self.sub_module(data_binding))

class RuleModule(LogicModule):
    """
    Top-Level compiled Module for a Rule.
    Calculates Truth Value of the Implication.
    """
    def __init__(self, rule: Rule, concept_map, tnorm):
        super().__init__(tnorm)
        self.head = compile_expression(rule.head, concept_map, tnorm)
        self.body = compile_expression(rule.body, concept_map, tnorm)

    def forward(self, data_binding):
        head_val = self.head(data_binding)
        body_val = self.body(data_binding)
        return self.tnorm.implies_op(body_val, head_val)

# Factory Function (Recursive Compiler)
def compile_expression(expr: LogicExpression, concept_map: Dict, tnorm: TNorm) -> LogicModule:
    """
    Recursively turns a Logic Expression Object (Python) into a LogicModule (PyTorch).
    """
    if isinstance(expr, Atom):
        return AtomModule(expr, concept_map, tnorm)
    elif isinstance(expr, And):
        return AndModule(expr, concept_map, tnorm)
    elif isinstance(expr, Or):
        return OrModule(expr, concept_map, tnorm)
    elif isinstance(expr, Not):
        return NotModule(expr, concept_map, tnorm)
    elif isinstance(expr, Rule):
        return RuleModule(expr, concept_map, tnorm)
    else:
        raise TypeError(f"Unknown logic type: {type(expr)}")