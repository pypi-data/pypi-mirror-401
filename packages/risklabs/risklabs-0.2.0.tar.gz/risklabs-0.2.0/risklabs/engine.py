import random
from typing import Dict, List, Any
import pandas as pd
import numpy as np
from datetime import date, timedelta

from risklabs.models import Strategy, Scenario, SimulationRun, RobustnessResult, SimulationStatus, Position
from risklabs.analysis_models import RegimeProfile, FragilityMatrix, SensitivityProfile, DecisionScorecard
from risklabs.data import data_service

class RegimeDetectionEngine:
    def detect_regimes(self, returns: pd.Series) -> RegimeProfile:
        if returns.empty:
            return RegimeProfile()
        
        # Rolling annualized vol (21-day)
        rolling_vol = returns.rolling(window=21).std() * (252**0.5)
        
        # Trend (Price vs 200-day SMA)
        price_proxy = (1 + returns).cumprod()
        sma_200 = price_proxy.rolling(window=200).mean()
        # Handle case where sma_200 might be mostly NaN if history is short
        if sma_200.isna().all():
             trend = pd.Series(1, index=returns.index) # Assume Bull if no history
        else:
             trend = (price_proxy > sma_200).astype(int).replace(0, -1)
        
        # Vol Regime: 1 if Vol > Median, -1 if Vol < Median
        median_vol = rolling_vol.median()
        if pd.isna(median_vol): median_vol = 0.0
        vol_regime = (rolling_vol > median_vol).astype(int).replace(0, -1)
        
        # Masks
        bull_mask = trend == 1
        bear_mask = trend == -1
        high_vol_mask = vol_regime == 1
        low_vol_mask = vol_regime == -1

        def get_sharpe(mask):
            return self._calculate_sharpe(returns[mask]) if mask.any() else 0.0

        sharpe_bull = get_sharpe(bull_mask)
        sharpe_bear = get_sharpe(bear_mask)
        
        dep_score = sharpe_bull - sharpe_bear

        return RegimeProfile(
            regime_name="Mixed", # TODO: Determine dominant regime
            sharpe_bull=float(sharpe_bull),
            sharpe_bear=float(sharpe_bear),
            sharpe_high_vol=float(get_sharpe(high_vol_mask)),
            sharpe_low_vol=float(get_sharpe(low_vol_mask)),
            regime_dependence_score=float(dep_score)
        )
    
    def _calculate_sharpe(self, series: pd.Series) -> float:
        if series.std() == 0:
            return 0.0
        return (series.mean() * 252) / (series.std() * (252**0.5))

class FragilityAnalyzer:
    def analyze(self, engine: 'SimulationEngine', data: pd.DataFrame, strategy: Strategy, n_sims: int = 20) -> FragilityMatrix:
        base_ret = engine._apply_strategy(data, strategy)
        # Get base metrics manually or assume engine passed them? 
        # We'll just recalc to be safe or use engine method
        
        perturbed_sharpes = []
        simulation_data = [] # To store heatmap data
        
        original_weights = {p.ticker: p.weight for p in strategy.allocation}
        tickers = list(original_weights.keys())
        
        for i in range(n_sims):
            new_weights = {}
            for t in tickers:
                noise = random.uniform(0.9, 1.1)
                w = original_weights[t] * noise
                new_weights[t] = w
            
            # Normalize
            current_sum = sum(new_weights.values())
            if current_sum != 0:
                for t in new_weights:
                    new_weights[t] /= current_sum
            
            temp_strat = Strategy(
                name=f"temp_{i}", 
                allocation=[Position(ticker=t, weight=w) for t, w in new_weights.items()]
            )
            
            ret = engine._apply_strategy(data, temp_strat)
            metrics = engine._calculate_metrics(ret)
            sharpe = metrics.get("sharpe_ratio", 0.0)
            perturbed_sharpes.append(sharpe)
            
            # Store data for heatmap (sim_id, weight_deviation_norm, result)
            # For simplicity, just storing result
            simulation_data.append({"sim": i, "sharpe": sharpe})
            
        sharpe_std = float(np.std(perturbed_sharpes)) if perturbed_sharpes else 0.0
        min_sharpe = float(np.min(perturbed_sharpes)) if perturbed_sharpes else 0.0
        
        # Fragility Score logic
        fragility = min((sharpe_std / 0.2) * 100, 100)
        
        return FragilityMatrix(
            sharpe_variance=sharpe_std,
            min_perturbed_sharpe=min_sharpe,
            fragility_score=float(fragility),
            simulation_data=simulation_data
        )

