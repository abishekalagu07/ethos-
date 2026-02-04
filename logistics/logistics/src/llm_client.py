import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from .models import DomainCategory

# Load environment variables
load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.client = None
        if self.api_key:
            # Use a specialized Zero-Shot Classifier
            self.repo_id = "facebook/bart-large-mnli"
            self.client = InferenceClient(token=self.api_key)

    def classify_domain(self, text: str) -> DomainCategory:
        """
        Uses Hugging Face Zero-Shot Classification to categorize text.
        """
        if not self.client:
            print("[WARN] LLM fallback skipped: HUGGINGFACE_API_KEY not found.")
            return None

        # Define the labels exactly as we want them
        labels = ["MEDICAL", "EMERGENCY", "ESSENTIAL", "GENERAL"]

        try:
            # Dedicated method for classification - much more reliable than text generation
            # Returns a list of result objects, usually just one for single text input?
            # Based on test output, it returns a list of ZeroShotClassificationOutputElement objects if simple list?
            # Or the client returns a structured object. Let's handle the object returned by the library.
            response = self.client.zero_shot_classification(text, labels, model=self.repo_id)
            
            # The library returns a list of results if input is list, or single result? 
            # Looking at test output: [ZeroShotClassificationOutputElement(label='MEDICAL', ...), ...]
            # So response is a LIST of elements sorted by score desc.
            if isinstance(response, list) and len(response) > 0:
                top_result = response[0]
                top_label = top_result.label
            else:
                # Handle unexpected format
                top_label = "GENERAL"

            # Map string back to Enum
            top_label = top_label.upper()
            for domain in DomainCategory:
                if domain.value == top_label:
                    print(f"   (LLM Verdict: {domain.value})")
                    return domain
            
            return DomainCategory.GENERAL

        except Exception as e:
            print(f"[ERROR] LLM Classification failed: {e}")
            return None
