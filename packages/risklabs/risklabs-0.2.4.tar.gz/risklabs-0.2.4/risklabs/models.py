from datetime import date
from enum import Enum
from typing import Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict


class StrategyType(str, Enum):
    STATIC_WEIGHTS = "static_weights"
    DYNAMIC_RULE = "dynamic_rule"


class AssetClass(str, Enum):
    EQUITY = "equity"
    OPTION = "option"
    CASH = "cash"


class Position(BaseModel):
    ticker: str
    weight: float = Field(..., ge=-1.0, le=1.0, description="Portfolio weight, negative for shorts")
    asset_class: AssetClass = AssetClass.EQUITY


class Strategy(BaseModel):
    """
    Defines the capital allocation strategy to be tested.
    For MVP, we support static weights.
    """
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: Optional[str] = None
    strategy_type: StrategyType = StrategyType.STATIC_WEIGHTS
    # For static weights, this is the target allocation.
    # For dynamic rules, this might be initial config.
    allocation: List[Position]

    model_config = ConfigDict(from_attributes=True)


class ScenarioType(str, Enum):
    USER_DEFINED = "user_defined"
    HISTORICAL_REPLAY = "historical_replay"
    MONTE_CARLO = "monte_carlo"
    REGIME_STRESS = "regime_stress"


class Scenario(BaseModel):
    """
    Defines the market conditions or 'flight path' for the simulation.
    """
    id: UUID = Field(default_factory=uuid4)
    name: str
    scenario_type: ScenarioType
    # Parameters for the scenario (e.g., {"shock_magnitude": 0.2, "regime": "inflationary"})
    parameters: Dict[str, Union[float, str]] = Field(default_factory=dict)
    
    # Date range for historical replay
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class SimulationStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class SimulationRun(BaseModel):
    """
    Configuration for a specific simulation execution.
    Links a strategy to a scenario.
    """
    id: UUID = Field(default_factory=uuid4)
    strategy_id: UUID
    scenario_id: UUID
    status: SimulationStatus = SimulationStatus.PENDING
    
    # Results will be populated after run
    robustness_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    max_drawdown: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    
    created_at: date = Field(default_factory=date.today)


class RobustnessResult(BaseModel):
    """
    Detailed artifacts from a simulation run.
    """
    run_id: UUID
    metrics: Dict[str, float]  # e.g. {"calmar": 1.2, "sortino": 1.5}
    # Timeseries data would typically be stored separately or as a URL to a parquet file
    # For MVP API response, we might include a small snippet or summary
    regime_breakdown: Dict[str, float] # e.g. {"bull": 10.0, "bear": -5.0} Score per regime
