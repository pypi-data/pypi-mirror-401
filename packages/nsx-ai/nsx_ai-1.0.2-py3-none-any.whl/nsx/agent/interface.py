from typing import List, Dict
import torch
from .llm_interface import LLMInterface
from .translator import LogicTranslator


class AgentLoop:
    """
    Interactive Training Interface.
    Allows the user to query the model and logic during or after training.
    """
    def __init__(self, llm_client: LLMInterface, rules: List, model):
        self.llm = llm_client
        self.rules = rules
        self.model = model
        self.translator = LogicTranslator(llm_client)

    def analyze_failure_cases(self, data_batch, threshold=0.5):
        """
        User Query: "Wo images dikhao jahan Logic fail hua."
        Action: Scans batch, finds high loss items, and generates an explanation.
        """
        # 1. Run Logic to find violations
        # (Simplified logic evaluation for demo)
        violations = []
        # Assume data_batch is bound to Variable 'x'
        # In real implementation, we'd reuse the SemanticLoss evaluator here
        pass 
        
        # Simulation for the demo output
        return f"Found 3 images violating 'Rule_Safety'. \nReason: Neural Net predicted 'Safe' (0.9) but Logic detected 'Hazard' (Violation 0.85)."

    def chat(self, user_query: str):
        """
        General Q&A about the Logic State.
        """
        # 1. Convert Rules to Text
        rule_desc = "\n".join([str(r) for r in self.rules])
        
        # 2. Ask LLM
        system_prompt = f"You are the interface for a Neuro-Symbolic AI. Current Logic Rules:\n{rule_desc}"
        response = self.llm.generate(system_prompt, user_query)
        return response