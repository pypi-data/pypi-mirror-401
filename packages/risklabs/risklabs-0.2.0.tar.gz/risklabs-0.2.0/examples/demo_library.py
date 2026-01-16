from risklabs.client import create_strategy, analyze
import os

def main():
    strategies = [
        create_strategy(
            name="Conservative 60/40",
            allocations=[{"ticker": "SPY", "weight": 0.6}, {"ticker": "AGG", "weight": 0.4}]
        ),
        create_strategy(
            name="Aggressive Growth",
            allocations=[{"ticker": "SPY", "weight": 1.0}]
        )
    ]
    
    print(f"Running analysis for {len(strategies)} strategies...")
    
    for strategy in strategies:
        print(f"\n--- Processing {strategy.name} ---")
        
        # 1. Run the analysis loop (Simulates Scenarios)
        report = analyze(strategy)
        
        # 2. Output the Dashboard
        safe_name = strategy.name.replace(' ', '_').replace('/', '-').lower()
        filename = f"report_{safe_name}.html"
        report.to_file(filename)
        
        if os.path.exists(filename):
            print(f"Dashboard generated: {filename}")

if __name__ == "__main__":
    main()
