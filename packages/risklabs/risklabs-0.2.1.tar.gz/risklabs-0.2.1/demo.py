import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Path: {sys.path}")

# Add project root to path

# Add project root to path
sys.path.append(os.path.abspath("/Users/pedroparis/Antigravity Projects/risklab"))

from risklabs.client import create_strategy, analyze
from risklabs.reporting import RiskReport

def run_demo():
    print("Creating Strategy...")
    strategy = create_strategy("Test Strategy", [
        {"ticker": "SPY", "weight": 0.6},
        {"ticker": "TLT", "weight": 0.4}
    ])
    
    print("Running Analysis... (This triggers engine logic)")
    try:
        report = analyze(strategy)
        print("Analysis Complete.")
        
        output_file = "/Users/pedroparis/Antigravity Projects/risklab/demo_report.html"
        report.to_file(output_file)
        print(f"Report generated at {output_file}")
        
    except Exception as e:
        print(f"ERROR during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_demo()
