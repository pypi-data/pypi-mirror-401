from typing import List, Dict
from .llm_interface import LLMInterface
from .prompts import GUARD_SYSTEM_PROMPT
from ..core.logic import Rule


class LogicGuard:
    """
    Prevents hallucinations by validating AI output against Logic Rules.
    """
    def __init__(self, llm_client: LLMInterface):
        self.llm = llm_client

    def verify(self, response_text: str, rules: List[Rule]) -> Dict:
        """
        Checks if 'response_text' contradicts any 'rules'.
        """
        # 1. Convert Rules to readable text for the LLM
        rules_text = "\n".join([f"- {r}" for r in rules])
        
        user_prompt = f"STRICT LOGIC RULES:\n{rules_text}\n\nAI RESPONSE TO CHECK:\n\"{response_text}\""

        # 2. Get Verdict
        result = self.llm.generate_json(
            system_prompt=GUARD_SYSTEM_PROMPT,
            user_prompt=user_prompt
        )
        
        return result