class SensitivityAnalyzer:
    def analyze(self, engine: 'SimulationEngine', data: pd.DataFrame, strategy: Strategy, param_name: str = "vol_mult", start: float = 1.0, end: float = 3.0, steps: int = 5) -> SensitivityProfile:
        step_vals = []
        sharpes = []
        
        if steps > 1:
            step_size = (end - start) / (steps - 1)
            rng = [start + i*step_size for i in range(steps)]
        else:
            rng = [start]
            
        base_scenario = Scenario(name="Sensitivity Temp", scenario_type="regime_stress", parameters={"shock": "volatility"})
        
        for val in rng:
            if param_name == "vol_mult":
                base_scenario.parameters["vol_mult"] = val
                base_scenario.parameters["shock"] = "volatility"
            elif param_name == "corr_factor":
                base_scenario.parameters["corr_factor"] = val
                base_scenario.parameters["shock"] = "correlation"
                
            stressed_data = engine._apply_scenario_stress(data, base_scenario)
            ret = engine._apply_strategy(stressed_data, strategy)
            metrics = engine._calculate_metrics(ret)
            
            step_vals.append(float(val))
            sharpes.append(metrics.get("sharpe_ratio", 0.0))
            
        delta_sharpe = sharpes[0] - sharpes[-1]
        delta_param = rng[-1] - rng[0]
        score = delta_sharpe / delta_param if delta_param != 0 else 0.0
        
        return SensitivityProfile(
            parameter_name=param_name,
            steps=step_vals,
            sharpes=sharpes,
            sensitivity_score=float(score)
        )

class DecisionEngine:
    def evaluate(self, metrics: Dict[str, float], regime_profile: RegimeProfile, fragility: FragilityMatrix, sensitivity: SensitivityProfile, tail_ratio: float) -> DecisionScorecard:
        # 1. Confidence Score
        # Start at 100
        # Penalize for Fragility
        confidence = 100.0
        confidence -= fragility.fragility_score * 0.5  # If fragility is 100 (super fragile), deduct 50 pts
        
        # Penalize for Tail Risk
        if tail_ratio > 1.2:
            confidence -= (tail_ratio - 1.2) * 20 # If ratio is 1.5, deduct (0.3*20)=6 pts
        
        # Penalize for Regime Dependence
        if abs(regime_profile.regime_dependence_score) > 1.0:
             confidence -= 10.0
             
        # Clamp
        confidence = max(0.0, min(100.0, confidence))
        
        # 2. Assumption Sensitvity Rank
        ranks = []
        if sensitivity.sensitivity_score > 0.5:
            ranks.append(f"High sensitivity to {sensitivity.parameter_name}")
            
        # 3. Freeze Triggers
        triggers = []
        if fragility.fragility_score > 80:
            triggers.append("FRAGMENTATION_RISK_CRITICAL")
        if tail_ratio > 2.0:
            triggers.append("TAIL_RISK_UNACCEPTABLE")
        if metrics.get("max_drawdown", 0.0) < -0.4:
            triggers.append("DRAWDOWN_LIMIT_EXCEEDED")
            
        # 4. Recommendation
        rec = "APPROVE"
        if confidence < 70 or triggers:
            rec = "REVIEW"
        if confidence < 40:
            rec = "REJECT"
            
        return DecisionScorecard(
            confidence_rating=confidence,
            tail_amplification_ratio=tail_ratio,
            assumption_sensitivity_rank=ranks,
            freeze_triggers=triggers,
            recommendation=rec
        )

