import sys
import os

# Ensure we can import the app package from root
sys.path.append(os.getcwd())

from app.client import create_strategy, analyze

def main():
    print("--- RiskLab Local Analysis ---")
    
    # 1. Define Strategy
    print("1. Defining Strategy (60/40)...")
    portfolio = create_strategy("My Local 60/40", [
        {"ticker": "SPY", "weight": 0.6},
        {"ticker": "AGG", "weight": 0.4}
    ])
    
    # 2. Run Analysis
    print("2. Running Analysis (fetching data & stressing)...")
    # This runs synchronously
    report = analyze(portfolio)
    
    # 3. Save Report
    output_file = "my_portfolio_report.html"
    print(f"3. Saving report to {output_file}...")
    report.to_file(output_file)
    
    print("Done! Open the HTML file to view results.")

if __name__ == "__main__":
    main()
