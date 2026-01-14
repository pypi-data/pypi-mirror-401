from typing import List, Dict, Any
from .llm_interface import LLMInterface
from .prompts import TRANSLATOR_SYSTEM_PROMPT, EXPLAINER_SYSTEM_PROMPT

# Import Core definitions to construct objects
from ..core.logic import Rule, Predicate, Atom
from ..core.symbols import Variable, Term


class LogicTranslator:
    """
    Translates Natural Language to NSAI Logic Rules and vice-versa.
    """
    def __init__(self, llm_client: LLMInterface):
        self.llm = llm_client

    def text_to_rules(self, text: str, predicates: List[Predicate]) -> List[Rule]:
        """
        Converts English text into executable Rule objects.
        
        Args:
            text: "Zorgs imply antennas"
            predicates: List of available Predicate objects [IsZorg, HasAntenna]
        """
        # 1. Prepare Context (List available predicates for the LLM)
        pred_info = ", ".join([f"{p.name}(arity={p.arity})" for p in predicates])
        user_prompt = f"Available Predicates: [{pred_info}]\n\nInput Text: \"{text}\""

        # 2. Get JSON from LLM
        response_json = self.llm.generate_json(
            system_prompt=TRANSLATOR_SYSTEM_PROMPT,
            user_prompt=user_prompt
        )

        # 3. Parse JSON into Python Objects
        # We need a lookup dict to find Predicate objects by name
        pred_lookup = {p.name: p for p in predicates}
        generated_rules = []

        try:
            for rule_dict in response_json.get("rules", []):
                # Construct Head
                head_data = rule_dict["head"]
                head_pred = self._get_pred(head_data["predicate"], pred_lookup)
                head_terms = self._get_terms(head_data["terms"])
                head_atom = head_pred(*head_terms)

                # Construct Body
                body_atoms = []
                for atom_data in rule_dict["body"]:
                    body_pred = self._get_pred(atom_data["predicate"], pred_lookup)
                    body_terms = self._get_terms(atom_data["terms"])
                    body_atoms.append(body_pred(*body_terms))

                # Combine Body (Assuming AND for list items)
                if not body_atoms:
                    raise ValueError("Rule body cannot be empty")
                
                # Create Logic Expression for body (Atom1 & Atom2 & ...)
                body_expr = body_atoms[0]
                for i in range(1, len(body_atoms)):
                    body_expr = body_expr & body_atoms[i]

                # Create Rule
                # Syntax: Head << Body (or Rule(head, body))
                generated_rules.append(Rule(head=head_atom, body=body_expr))

        except Exception as e:
            raise ValueError(f"Failed to parse LLM output: {e}. \nResponse: {response_json}")

        return generated_rules

    def explain_rule(self, rule: Rule) -> str:
        """
        Converts a Rule object back to English.
        """
        rule_str = str(rule) # Uses the __repr__ we defined in core
        return self.llm.generate(
            system_prompt=EXPLAINER_SYSTEM_PROMPT,
            user_prompt=f"Rule: {rule_str}"
        )

    # --- Helpers ---
    def _get_pred(self, name: str, lookup: Dict[str, Predicate]) -> Predicate:
        if name not in lookup:
            raise ValueError(f"LLM hallucinated a predicate '{name}' which does not exist.")
        return lookup[name]

    def _get_terms(self, term_names: List[str]) -> List[Term]:
        # Simple factory: If string starts with lowercase, it's a Variable
        return [Variable(t) for t in term_names]