import os 
import json 
from typing import Any, Dict, List, Optional, Union

try:  
    import litellm 
    from litellm import completion 
except ImportError: 
    raise ImportError("To use the Agent module, please install litellm: pip install litellm") 


class LLMInterface:
    """
    A unified interface for any LLM powered by LiteLLM. 
    """
    def __init__(self, model_name: str = "openai/gpt-4o-mini", api_key: Optional[str] = None, **kwargs):
        """
        Args: 
            model_name: The name of the LLM model to use. 
            api_key: The API key to use for authentication. 
            **kwargs: Additional arguments to pass to the LLM.
        """
        self.model_name = model_name
        self.api_key = api_key
        self.default_params = kwargs 

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
        """
        Basic Text Generation.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            response = completion(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                **self.default_params
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            raise RuntimeError(f"LLM Generation Failed ({self.model_name}): {str(e)}")
    
    def generate_json(self, system_prompt: str, user_prompt: str, schema: Optional[Dict] = None) -> Dict:
        """
        Generates structured JSON output. Crucial for converting English -> Logic Code.
        Uses 'response_format' where supported (OpenAI) or prompt engineering for others.
        """
        messages = [
            {"role": "system", "content": system_prompt + "\nIMPORTANT: Output MUST be valid JSON."},
            {"role": "user", "content": user_prompt}
        ]

        params = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.1, # Low temp for code/logic
            **self.default_params
        }

        # Enable JSON mode for models that support it
        if "gpt" in self.model_name or "json" in self.model_name:
            params["response_format"] = {"type": "json_object"}

        try:
            response = completion(**params)
            content = response.choices[0].message.content.strip()
            
            # Sanitize: Remove markdown code blocks if LLM adds them ```json ... ```
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            
            return json.loads(content)

        except json.JSONDecodeError:
            raise ValueError(f"LLM did not return valid JSON. Response: {content}")
        except Exception as e:
            raise RuntimeError(f"LLM JSON Generation Failed: {str(e)}")


# Example Usage Helper
def get_client(model: str = "openai/gpt-4o"):
    return LLMInterface(model_name=model)