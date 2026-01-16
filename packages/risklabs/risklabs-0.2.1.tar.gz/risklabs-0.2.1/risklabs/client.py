import asyncio
from typing import List, Dict, Union
from uuid import uuid4

from datetime import date, timedelta
from risklabs.models import Strategy, StrategyType, Position, AssetClass, Scenario, SimulationRun, SimulationStatus
from risklabs.engine import engine
from risklabs.reporting import RiskReport
from risklabs.analysis_models import RobustnessMatrix, ScenarioResult, RegimeProfile, FragilityMatrix, SensitivityProfile, DecisionScorecard
from risklabs.data import data_service

def create_strategy(name: str, allocations: List[Dict[str, Union[str, float]]]) -> Strategy:
    """
    Helper to create a Strategy object from simple dict list.
    allocations = [{"ticker": "SPY", "weight": 0.6}, ...]
    """
    positions = []
    for alloc in allocations:
        pos = Position(
            ticker=alloc["ticker"],
            weight=alloc["weight"],
            asset_class=AssetClass.EQUITY # Default for now
        )
        positions.append(pos)
        
    return Strategy(
        id=uuid4(),
        name=name,
        strategy_type=StrategyType.STATIC_WEIGHTS,
        allocation=positions
    )

def analyze(strategy: Strategy) -> RiskReport:
    """
    Runs the full robustness analysis suite on the given strategy.
    Returns a RiskReport object.
    """
    # 1. Fetch Data for Strategy (Standard Baseline)
    tickers = [p.ticker for p in strategy.allocation]
    start = date.today() - timedelta(days=365*5)
    end = date.today()
    data = data_service.fetch_data(tickers, start, end)
    
    # Baseline Returns
    base_returns = engine._apply_strategy(data, strategy)
    
    # 2. Advanced Metrics
    
    # A. Regime Metrics
    regime_profile = engine.regime_engine.detect_regimes(base_returns)
    
    # B. Fragility
    # n_sims=10 for speed in interactive/demo mode
    fragility_matrix = engine.fragility_analyzer.analyze(engine, data, strategy, n_sims=10) 
    
    # C. Tail Amplification
    # We need SPY data for benchmark
    bench_data = data_service.fetch_data(["SPY"], start, end)
    bench_returns = bench_data["SPY"] if not bench_data.empty else base_returns # Fallback
    
    tail_stats = engine.calculate_tail_metrics(base_returns, bench_returns)
    tail_ratio = tail_stats.get("tail_amplification_ratio", 1.0)
    
    # D. Sensitivity Profile
    # Sweep Volatility from 1.0x to 3.0x
    sensitivity_profile = engine.sensitivity_analyzer.analyze(engine, data, strategy, param_name="vol_mult", start=1.0, end=3.0, steps=5)
    
    # E. Decision Scorecard
    # We use the DecisionEngine for this now
    # Need to pass basic metrics too (e.g. max_drawdown) which usually come from a simulation run.
    # Let's calculate base metrics first.
    base_metrics = engine._calculate_metrics(base_returns)
    
    decision_scorecard = engine.decision_engine.evaluate(
        metrics=base_metrics,
        regime_profile=regime_profile,
        fragility=fragility_matrix,
        sensitivity=sensitivity_profile,
        tail_ratio=tail_ratio
    )
    
    # 3. Scenarios (Standard Loop)
    # Define Scenarios
    scenarios = [
        Scenario(name="Historical Baseline", scenario_type="historical_replay"),
        Scenario(name="2008 Crash Replay", scenario_type="regime_stress", parameters={"shock": "crash"}),
        Scenario(name="Volatility Spike (2x)", scenario_type="regime_stress", parameters={"shock": "volatility", "vol_mult": 2.0}),
        Scenario(name="Correlation Breakdown", scenario_type="regime_stress", parameters={"shock": "correlation", "corr_factor": 0.9})
    ]
    
    results = []
    total_score = 0.0
    
    for scen in scenarios:
        run = SimulationRun(strategy_id=strategy.id, scenario_id=scen.id)
        
        # Execute engine method
        executed_run = engine.run_simulation(run, strategy, scen)
        
        # Collect results
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
        scenario_results=results,
        regime_profile=regime_profile,
        fragility_matrix=fragility_matrix,
        sensitivity_profile=sensitivity_profile,
        decision_scorecard=decision_scorecard
    )
    
    return RiskReport(matrix)
