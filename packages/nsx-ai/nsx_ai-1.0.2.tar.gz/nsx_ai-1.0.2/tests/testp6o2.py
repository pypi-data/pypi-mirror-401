import torch
import src.nsx as ns
from src.nsx.core.tnorms import get_logic_engine

def test_log_stability():
    print("--- Phase 6.2: Log-Space Stability Test ---")

    # 1. Setup Data (Small probabilities)
    # 0.5 * 0.5 * 0.5 ... (10 times) -> Very small number in linear space
    val_prob = torch.tensor(0.5)
    val_log = torch.log(val_prob) # -0.693

    # 2. Compare Linear vs Log Product
    linear_eng = get_logic_engine("product")
    log_eng = get_logic_engine("log_product")

    # Simulate a Deep Chain: A & B & C & D ... (10 times)
    res_linear = val_prob
    res_log = val_log

    for _ in range(10):
        res_linear = linear_eng.and_op(res_linear, val_prob)
        res_log = log_eng.and_op(res_log, val_log)

    print(f"Linear Result (0.5^11): {res_linear.item():.10f}")
    print(f"Log Result (in Log Space): {res_log.item():.4f}")
    
    # Convert Log back to Linear to check accuracy
    res_log_converted = torch.exp(res_log)
    print(f"Log Result (Converted):   {res_log_converted.item():.10f}")

    # Check Difference
    diff = torch.abs(res_linear - res_log_converted)
    if diff < 1e-6:
        print("✅ Log Logic is Accurate!")
    else:
        print("❌ Precision Mismatch.")

    # 3. Test Loss Handling
    # If Truth is High (1.0), LogTruth is 0.0. Loss should be 0.
    # If Truth is Low (0.1), LogTruth is -2.3. Loss should be 2.3.
    
    # Mocking Semantic Loss Calculation
    truth_log = torch.tensor(-2.3) # Low probability
    loss = -1.0 * truth_log
    print(f"Loss for Log-Prob(-2.3): {loss.item()} (Should be positive)")

if __name__ == "__main__":
    test_log_stability()