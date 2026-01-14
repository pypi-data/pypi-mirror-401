import torch
from typing import Dict, Any

from ..core.symbols import Variable, Constant, Term
from ..core.logic import Atom, And, Or, Not, Rule, LogicExpression
from ..core.tnorms import TNorm


class LogicEvaluator:
    """
    Evaluates a Logic Expression Tree using Neural Networks and T-Norms.
    """
    def __init__(self, tnorm: TNorm, concept_map: Dict[str, Any]):
        """
        tnorm: Math Engine (Product, Godel, etc.)
        concept_map: Mapping { PredicateName: NeuralConcept }
        """
        self.tnorm = tnorm
        self.concept_map = concept_map

    def evaluate(self, expr: LogicExpression, data_binding: Dict[Variable, torch.Tensor]) -> torch.Tensor:
        """
        Recursive function to compute Truth Value.
        
        data_binding: Maps Logic Variables (x) to Real Data (Image Tensors).
        Example: { Variable('img'): tensor_batch_images }
        """
        
        # Case 1: Base Case (The Atom) -> Run Neural Net
        if isinstance(expr, Atom):
            predicate_name = expr.predicate.name
            
            # Find the Neural Network for this predicate
            if predicate_name not in self.concept_map:
                raise ValueError(f"No Neural Concept mapped for predicate: {predicate_name}")
            
            neural_concept = self.concept_map[predicate_name]
            
            # Get the input data for this atom's arguments
            # Assuming unary predicate for now: Smokes(x) -> x is input
            # Future: Handle binary like Friends(x, y)
            term = expr.terms[0] 
            
            if isinstance(term, Variable):
                if term not in data_binding:
                    raise ValueError(f"Variable '{term}' is not bound to any data.")
                input_data = data_binding[term]
            else:
                # Handle Constants (Not implemented for Phase 3 simple test)
                raise NotImplementedError("Constants not yet supported in neural binding.")

            # RUN THE NEURAL NET!
            return neural_concept(input_data)

        # Case 2: AND Operation
        elif isinstance(expr, And):
            left_val = self.evaluate(expr.left, data_binding)
            right_val = self.evaluate(expr.right, data_binding)
            return self.tnorm.and_op(left_val, right_val)

        # Case 3: OR Operation
        elif isinstance(expr, Or):
            left_val = self.evaluate(expr.left, data_binding)
            right_val = self.evaluate(expr.right, data_binding)
            return self.tnorm.or_op(left_val, right_val)

        # Case 4: NOT Operation
        elif isinstance(expr, Not):
            val = self.evaluate(expr.expression, data_binding)
            return self.tnorm.not_op(val)

        # Case 5: Rule (Implication)
        elif isinstance(expr, Rule):
            body_val = self.evaluate(expr.body, data_binding)
            head_val = self.evaluate(expr.head, data_binding)
            return self.tnorm.implies_op(body_val, head_val)
        
        else:
            raise TypeError(f"Unknown logic expression type: {type(expr)}")