import torch
import torch.nn as nn
from typing import Callable, Union, Tuple

class NeuralConcept(nn.Module):
    """
    Acts as a bridge between a Logic Predicate and a Neural Network.
    Updated to support Relational Predicates (Arity > 1).
    """
    def __init__(self, name: str, module: nn.Module, output_index: int = None):
        super().__init__()
        self.name = name
        self.module = module
        self.output_index = output_index 

    def forward(self, *args: torch.Tensor) -> torch.Tensor:
        """
        Runs the neural net. 
        If multiple args are passed (e.g., Friends(x, y)), they are passed to the module.
        The user's module is responsible for handling concatenation or broadcasting if needed.
        """
        # Pass all arguments to the underlying network
        # Example: net(x) or net(x, y)
        output = self.module(*args)

        # Handle Output Indexing (for Softmax/Multi-class)
        if self.output_index is not None:
            # We assume the last dimension is the class dimension
            # Shape could be (Batch,) or (Batch_A, Batch_B, Classes)
            if output.dim() > 1:
                return output[..., self.output_index] # Use Ellipsis (...) for flexible dims
            else:
                return output[self.output_index]
        
        # If binary classifier output (Batch, 1) -> Squeeze to (Batch,)
        return output.squeeze(-1) if output.dim() > 1 and output.shape[-1] == 1 else output

    def __repr__(self):
        return f"NeuralConcept({self.name})"