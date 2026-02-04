import sys
from src.pipeline import EthosPipeline

def main():
    print("------------------------------------------------")
    print("  ETHOS-DELIVER: Ethical Priority System (CLI)  ")
    print("------------------------------------------------")
    
    pipeline = EthosPipeline()
    
    if len(sys.argv) > 1:
        # CLI Argument Mode
        desc = " ".join(sys.argv[1:])
        run_pipeline(pipeline, desc)
    else:
        # Interactive Mode
        while True:
            desc = input("\nEnter Package Description (or 'q' to quit): ")
            if desc.lower() == 'q':
                break
            run_pipeline(pipeline, desc)

def run_pipeline(pipeline, desc):
    print(f"\nProcessing: '{desc}'...")
    try:
        decision = pipeline.process(desc)
        
        print("\n=== DECISION OUTPUT ===")
        print(f"PRIORITY LEVEL: {decision.priority_level}")
        print(f"APPROVAL REQ:   {decision.requires_approval}")
        print("-" * 30)
        print(decision.explanation)
        print("=======================")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
