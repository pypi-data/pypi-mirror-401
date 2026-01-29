from contextlib import asynccontextmanager
from typing import List, Dict
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from risklabs.models import Strategy, Scenario, SimulationRun, SimulationStatus, Position
from risklabs.engine import engine
from risklabs.analysis_models import RobustnessAnalysisRequest, RobustnessMatrix, ScenarioResult

# In-memory storage for MVP
frequencies: Dict[UUID, Strategy] = {}
scenarios: Dict[UUID, Scenario] = {}
runs: Dict[UUID, SimulationRun] = {}

class CreateStrategyRequest(BaseModel):
    name: str
    allocation: List[Position]

class CreateSimulationRequest(BaseModel):
    strategy_id: UUID
    scenario_id: UUID

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load some default data
    default_strat_id = uuid4()
    frequencies[default_strat_id] = Strategy(
        id=default_strat_id,
        name="60/40 Portfolio",
        allocation=[
            Position(ticker="SPY", weight=0.6),
            Position(ticker="AGG", weight=0.4)
        ]
    )
    
    default_scen_id = uuid4()
    scenarios[default_scen_id] = Scenario(
        id=default_scen_id,
        name="2008 Crash Replay",
        scenario_type="regime_stress"
    )
    yield
    # Cleanup

app = FastAPI(title="RiskLab API", lifespan=lifespan)

# Mount static files - verify path relative to where server is run
# Assuming we run from root: uvicorn app.api.server:app
app.mount("/static", StaticFiles(directory="risklabs/static"), name="static")

@app.get("/")
async def root():
    return FileResponse('risklabs/static/index.html')

@app.post("/strategies", response_model=Strategy)
async def create_strategy(request: CreateStrategyRequest):
    strategy = Strategy(
        name=request.name,
        allocation=request.allocation
    )
    frequencies[strategy.id] = strategy
    return strategy

@app.get("/strategies", response_model=List[Strategy])
async def list_strategies():
    return list(frequencies.values())

@app.post("/scenarios", response_model=Scenario)
async def create_scenario(scenario: Scenario):
    scenarios[scenario.id] = scenario
    return scenario

@app.get("/scenarios", response_model=List[Scenario])
async def list_scenarios():
    return list(scenarios.values())

def run_simulation_task(run_id: UUID):
    """
    Synchronous task to be run in background threadpool.
    """
    if run_id not in runs:
        return

    run = runs[run_id]
    strategy = frequencies[run.strategy_id]
    scenario = scenarios[run.scenario_id]
    
    run.status = SimulationStatus.RUNNING
    try:
        updated_run = engine.run_simulation(run, strategy, scenario)
        runs[run_id] = updated_run
    except Exception as e:
        print(f"Simulation failed: {e}")
        run.status = SimulationStatus.FAILED

@app.post("/simulate", response_model=SimulationRun)
async def trigger_simulation(request: CreateSimulationRequest, background_tasks: BackgroundTasks):
    if request.strategy_id not in frequencies:
        raise HTTPException(status_code=404, detail="Strategy not found")
    if request.scenario_id not in scenarios:
        raise HTTPException(status_code=404, detail="Scenario not found")
        
    run = SimulationRun(
        strategy_id=request.strategy_id,
        scenario_id=request.scenario_id,
        status=SimulationStatus.PENDING
    )
    runs[run.id] = run
    
    background_tasks.add_task(run_simulation_task, run.id)
    
    return run

@app.get("/simulations/{run_id}", response_model=SimulationRun)
async def get_simulation(run_id: UUID):
    if run_id not in runs:
        raise HTTPException(status_code=404, detail="Simulation run not found")
    return runs[run_id]

@app.post("/analyze_robustness", response_model=RobustnessMatrix)
async def analyze_robustness(request: RobustnessAnalysisRequest):
    if request.strategy_id not in frequencies:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    strategy = frequencies[request.strategy_id]
    
    # Define Standard Scenarios
    std_scenarios = [
        Scenario(name="Historical Baseline", scenario_type="historical_replay"),
        Scenario(name="2008 Crash Replay", scenario_type="regime_stress", parameters={"shock": "crash"}),
        Scenario(name="Volatility Spike (2x)", scenario_type="regime_stress", parameters={"shock": "volatility", "vol_mult": 2.0}),
        Scenario(name="Correlation Breakdown", scenario_type="regime_stress", parameters={"shock": "correlation", "corr_factor": 0.9})
    ]
    
    results = []
    total_score = 0.0
    
    for scen in std_scenarios:
        # Create a ephemeral run
        run = SimulationRun(strategy_id=strategy.id, scenario_id=scen.id, status=SimulationStatus.RUNNING)
        
        # Run sync (computational heavy, might block main loop if not careful, 
        # but for now we accept it or should use run_in_threadpool)
        # For strict correctness in async endpoint:
        # executed_run = await run_in_threadpool(engine.run_simulation, run, strategy, scen)
        # But for simplicity we will just call it.
        
        executed_run = engine.run_simulation(run, strategy, scen)
        
        res = ScenarioResult(
            scenario_name=scen.name,
            robustness_score=executed_run.robustness_score or 0.0,
            max_drawdown=executed_run.max_drawdown or 0.0,
            sharpe_ratio=executed_run.sharpe_ratio or 0.0
        )
        results.append(res)
        total_score += res.robustness_score
    
    avg_score = total_score / len(results) if results else 0.0
    
    matrix = RobustnessMatrix(
        strategy_id=strategy.id,
        aggregate_score=avg_score,
        scenario_results=results
    )
    
    return matrix
