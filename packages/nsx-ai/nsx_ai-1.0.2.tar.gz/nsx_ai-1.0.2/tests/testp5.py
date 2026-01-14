import src.nsx as ns
from src.nsx.agent import LLMInterface, LogicTranslator

def test_translator():
    print("--- Phase 5.2: Text-to-Logic Translator ---")

    # 1. Setup Context (Our Vocabulary)
    # Humein LLM ko batana padega ki humare paas ye concepts hain
    IsZorg = ns.Predicate("IsZorg", 1)
    HasAntenna = ns.Predicate("HasAntenna", 1)
    IsBleeb = ns.Predicate("IsBleeb", 1)
    HasSixEyes = ns.Predicate("HasSixEyes", 1)
    
    vocab = [IsZorg, HasAntenna, IsBleeb, HasSixEyes]

    # 2. Initialize Agent
    # Make sure API keys are set!
    try:
        client = LLMInterface(model_name="gpt-3.5-turbo") # Or any cheap model
        translator = LogicTranslator(client)
    except Exception as e:
        print(f"Skipping test due to connection/import error: {e}")
        return

    # 3. Test: English -> Code
    user_input = "If it is a Zorg, then it must have an Antenna."
    print(f"\nUser Input: '{user_input}'")
    
    try:
        rules = translator.text_to_rules(user_input, predicates=vocab)
        
        print(f"Generated Rule Object: {rules[0]}")
        print(f"Internal Type: {type(rules[0])}")
        
        # Verify correctness
        # Expected: HasAntenna(x) :- IsZorg(x)
        expected_repr = "HasAntenna(x) :- IsZorg(x)"
        # Note: Variable names might vary (x, y) depending on LLM, but structure should match.
        if "HasAntenna" in str(rules[0]) and "IsZorg" in str(rules[0]):
             print("✅ Logic Structure Verified!")
        else:
             print("❌ Logic Mismatch.")

    except Exception as e:
        print(f"❌ Translation Failed: {e}")

    # 4. Test: Code -> English
    print("\nTesting Explanation (Code -> English)...")
    # Rule: HasSixEyes(x) :- IsBleeb(x)
    complex_rule = HasSixEyes(ns.Variable('x')) << IsBleeb(ns.Variable('x'))
    
    explanation = translator.explain_rule(complex_rule)
    print(f"Rule: {complex_rule}")
    print(f"Agent Explanation: {explanation}")

if __name__ == "__main__":
    test_translator()