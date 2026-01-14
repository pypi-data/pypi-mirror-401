# -- Variables and Constants -- 
from dataclasses import dataclass 
from typing import Union 

@dataclass(frozen=True)
class Term: 
    """
    Base Class for all symbolic terms. 
    frozen=True makes it immutable (hashable), so we can use it in sets/dicts.
    """
    name: str 
    
    def __repr__(self):
        return self.name
    

@dataclass(frozen=True)
class Variable(Term):
    """
    Represents a placeholder like x, y, z. 
    Values will be added during execution. 
    """
    pass 

@dataclass(frozen=True)
class Constant(Term):
    """
    Represents a constant like alice, bob, number_1. 
    Values will be added during execution. 
    """
    pass