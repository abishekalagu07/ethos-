import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
api_key = os.getenv("HUGGINGFACE_API_KEY")

MODELS_TO_TEST = [
    "google/flan-t5-large",
    "gpt2",
    "bigscience/bloom-560m",
    "facebook/bart-large-mnli" 
]

text = "My EpiPen is broken"
prompt = f"Classify this package into MEDICAL, EMERGENCY, ESSENTIAL, or GENERAL: '{text}'"

print(f"Testing with Key: {api_key[:5]}...")

for model in MODELS_TO_TEST:
    print(f"\n--- Testing Model: {model} ---")
    try:
        client = InferenceClient(model=model, token=api_key)
        # Try text_generation
        response = client.text_generation(prompt, max_new_tokens=10)
        print(f"[SUCCESS] Response: {response.strip()}")
        print(f"[VERDICT] Model '{model}' IS COMPATIBLE.")
        # If successful, we recommend this
        break 
    except Exception as e:
        print(f"[FAILED] Error: {e}")
