import torch
import torch.nn as nn
import time
import src.nsx as ns
from src.nsx.core.logic import Rule

def test_compiler():
    print("--- Phase 6.1: Logic Compilation & Vectorization ---")

    # 1. Setup Logic
    x = ns.Variable("x")
    IsCat = ns.Predicate("IsCat", 1)
    HasWhiskers = ns.Predicate("HasWhiskers", 1)
    
    # Rule: IsCat(x) -> HasWhiskers(x)
    rule = HasWhiskers(x) << IsCat(x)

    # 2. Dummy Neural Net
    class MockNet(nn.Module):
        def forward(self, x):
            # Simulating output for 1000 images
            # Batch size = 1000
            # Col 0: IsCat, Col 1: HasWhiskers
            return torch.rand(x.shape[0], 2, requires_grad=True)

    net = MockNet()
    model = ns.NeuroSymbolicModel(net)
    model.register(IsCat, 0)
    model.register(HasWhiskers, 1)

    # 3. Init Semantic Loss (This now uses the Compiler)
    criterion = ns.SemanticLoss(model.concept_map, logic="product")

    # 4. Data
    data = torch.randn(1000, 5) # Batch of 1000

    # 5. Run Forward (First time: Compiles. Second time: Uses Cache)
    start_time = time.time()
    loss = criterion([rule], {x: data})
    loss.backward()
    end_time = time.time()

    print(f"Loss: {loss.item():.4f}")
    print(f"Execution Time (First Run + Compile): {end_time - start_time:.4f}s")

    # 6. Run again (Should be faster)
    start_time = time.time()
    loss = criterion([rule], {x: data})
    loss.backward()
    end_time = time.time()
    
    print(f"Execution Time (Cached): {end_time - start_time:.4f}s")
    
    # Check structure
    if hasattr(criterion, 'compiled_rules') and len(criterion.compiled_rules) > 0:
        print("✅ Compiler Active: Logic Tree converted to nn.Module")
    else:
        print("❌ Compiler Failed")

if __name__ == "__main__":
    test_compiler()