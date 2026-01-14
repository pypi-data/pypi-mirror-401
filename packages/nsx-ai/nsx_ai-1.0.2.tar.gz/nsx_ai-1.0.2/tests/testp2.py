import torch
from src.nsx.config import conf
from src.nsx.core.tnorms import get_logic_engine

def test_math_engine():
    print("--- Phase 2 Test: Math Engine ---")
    
    # 1. Select Logic
    conf.logic = "product"
    engine = get_logic_engine(conf.logic)
    print(f"Using Logic: {conf.logic}")

    # 2. Create Dummy Tensors (Predictions from a Neural Net)
    # requires_grad=True is important! Tabhi backprop hoga.
    prob_rain = torch.tensor(0.8, requires_grad=True) 
    prob_umbrella = torch.tensor(0.4, requires_grad=True)

    # 3. Test AND Operation (Rain AND Umbrella)
    # Product Logic: 0.8 * 0.4 = 0.32
    result_and = engine.and_op(prob_rain, prob_umbrella)
    print(f"Rain(0.8) AND Umbrella(0.4) = {result_and.item():.4f}")

    # 4. Test IMPLIES Operation (Rule)
    # Rule: Rain -> Umbrella (Agar barish hai to chhata hona chahiye)
    # Reichenbach: 1 - 0.8 + (0.8 * 0.4) = 0.2 + 0.32 = 0.52
    result_rule = engine.implies_op(prob_rain, prob_umbrella)
    print(f"Rule (Rain -> Umbrella) Truth: {result_rule.item():.4f}")

    # 5. Gradient Check (The most crucial part)
    # Maan lo hum chahte hain Rule Truth 1.0 ho.
    # Loss = 1 - Truth
    loss = 1.0 - result_rule
    loss.backward()

    print("\n--- Gradient Flow Check ---")
    print(f"Loss: {loss.item():.4f}")
    # Agar Gradient Non-Zero hai, iska matlab Neural Net seekh payega!
    print(f"Grad Rain: {prob_rain.grad.item():.4f}") 
    print(f"Grad Umbrella: {prob_umbrella.grad.item():.4f}")

    if prob_rain.grad is not None and prob_umbrella.grad is not None:
        print("✅ Success: Gradients are flowing through logic!")
    else:
        print("❌ Failed: No gradients.")

if __name__ == "__main__":
    test_math_engine()