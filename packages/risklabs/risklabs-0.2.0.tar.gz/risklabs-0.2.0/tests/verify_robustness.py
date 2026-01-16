import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"

async def main():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=60.0) as client:
        print("1. Creating Strategy...")
        strat_payload = {
            "name": "60/40 Standard",
            "allocation": [
                {"ticker": "SPY", "weight": 0.60, "asset_class": "equity"},
                {"ticker": "AGG", "weight": 0.40, "asset_class": "equity"}
            ]
        }
        resp = await client.post("/strategies", json=strat_payload)
        strat = resp.json()
        print(f"Created Strategy: {strat['id']}")
        
        print("\n2. Triggering Robustness Analysis...")
        # robust analysis payload
        payload = {"strategy_id": strat['id']}
        
        resp = await client.post("/analyze_robustness", json=payload)
        matrix = resp.json()
        
        print(f"Analysis Complete! Aggregate Score: {matrix['aggregate_score']}")
        print("Breakdown:")
        for res in matrix['scenario_results']:
            print(f" - {res['scenario_name']}: Score={res['robustness_score']}, DD={res['max_drawdown']}")
            
        assert matrix['aggregate_score'] > 0
        print("\n✅ Robustness Matrix Verification Successful!")

if __name__ == "__main__":
    asyncio.run(main())
