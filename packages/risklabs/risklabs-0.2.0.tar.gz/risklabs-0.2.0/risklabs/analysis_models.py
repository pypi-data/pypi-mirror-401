from datetime import date
from typing import List, Dict
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class RobustnessAnalysisRequest(BaseModel):
    strategy_id: UUID

class ScenarioResult(BaseModel):
    scenario_name: str
    robustness_score: float
    max_drawdown: float
    sharpe_ratio: float

class RegimeProfile(BaseModel):
    """
    Performance broken down by market regime.
    """
    regime_name: str = "General"
    sharpe_bull: float = 0.0
    sharpe_bear: float = 0.0
    sharpe_high_vol: float = 0.0
    sharpe_low_vol: float = 0.0
    
    # "Dependency Score" - How much better is it in Bull vs Bear? 
    # (High + = Good in Bull, Bad in Bear. Near 0 = All Weather)
    regime_dependence_score: float = 0.0

class FragilityMatrix(BaseModel):
    """
    Metrics derived from Monte Carlo perturbation of parameters.
    """
    sharpe_variance: float = 0.0
    min_perturbed_sharpe: float = 0.0
    fragility_score: float = 0.0 # 0-100, higher is more fragile
    # Optional: could store raw simulation results here for heatmaps if needed
    simulation_data: List[Dict[str, float]] = Field(default_factory=list)

class SensitivityProfile(BaseModel):
    """
    Results from sweeping a specific stress parameter (e.g. Correlation or Volatility).
    """
    parameter_name: str # e.g. "Volatility Multiplier"
    steps: List[float] # e.g. [1.0, 1.2, 1.4, ...]
    sharpes: List[float] # Resulting Sharpe for each step
    sensitivity_score: float = 0.0 # Slope or impact metric

class DecisionScorecard(BaseModel):
    """
    Final decision support metrics.
    """
    confidence_rating: float = 0.0 # 0-100
    tail_amplification_ratio: float = 1.0 # >1.0 means worse tails than benchmark
    assumption_sensitivity_rank: List[str] = Field(default_factory=list) # Top assumptions impacting result
    freeze_triggers: List[str] = Field(default_factory=list) # Conditions to halt trading
    recommendation: str = "REVIEW" # APPROVE, REVIEW, REJECT

class RobustnessMatrix(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    strategy_id: UUID
    aggregate_score: float
    scenario_results: List[ScenarioResult]
    
    # New Advanced Metrics
    regime_profile: RegimeProfile = Field(default_factory=RegimeProfile)
    fragility_matrix: FragilityMatrix = Field(default_factory=FragilityMatrix)
    sensitivity_profile: SensitivityProfile = Field(default_factory=lambda: SensitivityProfile(parameter_name="None", steps=[], sharpes=[]))
    decision_scorecard: DecisionScorecard = Field(default_factory=DecisionScorecard)
    
    created_at: date = Field(default_factory=date.today)
