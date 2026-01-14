import torch
import torch.nn as nn
from src.nsx.core.symbols import Variable
from src.nsx.core.logic import Predicate
from src.nsx.core.tnorms import get_logic_engine
from src.nsx.bridge import NeuralConcept, LogicEvaluator

def test_bridge():
    print("--- Phase 3 Test: The Bridge ---")

    # 1. Define Logic Symbols
    x = Variable("x")
    IsDigitZero = Predicate("IsDigitZero", 1)
    IsEven = Predicate("IsEven", 1)

    # 2. Define a Dummy Neural Network (Mocking a CNN)
    class MockCNN(nn.Module):
        def forward(self, images):
            # Pretend we processed images and output probabilities
            # Batch size = 2
            # Image 1: Prob(Zero)=0.9, Prob(Even)=0.8
            # Image 2: Prob(Zero)=0.1, Prob(Even)=0.2
            return torch.tensor([
                [0.9, 0.8], 
                [0.1, 0.2]
            ], requires_grad=True)

    net = MockCNN()

    # 3. Create Neural Concepts (Binding Logic to Net)
    # Output Index 0 -> IsDigitZero
    # Output Index 1 -> IsEven
    concept_zero = NeuralConcept("IsDigitZero", net, output_index=0)
    concept_even = NeuralConcept("IsEven", net, output_index=1)

    concept_map = {
        "IsDigitZero": concept_zero,
        "IsEven": concept_even
    }

    # 4. Define a Rule: IsDigitZero(x) -> IsEven(x)
    # (Agar digit Zero hai, to wo Even hona chahiye)
    rule = IsDigitZero(x) >> IsEven(x) # Using custom syntax (>> is not implemented yet, using manual Rule constr if needed, but lets use the one from logic.py)
    # Wait, in logic.py we used `Head << Body` or manual Rule. 
    # Let's use:
    rule = IsEven(x) << IsDigitZero(x) 
    # "IsEven if IsDigitZero" (Reverse notation used in Phase 1)
    # Or cleaner:
    # rule = Rule(head=IsEven(x), body=IsDigitZero(x))

    print(f"Evaluating Rule: {rule}")

    # 5. Setup Evaluator
    tnorm = get_logic_engine("product")
    evaluator = LogicEvaluator(tnorm, concept_map)

    # 6. Bind Data
    dummy_images = torch.randn(2, 10) # 2 images
    data_binding = {x: dummy_images}

    # 7. Run Logic Evaluation
    # This will recursively call MockCNN -> T-Norm -> Final Truth Score
    truth_values = evaluator.evaluate(rule, data_binding)

    print(f"\nTruth Values for Batch: {truth_values}")
    
    # Check Manual Calculation for Image 1:
    # Zero=0.9, Even=0.8
    # Rule (Zero -> Even) = 1 - 0.9 + (0.9*0.8) = 0.1 + 0.72 = 0.82
    expected_1 = 1.0 - 0.9 + (0.9 * 0.8)
    print(f"Expected Val 1: {expected_1:.4f}")
    
    # 8. Check Gradients
    loss = (1.0 - truth_values).mean()
    loss.backward()
    print("Gradient check: Success if no errors above.")

if __name__ == "__main__":
    test_bridge()