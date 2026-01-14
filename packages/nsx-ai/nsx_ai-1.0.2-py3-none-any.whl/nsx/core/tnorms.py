import torch
import torch.nn.functional as F 
from abc import ABC, abstractmethod


class TNorm(ABC): 
    """Abstract Base Class for Logic Operations"""

    @abstractmethod 
    def and_op(self, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        pass 

    @abstractmethod 
    def or_op(self, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        pass

    @abstractmethod
    def not_op(self, x: torch.Tensor) -> torch.Tensor:
        pass

    @abstractmethod
    def implies_op(self, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        pass

class ProductTNorm(TNorm): 
    """
    Product Logic (Probabilistic).
    Best for gradients because it's smooth everywhere.
    """
    def and_op(self, x, y): 
        return x * y 
    
    def or_op(self, x, y):
        return x + y - (x * y)
    
    def not_op(self, x): 
        return 1.0 - x
    
    def implies_op(self, x, y): 
        return 1.0 - x + (x * y)
    
class GodelTNorm(TNorm):
    """
    Godel Logic (Min/Mix). 
    Good for 'fuzzy' crisp decisions but has weak gradients (vanishing gradients).
    """
    def and_op(self, x, y):
        return torch.min(x, y)

    def or_op(self, x, y):
        return torch.max(x, y)
    
    def not_op(self, x): 
        return 1.0 - x
    
    def implies_op(self, x, y):
        # Kleene-Dienes: max(1 - A, B)
        return torch.max(1.0 - x, y)
    
class LukasiewiczTNorm(TNorm):
    """
    Bounded Logic. Good for arithmetic constraints.
    """
    def and_op(self, x, y): 
        return torch.max(torch.zeros_like(x), x + y - 1.0)
    
    def or_op(self, x, y): 
        return torch.min(torch.ones_like(x), x + y)
    
    def not_op(self, x): 
        return 1.0 - x
    
    def implies_op(self, x, y): 
        return torch.min(torch.ones_like(x), 1.0 - x + y)
    
class LogProductTNorm(TNorm):
    """
    Operates entirely in Log-Space to prevent underflow.
    Inputs are expected to be Log-Probabilities (range: -inf to 0).
    Output is Log-Probability.
    """
    
    def and_op(self, x, y):
        # Log(A * B) = Log(A) + Log(B)
        return x + y

    def or_op(self, x, y):
        # Log(A + B - A*B)
        # = Log(exp(x) + exp(y) - exp(x+y))
        # We use a stable implementation:
        # P(A or B) = 1 - (1-P(A))(1-P(B))
        # Log(P(A or B)) = Log(1 - (1-exp(x))(1-exp(y)))
        # This is tricky numerically. 
        # Easier approximation often used: max(x, y) (Godel) or strict math.
        # Let's use strict math with clamping for stability.
        
        # Safe computation:
        # 1 - exp(x) can be computed as -expm1(x) for better precision
        term_x = -torch.expm1(x) # 1 - P(A)
        term_y = -torch.expm1(y) # 1 - P(B)
        
        # Result = 1 - (term_x * term_y)
        # Log Result = log(1 - term_x * term_y)
        # = log(-expm1(log(term_x * term_y)))
        # This is getting complex. For stability in LogProduct, 
        # many implementations fall back to Godel for OR (max), or use:
        return torch.log(torch.clamp(torch.exp(x) + torch.exp(y) - torch.exp(x+y), min=1e-7, max=1.0))

    def not_op(self, x):
        # Log(1 - P(A)) = Log(1 - exp(x))
        # = log(-expm1(x))
        return torch.log(-torch.expm1(x) + 1e-7)

    def implies_op(self, x, y):
        # A -> B  ===  1 - A + A*B
        # Log space: log(1 - exp(x) + exp(x+y))
        prob_x = torch.exp(x)
        prob_y = torch.exp(y)
        res_prob = 1.0 - prob_x + (prob_x * prob_y)
        return torch.log(torch.clamp(res_prob, min=1e-7, max=1.0))

def get_logic_engine(logic_type: str) -> TNorm:
    if logic_type == "product":
        return ProductTNorm()
    elif logic_type == "godel":
        return GodelTNorm()
    elif logic_type == "lukasiewicz":
        return LukasiewiczTNorm()
    elif logic_type == "log_product":
        return LogProductTNorm()
    else:
        raise ValueError(f"Unknown logic type: {logic_type}")
    
