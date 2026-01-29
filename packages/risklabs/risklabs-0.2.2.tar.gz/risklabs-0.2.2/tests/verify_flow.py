import asyncio
import httpx
from uuid import UUID

BASE_URL = "http://127.0.0.1:8000"

async def main():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        print("1. Checking Root...")
        resp = await client.get("/")
        print(resp.json())
        assert resp.status_code == 200

        print("\n2. Creating Strategy...")
        strat_payload = {
            "name": "60/40 Standard",
            "allocation": [
                {"ticker": "SPY", "weight": 0.60, "asset_class": "equity"},
                {"ticker": "AGG", "weight": 0.40, "asset_class": "equity"}
            ]
        }
        resp = await client.post("/strategies", json=strat_payload)
        strat = resp.json()
        print(f"Created Strategy: {strat['id']} - {strat['name']}")
        strat_id = strat['id']

        print("\n3. Creating Scenario...")
        scen_payload = {
            "name": "Hyper-Inflation Shock",
            "scenario_type": "regime_stress",
            "parameters": {"inflation_shock": 0.10} # 10% jump
        }
        resp = await client.post("/scenarios", json=scen_payload)
        scen = resp.json()
        print(f"Created Scenario: {scen['id']} - {scen['name']}")
        scen_id = scen['id']

        print("\n4. Triggering Simulation...")
        sim_payload = {
            "strategy_id": strat_id,
            "scenario_id": scen_id
        }
        resp = await client.post("/simulate", json=sim_payload)
        run = resp.json()
        print(f"Simulation Queued: {run['id']} (Status: {run['status']})")
        run_id = run['id']

        print("\n5. Polling for Results...")
        for _ in range(5):
            await asyncio.sleep(1)
            resp = await client.get(f"/simulations/{run_id}")
            run = resp.json()
            status = run['status']
            print(f"Status: {status}")
            if status in ["completed", "failed"]:
                break
        
        print("\n6. Final Result:")
        print(run)
        assert run['status'] == 'completed'
        print("\n✅ Verification Successful!")

if __name__ == "__main__":
    asyncio.run(main())
