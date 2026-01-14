from src.nsx.core.symbols import Variable, Constant
from src.nsx.core.logic import Predicate

def test_syntax():
    # 1. Define Terms
    x = Variable("x")
    y = Variable("y")
    alice = Constant("Alice")

    # 2. Define Predicates
    Smokes = Predicate("Smokes", 1)
    Friends = Predicate("Friends", 2)
    Cancer = Predicate("Cancer", 1)

    # 3. Create Rule using Python Operators
    # Rule: Cancer(x) :- Smokes(x) & Friends(x, y)
    rule_1 = Cancer(x) << (Smokes(x) & Friends(x, y))

    print("--- Phase 1 Test ---")
    print(f"Rule Created: {rule_1}")
    
    # Check Internal Structure
    assert rule_1.head.predicate.name == "Cancer"
    assert rule_1.body.left.predicate.name == "Smokes"
    print("✅ Syntax Check Passed: Framework structure is ready!")

if __name__ == "__main__":
    test_syntax()