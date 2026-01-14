import src.nsx as ns
from src.nsx.agent import LLMInterface, RuleMiner, LogicGuard

def test_advanced_agent():
    print("--- Phase 5.3: Scientist & Guard Test ---")
    
    try:
        client = LLMInterface(model_name="gpt-3.5-turbo")
    except:
        print("Skipping: Connection setup failed.")
        return

    # ================================
    # Test 1: Rule Discovery (The Scientist)
    # ================================
    print("\n[1] Testing Rule Miner...")
    
    # Context: A Bank Fraud Dataset
    x = ns.Variable("x")
    IsFraud = ns.Predicate("IsFraud", 1)
    HighAmount = ns.Predicate("HighAmount", 1)
    ForeignIP = ns.Predicate("ForeignIP", 1)
    
    miner = RuleMiner(client)
    
    suggestions = miner.propose_rules(
        data_description="Financial transaction data containing amount details and IP locations.",
        predicates=[IsFraud, HighAmount, ForeignIP]
    )
    
    for i, s in enumerate(suggestions):
        print(f"Hypothesis {i+1}: {s['description']}")
        print(f"  -> Code: {s['rule']}")
        
        # Verify it created a valid Rule object
        if isinstance(s['rule'], ns.Rule):
            print("  ✅ Valid Rule Object")

    # ================================
    # Test 2: Logic Guard (The Safety Layer)
    # ================================
    print("\n[2] Testing Logic Guard...")
    
    guard = LogicGuard(client)
    
    # Defined Rule: Max Discount is 50%
    # We can't express "50%" easily in simple predicates without arithmetic, 
    # but let's assume a conceptual rule for the text check.
    # Logic: Safe(x) :- Verified(x)
    # Let's use the bank example rules we just mined or defined.
    # Rule: Fraud(x) :- ForeignIP(x) & HighAmount(x)
    
    hard_rule = ns.Rule(
        head=IsFraud(x), 
        body=ForeignIP(x) & HighAmount(x)
    )
    
    # Case A: AI says something conflicting
    # AI Claim: "This transaction from a Foreign IP with High Amount is definitely SAFE."
    # Logic says: It implies FRAUD.
    ai_response = "Don't worry, the transaction from Nigeria (Foreign) with $1M (High) is perfectly safe and verified."
    
    check = guard.verify(response_text=ai_response, rules=[hard_rule])
    
    print(f"AI Claim: '{ai_response}'")
    print(f"Guard Verdict: Is Safe? {check['is_safe']}")
    if not check['is_safe']:
        print(f"Violation: {check['violation_reason']}")
        print("✅ Guard successfully blocked the hallucination!")

if __name__ == "__main__":
    test_advanced_agent()