class SimulationEngine:
    def __init__(self) -> None:
        self.regime_engine = RegimeDetectionEngine()
        self.fragility_analyzer = FragilityAnalyzer()
        self.sensitivity_analyzer = SensitivityAnalyzer()
        self.decision_engine = DecisionEngine()

    def run_simulation(self, run: SimulationRun, strategy: Strategy, scenario: Scenario) -> SimulationRun:
        """
        Main entry point for running a simulation.
        """
        print(f"Starting simulation {run.id} for strategy {strategy.name} in scenario {scenario.name}")
        
        # 1. Fetch Data (Real)
        # Extract tickers from strategy
        tickers = [pos.ticker for pos in strategy.allocation]
        start = scenario.start_date or (date.today() - timedelta(days=365*5))
        end = scenario.end_date or date.today()
        
        data = data_service.fetch_data(tickers, start, end)
        
        if data.empty:
            print("No data found for simulation.")
            run.status = SimulationStatus.FAILED
            return run
        
        # 2. Apply Stress/Scenario Logic (Data Level)
        stressed_data = self._apply_scenario_stress(data, scenario)

        # 3. Apply Strategy
        metrics_returns = self._apply_strategy(stressed_data, strategy)
        
        # 4. Calculate Basic Metrics
        metrics = self._calculate_metrics(metrics_returns)
        
        # 5. Update Run Result
        run.robustness_score = metrics.get("robustness_score", 0.0)
        run.max_drawdown = metrics.get("max_drawdown", 0.0)
        run.sharpe_ratio = metrics.get("sharpe_ratio", 0.0)
        run.status = SimulationStatus.COMPLETED
        
        print(f"Simulation Metrics: {metrics}")
        
        return run

    def calculate_tail_metrics(self, strategy_returns: pd.Series, benchmark_returns: pd.Series) -> Dict[str, float]:
        """
        Compare tail risk of strategy vs benchmark.
        Tail Amplification = CVaR95(Strategy) / CVaR95(Benchmark)
        """
        def cvar_95(returns):
            if returns.empty: return 0.0
            var_95 = returns.quantile(0.05)
            # return average of returns <= var_95
            tail = returns[returns <= var_95]
            if tail.empty: return 0.0
            return tail.mean()

        strat_cvar = cvar_95(strategy_returns)
        bench_cvar = cvar_95(benchmark_returns)
        
        # Lower CVaR (more negative) is worse.
        # Ratio: If Strat -3%, Bench -2%, Ratio = 1.5 (50% worse tables)
        
        if bench_cvar == 0:
            return {"tail_amplification_ratio": 1.0}
            
        ratio = abs(strat_cvar) / abs(bench_cvar)
        return {"tail_amplification_ratio": ratio}

    def _calculate_sharpe(self, series: pd.Series) -> float:
        if series.std() == 0:
            return 0.0
        return (series.mean() * 252) / (series.std() * (252**0.5))

    def _apply_scenario_stress(self, data: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
        """
        Apply scenario transformation to asset returns.
        """
        # Copy to avoid mutating original cache if we had one
        df = data.copy()
        params = scenario.parameters or {}
        
        if scenario.scenario_type == "regime_stress":
            
            # 1. Simple Crash (Legacy support)
            if "Crash" in scenario.name or params.get("shock") == "crash":
                 # Daily drag: -0.1% daily is ~-22% annualized 
                 return df - 0.001 

            # 2. Volatility Spike
            # Param: "vol_mult" (e.g. 1.5x)
            if params.get("shock") == "volatility":
                mult = float(params.get("vol_mult", 1.5))
                return df * mult
                
            # 3. Correlation Breakdown
            # Logic: Collapse all assets towards the cross-sectional mean (Market Mode)
            # Param: "corr_factor" (0.0 to 1.0). 1.0 = Perfect sequence.
            if params.get("shock") == "correlation":
                factor = float(params.get("corr_factor", 0.8))
                
                # Calculate equal-weighted market index of the current assets
                market_index = df.mean(axis=1)
                
                # Blend individual asset with market index
                # New = (1-F)*Old + F*Market
                for col in df.columns:
                    df[col] = (1 - factor) * df[col] + factor * market_index
                
                return df
                
        return df

    def _calculate_metrics(self, returns: pd.Series) -> Dict[str, float]:
        """
        Calculate key robustness metrics.
        """
        if returns.empty:
             return {}
             
        total_return = (1 + returns).prod() - 1
        vol = returns.std() * (252 ** 0.5)
        sharpe = (returns.mean() * 252) / (returns.std() * (252 ** 0.5)) if vol != 0 else 0.0
        
        # Max Drawdown
        cum_returns = (1 + returns).cumprod()
        peak = cum_returns.cummax()
        drawdown = (cum_returns - peak) / peak
        max_dd = drawdown.min() if not drawdown.empty else 0.0
        
        # Robustness Score (0-100)
        # Higher Sharpe & Lower DD = Higher Score
        # Normalize Sharpe (0 to 3) -> 0 to 60
        # Normalize DD (0 to -0.5) -> 40 to 0
        score_sharpe = min(max(sharpe * 20, 0), 60)
        score_dd = min(max((1 + max_dd) * 40, 0), 40)
        score = score_sharpe + score_dd
        
        return {
            "robustness_score": score,
            "max_drawdown": max_dd,
            "sharpe_ratio": sharpe,
            "total_return": total_return
        }

    def _apply_strategy(self, data: pd.DataFrame, strategy: Strategy) -> pd.Series:
        """
        Calculate portfolio returns based on strategy.
        """
        weights = {pos.ticker: pos.weight for pos in strategy.allocation}
        
        # Align data and weights
        portfolio_returns = pd.Series(0.0, index=data.index)
        
        for ticker, weight in weights.items():
            if ticker in data.columns:
                portfolio_returns += data[ticker] * weight
            else:
                pass
                
        return portfolio_returns

engine = SimulationEngine()

