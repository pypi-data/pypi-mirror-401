from typing import List, Union, Tuple
from dataclasses import dataclass
from .symbols import Term

# 1. Forward Declaration of Rule (Trick to avoid circular errors)
class Rule:
    pass

# 2. LogicExpression Base
class LogicExpression:
    def __and__(self, other):
        return And(self, other)
    
    def __or__(self, other):
        return Or(self, other)
    
    def __invert__(self):
        return Not(self)
    
    def __rshift__(self, head):
        # Syntax: Body >> Head
        return Rule(head=head, body=self) # LogicExpression ab Rule bana sakta hai

# 3. Structural Classes
@dataclass(frozen=True)
class Predicate:
    name: str
    arity: int
    def __call__(self, *args: Term) -> 'Atom':
        if len(args) != self.arity:
            raise ValueError(f"Predicate '{self.name}' expects {self.arity} terms.")
        return Atom(self, args)
    def __repr__(self):
        return self.name

@dataclass(frozen=True)
class Atom(LogicExpression):
    predicate: Predicate
    terms: Tuple[Term, ...]
    
    def __lshift__(self, body: LogicExpression):
        # Syntax: Head << Body
        return Rule(head=self, body=body)

    def __repr__(self):
        terms_str = ", ".join(map(str, self.terms))
        return f"{self.predicate.name}({terms_str})"

# 4. Compositional Classes
@dataclass(frozen=True)
class And(LogicExpression):
    left: LogicExpression
    right: LogicExpression
    def __repr__(self): return f"({self.left} & {self.right})"

@dataclass(frozen=True)
class Or(LogicExpression):
    left: LogicExpression
    right: LogicExpression
    def __repr__(self): return f"({self.left} | {self.right})"

@dataclass(frozen=True)
class Not(LogicExpression):
    expression: LogicExpression
    def __repr__(self): return f"~{self.expression}"

# 5. Rule Class (Actual Definition)
@dataclass(frozen=True)
class Rule:
    head: Atom
    body: LogicExpression
    def __repr__(self): return f"{self.head} :- {self.body}"