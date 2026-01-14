import torch
import torch.nn as nn
import src.nsx as ns
from src.nsx.core.logic import Rule

def test_relational_logic():
    print("--- Phase 6.3: Relational Logic & Broadcasting ---")

    # 1. Define Logic
    # We want to find pairs of objects that have the same color.
    # Rule: SameColor(x, y) :- Red(x) & Red(y)
    # This implies: If both are Red, they are the Same Color.
    
    x = ns.Variable("x")
    y = ns.Variable("y")
    
    IsRed = ns.Predicate("IsRed", 1)
    SameColor = ns.Predicate("SameColor", 2) # Arity 2
    
    # Logic: SameColor(x, y) << IsRed(x) & IsRed(y)
    rule = SameColor(x, y) << (IsRed(x) & IsRed(y))

    # 2. Define Network
    # A generic net that handles image features
    class ColorNet(nn.Module):
        def forward(self, inputs):
            # Dummy: determines probability of being Red based on input value
            # Assume input is just a scalar for simplicity. >0 means Red.
            return torch.sigmoid(inputs)

    # A relational net (Siamese style)
    class RelationNet(nn.Module):
        def forward(self, input_x, input_y):
            # This net needs to return similarity between x and y.
            # We rely on Broadcasting! 
            # If x is (N, 1) and y is (1, M), PyTorch ops will make (N, M)
            
            # Simple similarity: exp(-distance)
            diff = input_x - input_y
            return torch.exp(-torch.abs(diff))

    net_color = ColorNet()
    net_rel = RelationNet()

    # 3. Setup Model
    # Since we have different nets for different predicates, we can wrap them loosely 
    # or just register them to the NeuroSymbolicModel
    
    # We create a dummy container since NeuroSymbolicModel usually wraps one net,
    # but here we have distinct modules.
    # In practice, users might have one big net or multiple.
    # Let's manually map for this advanced test case.
    
    concept_map = {
        "IsRed": ns.bridge.NeuralConcept("IsRed", net_color),
        "SameColor": ns.bridge.NeuralConcept("SameColor", net_rel)
    }
    
    # 4. Data (Broadcasting Setup)
    # Batch X: 3 items (Strong Red, Weak Red, Not Red)
    data_x = torch.tensor([[10.0], [5.0], [-5.0]]) # Shape (3, 1)
    
    # Batch Y: 3 items (Same as X) transposed for matrix comparison
    data_y = data_x.T # Shape (1, 3) --> Broadcasting Trigger!
    
    # Note: Variable 'x' in logic binds to 'data_x'
    # Variable 'y' in logic binds to 'data_y'
    # But wait, in the rule SameColor(x, y) << IsRed(x) & IsRed(y)
    # IsRed(x) needs data_x (3, 1). Result (3, 1).
    # IsRed(y) needs data_y (1, 3). Result (1, 3).
    # AND Op: (3, 1) & (1, 3) -> Result (3, 3) Matrix!
    
    # 5. Execute Loss
    criterion = ns.SemanticLoss(concept_map, logic="product")
    
    # We bind x to data_x, y to data_y_reshaped
    data_binding = {
        x: data_x,            # (3, 1)
        y: data_x.reshape(1, 3) # (1, 3)
    }
    
    # Evaluate
    # Internal math:
    # IsRed(x) -> [0.99, 0.99, 0.01] (Column)
    # IsRed(y) -> [0.99, 0.99, 0.01] (Row)
    # Body (x & y) -> 3x3 Matrix of probabilities
    # Head (SameColor) -> 3x3 Matrix from RelationNet
    
    loss = criterion([rule], data_binding)
    print(f"Relational Loss: {loss.item():.4f}")
    
    # Check if we got a matrix calculation implicitly
    # Access the compiled rule output to verify shape
    compiled_rule = criterion.compiled_rules[str(id(rule))]
    output = compiled_rule(data_binding)
    
    print(f"Output Shape: {output.shape}")
    if output.shape == (3, 3):
        print("✅ Broadcasting Success: Computed logic for all 3x3 pairs!")
    else:
        print(f"❌ Shape Mismatch: Expected (3,3), got {output.shape}")

if __name__ == "__main__":
    test_relational_logic()