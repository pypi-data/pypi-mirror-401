import os
# Set dummy key if testing with a provider that needs it, or rely on Env
# os.environ["OPENAI_API_KEY"] = "sk-..." 
from dotenv import load_dotenv 
load_dotenv()


from src.nsx.agent.llm_interface import LLMInterface

def test_connection():
    print("--- Phase 5.1: LiteLLM Interface Test ---")
    
    # 1. Initialize Client (Change model to whatever you have access to)
    # Examples: "gpt-3.5-turbo", "ollama/llama2", "claude-3-haiku"
    model_name = "gpt-4o" 
    print(f"Connecting to: {model_name}...")
    
    try:
        agent = LLMInterface(model_name=model_name)
        
        # 2. Test Simple Chat
        response = agent.generate(
            system_prompt="You are a helpful assistant.",
            user_prompt="what is capital of france?"
        )
        print(f"✅ Raw Response: {response}")
        
        # 3. Test JSON Output (Critical for Logic Generation)
        print("Testing JSON Mode...")
        json_resp = agent.generate_json(
            system_prompt="Extract info.",
            user_prompt="My name is Alice and I am 30 years old."
        )
        print(f"✅ JSON Response: {json_resp}")
        print("Test Passed!")
        
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        print("Note: Make sure API Keys are set in environment variables.")

if __name__ == "__main__":
    test_connection()