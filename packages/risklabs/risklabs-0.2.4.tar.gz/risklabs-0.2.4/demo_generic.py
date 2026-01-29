import sys
import os
import pandas as pd
from datetime import date

# Add project root to path
sys.path.append(os.path.abspath("/Users/pedroparis/Antigravity Projects/Allostan Labs/risklabs"))

# Import Generic Strategy
from generic_model import run_generic_strategy, UNIVERSE_TICKERS

from risklabs.client import create_strategy, analyze
from risklabs.reporting import RiskReport

def run_demo():
    print("==========================================")
    print("Running Generic Trend-Robust Strategy...")
    print("==========================================")
    
    weights, prices = run_generic_strategy()
    
    print("\n==========================================")
    print("Constructing RiskLab Strategy...")
    print("==========================================")
    
    # Take the latest weights
    latest_w = weights.iloc[-1]
    
    allocations = []
    sorted_weights = latest_w.sort_values(ascending=False)
    
    for ticker, weight in sorted_weights.items():
        if weight > 0.001: 
            allocations.append({"ticker": ticker, "weight": float(weight)})
            
    if not allocations:
        print("Error: No allocations generated.")
        return

    # Create Strategy Object
    strategy = create_strategy("Trend-Robust Allocation", allocations)
    print(f"Strategy Created with {len(allocations)} positions.")
    for p in allocations:
        print(f"  - {p['ticker']}: {p['weight']:.2%}")
    
    print("\n==========================================")
    print("Running RiskLab Robustness Analysis...")
    print("==========================================")
    
    try:
        report = analyze(strategy)
        print("Analysis Complete.")
        
        output_file = "/Users/pedroparis/Antigravity Projects/Allostan Labs/risklabs/generic_report.html"
        report.to_file(output_file)
        print(f"\nSUCCESS! Report generated at: {output_file}")
        
    except Exception as e:
        print(f"ERROR during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_demo()
