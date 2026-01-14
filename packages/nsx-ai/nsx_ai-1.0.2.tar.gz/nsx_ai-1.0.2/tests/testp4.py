import torch
import torch.nn as nn
import torch.optim as optim

# Import your Framework
import src.nsx as ns

def test_user_workflow():
    print("--- Phase 4: User Workflow Demo ---")

    # ================================
    # 1. Define Logic (Business Rules)
    # ================================
    x = ns.Variable("x")
    
    # Define Predicates
    IsDigitZero = ns.Predicate("IsDigitZero", arity=1)
    IsEven = ns.Predicate("IsEven", arity=1)

    # Define Rule: "If it's Zero, it MUST be Even"
    # Logic: IsEven(x) :- IsDigitZero(x)
    rule_safety = IsEven(x) << IsDigitZero(x)
    print(f"✅ Rule Defined: {rule_safety}")


    # ================================
    # 2. Define Neural Network (Standard PyTorch)
    # ================================
    class SimpleClassifier(nn.Module):
        def __init__(self):
            super().__init__()
            # Input: 10 features, Output: 2 classes (Zero, Even)
            self.layer = nn.Linear(10, 2)
            self.sigmoid = nn.Sigmoid() # Output 0-1 probabilities

        def forward(self, x):
            return self.sigmoid(self.layer(x))

    net = SimpleClassifier()


    # ================================
    # 3. Connect Logic & Neural Net
    # ================================
    model = ns.NeuroSymbolicModel(net)
    
    # Map Neural Outputs to Predicates
    # Output[0] -> IsDigitZero
    # Output[1] -> IsEven
    model.register(IsDigitZero, output_index=0)
    model.register(IsEven, output_index=1)


    # ================================
    # 4. Training Setup
    # ================================
    # Initialize our Semantic Loss
    criterion = ns.SemanticLoss(model.concept_map, logic="product")
    
    optimizer = optim.Adam(net.parameters(), lr=0.1)

    # Fake Data (Batch of 5 images)
    data = torch.randn(5, 10) 


    # ================================
    # 5. Training Loop (The Magic)
    # ================================
    print("\nStarting Training...")
    
    for epoch in range(5):
        optimizer.zero_grad()

        # Step A: Calculate Semantic Loss directly
        # Notice: We don't need labels! We just give data and rules.
        loss = criterion(
            rules=[rule_safety], 
            data_binding={x: data}
        )
        
        # Step B: Standard Backprop
        loss.backward()
        optimizer.step()

        print(f"Epoch {epoch+1} | Semantic Loss: {loss.item():.4f}")

    print("\n✅ Training Complete! Logic has optimized the Neural Network.")

if __name__ == "__main__":
    test_user_workflow()