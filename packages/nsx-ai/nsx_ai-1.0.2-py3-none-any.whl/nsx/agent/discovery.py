from typing import List, Dict
from .llm_interface import LLMInterface
from .prompts import DISCOVERY_SYSTEM_PROMPT
from ..core.logic import Rule, Predicate
from .translator import LogicTranslator 


class RuleMiner:
    """
    Automated Rule Discovery Agent.
    """
    def __init__(self, llm_client: LLMInterface):
        self.llm = llm_client
        # We reuse translator logic to parse the JSON rule structure
        self.translator = LogicTranslator(llm_client) 

    def propose_rules(self, data_description: str, predicates: List[Predicate]) -> List[Dict]:
        """
        Generates hypothesis rules based on data context.
        Returns a list of dicts with {'rule': RuleObject, 'description': str}
        """
        # 1. Prepare Prompt
        pred_info = ", ".join([f"{p.name}" for p in predicates])
        user_prompt = f"Dataset Context: {data_description}\nAvailable Predicates: [{pred_info}]"

        # 2. Query LLM
        response = self.llm.generate_json(
            system_prompt=DISCOVERY_SYSTEM_PROMPT,
            user_prompt=user_prompt
        )

        # 3. Parse Hypotheses
        suggestions = []
        pred_lookup = {p.name: p for p in predicates}

        for item in response.get("hypotheses", []):
            try:
                # Reuse the parsing logic we wrote in Translator
                # We mock a wrapper dict to match translator's expected input
                temp_json = {"rules": [item["rule_json"]]}
                
                # We need a method in translator to parse raw dicts, 
                # but for now, let's manually parse or refactor. 
                # To keep it DRY (Don't Repeat Yourself), let's assume we copy-pasted parsing logic 
                # or better, let's execute the parsing here simply.
                
                rule_obj = self._parse_single_rule(item["rule_json"], pred_lookup)
                
                suggestions.append({
                    "description": item["description"],
                    "rule": rule_obj
                })
            except Exception as e:
                print(f"Skipping invalid hypothesis: {e}")

        return suggestions

    def _parse_single_rule(self, rule_dict, pred_lookup):
        # Mini-parser (Same logic as Translator)
        # Head
        head_data = rule_dict["head"]
        head_pred = pred_lookup[head_data["predicate"]]
        head_terms = self.translator._get_terms(head_data["terms"])
        head_atom = head_pred(*head_terms)

        # Body
        body_atoms = []
        for atom_data in rule_dict["body"]:
            body_pred = pred_lookup[atom_data["predicate"]]
            body_terms = self.translator._get_terms(atom_data["terms"])
            body_atoms.append(body_pred(*body_terms))

        # Compose
        body_expr = body_atoms[0]
        for i in range(1, len(body_atoms)):
            body_expr = body_expr & body_atoms[i]

        return Rule(head=head_atom, body=body_expr)