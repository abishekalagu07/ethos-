import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
api_key = os.getenv("HUGGINGFACE_API_KEY")
if not api_key:
    # Use a public token for testing if env is missing? No, rely on user env.
    pass

model = "facebook/bart-large-mnli"
labels = ["MEDICAL", "EMERGENCY", "ESSENTIAL", "GENERAL"]
text = "My EpiPen is broken"

print(f"Testing Zero-Shot with: {model}")

try:
    client = InferenceClient(token=api_key)
    # The client has a dedicated method for this
    response = client.zero_shot_classification(text, labels, model=model)
    print(f"[SUCCESS] Response: {response}")
    # Response format: {'sequence': '...', 'labels': ['MEDICAL', ...], 'scores': [0.9, ...]}
    top_label = response['labels'][0]
    print(f"[VERDICT] Best Label: {top_label}")
except Exception as e:
    print(f"[FAILED] Error: {e}")
