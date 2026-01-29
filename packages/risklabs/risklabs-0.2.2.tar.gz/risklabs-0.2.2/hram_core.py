# ==============================================================
# HRAM-Core v3.2.1 — IBKR Trade Sheet (Momentum + ML + Signal-HRP)
#   • Quarterly, lagged rebalancing
#   • Survivorship-safer dynamic universe (liquidity + history)
#   • XGBoost walk-forward with cached features
#   • Signal-weighted Hierarchical Risk Parity allocator
#   • IBKR manual execution pack:
#       - Cash-only start (default $10k) ✅
#       - Produce target weights + trade sheet + diagnostics
#
# KEY PATCHES
#   1) Robust yfinance download for 1 ticker vs many tickers ✅
#   2) Adj Close fallback to Close ✅
#   3) Safe handling of missing tickers/volumes ✅
#   4) Cash-only holdings mode (no CSV) ✅
# ==============================================================

import random
import warnings
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, cast

import numpy as np
import pandas as pd
import yfinance as yf

# --- tqdm (auto-install if missing) ---
try:
    from tqdm.auto import tqdm
except ImportError:  # pragma: no cover
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
    from tqdm.auto import tqdm  # type: ignore

# --- SciPy for HRP clustering (try import, otherwise install) ---
try:
    from scipy.cluster.hierarchy import linkage, leaves_list
    from scipy.spatial.distance import squareform
except ImportError:  # pragma: no cover
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "scipy"])
    from scipy.cluster.hierarchy import linkage, leaves_list  # type: ignore
    from scipy.spatial.distance import squareform  # type: ignore

# --- XGBoost ---
try:
    from xgboost import XGBRegressor
except ImportError:  # pragma: no cover
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "xgboost"])
    from xgboost import XGBRegressor  # type: ignore

warnings.filterwarnings("ignore")
np.random.seed(42)
random.seed(42)

# ==============================================================
# CONFIG
# ==============================================================

UNIVERSE = [
    "AAPL",
    "MSFT",
    "AMZN",
    "NVDA",
    "GOOGL",
    "META",
    "GOOG",
    "BRK-B",
    "LLY",
    "JPM",
    "XOM",
    "V",
    "WMT",
    "MA",
    "AVGO",
    "TSLA",
    "UNH",
    "PG",
    "JNJ",
    "HD",
    "MRK",
    "COST",
    "ORCL",
    "ABBV",
    "PEP",
    "KO",
    "BAC",
    "ADBE",
    "NFLX",
    "CSCO",
    "TM",
    "TMO",
    "INTU",
    "LIN",
    "AMD",
    "CRM",
    "TXN",
    "NKE",
    "AMAT",
    "QCOM",
]

INDEX_TKR = "SPY"
START, END = "2010-01-01", None

# Portfolio & rebalance cadence
INIT_CASH = 10_000.0
CORE_TOP_K = 20
CORE_REBAL_MONTHS = {3, 6, 9, 12}  # quarterly

# Deployment rules for manual IBKR
TARGET_CORE_FRACT = 0.90  # invest 90% of NAV, keep 10% cash buffer
MIN_TRADE_USD = 200.0  # ignore tiny trades
ROUND_SHARES = True  # shares integer rounding for stocks/ETFs

# Survivorship / liquidity gating
LIQ_LOOKBACK_W = 52
MIN_DOLLAR_VOL = 1e9  # if too strict, reduce (e.g., 1e7–1e8)

# Risk / constraints
CORE_CAP_PER_NAME = 0.10
MAX_SECTOR_WEIGHT = 0.40
TURNOVER_CAP = 0.35

# Transaction costs (rough)
EQUITY_TC_BPS = 0.0002
IMPACT_COEFF = 0.7  # square-root impact coefficient
SLIPPAGE_BPS = 0.0001  # extra slippage placeholder

# HRP signal strength
HRP_SIGNAL_ALPHA = 1.0  # 0=pure HRP; 1=signal-adjusted HRP

# ML blend weights
W_MOM = 0.30
W_RESID = 0.30
W_ML = 0.40

SECTOR_MAP = {
    "AAPL": "Tech",
    "MSFT": "Tech",
    "AMZN": "Consumer",
    "NVDA": "Tech",
    "GOOGL": "Tech",
    "META": "Tech",
    "GOOG": "Tech",
    "BRK-B": "Financials",
    "LLY": "Healthcare",
    "JPM": "Financials",
    "XOM": "Energy",
    "V": "Financials",
    "WMT": "Consumer",
    "MA": "Financials",
    "AVGO": "Tech",
    "TSLA": "Consumer",
    "UNH": "Healthcare",
    "PG": "Consumer",
    "JNJ": "Healthcare",
    "HD": "Consumer",
    "MRK": "Healthcare",
    "COST": "Consumer",
    "ORCL": "Tech",
    "ABBV": "Healthcare",
    "PEP": "Consumer",
    "KO": "Consumer",
    "BAC": "Financials",
    "ADBE": "Tech",
    "NFLX": "Consumer",
    "CSCO": "Tech",
    "TM": "Industrial",
    "TMO": "Healthcare",
    "INTU": "Tech",
    "LIN": "Industrial",
    "AMD": "Tech",
    "CRM": "Tech",
    "TXN": "Tech",
    "NKE": "Consumer",
    "AMAT": "Tech",
    "QCOM": "Tech",
}

# ==============================================================
# DATA (PATCHED: works for 1 ticker or many tickers)
# ==============================================================


def _extract_field(raw: pd.DataFrame, ticker: str, field: str) -> Optional[pd.Series]:
    """
    yfinance returns either:
      - MultiIndex columns when multiple tickers
      - Flat columns when single ticker
    This function handles both.
    """
    if raw.empty:
        return None

    if isinstance(raw.columns, pd.MultiIndex):
        if ticker in raw.columns.get_level_values(0):
            sub = raw[ticker]
            if field in sub.columns:
                return cast(pd.Series, sub[field]).rename(ticker)
        return None

    if field in raw.columns:
        return cast(pd.Series, raw[field]).rename(ticker)

    return None


def download_weekly(
    tickers: List[str], start: str, end: Optional[str]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Robust weekly downloader:
      - Works for 1 ticker or many tickers
      - Uses Adj Close when available, else Close
      - Skips tickers that fail, without crashing
    """
    tickers = [t.upper() for t in tickers]

    raw = yf.download(
        tickers,
        start=start,
        end=end,
        progress=False,
        group_by="ticker",
        auto_adjust=False,
        threads=True,
    )

    px_list: List[pd.Series] = []
    vol_list: List[pd.Series] = []

    for t in tickers:
        s_px = _extract_field(raw, t, "Adj Close")
        if s_px is None:
            s_px = _extract_field(raw, t, "Close")

        s_vol = _extract_field(raw, t, "Volume")

        if s_px is None or s_px.dropna().empty:
            continue

        px_list.append(s_px.astype(float))

        if s_vol is not None and not s_vol.dropna().empty:
            vol_list.append(s_vol.astype(float))

    if not px_list:
        raise ValueError("No price data returned. Check tickers/network/Yahoo limits.")

    px = pd.concat(px_list, axis=1).sort_index()

    if vol_list:
        vol = pd.concat(vol_list, axis=1).sort_index()
    else:
        vol = pd.DataFrame(index=px.index, columns=px.columns, data=np.nan)

    wk_px = px.resample("W-FRI").last().ffill()

    if not vol.empty:
        wk_vol = vol.resample("W-FRI").sum().reindex(wk_px.index).ffill()
        wk_vol = wk_vol.reindex(columns=wk_px.columns)
    else:
        wk_vol = pd.DataFrame(index=wk_px.index, columns=wk_px.columns, data=np.nan)

    return wk_px, wk_vol


def align_on_common_index(
    stk_px: pd.DataFrame, spy_px: pd.Series
) -> Tuple[pd.DataFrame, pd.Series]:
    common = stk_px.index.intersection(spy_px.index)
    stk_px = stk_px.reindex(common).ffill()
    spy_px = spy_px.reindex(common).ffill()
    return stk_px, spy_px


# ==============================================================
# UTILITIES / CONSTRAINTS
# ==============================================================


def apply_sector_and_cap_constraints(w: pd.Series) -> pd.Series:
    if w.empty:
        return w
    w = w.copy()

    sec = pd.Series({t: SECTOR_MAP.get(t, "Other") for t in w.index})
    for sname, tot in w.groupby(sec).sum().items():
        if tot > MAX_SECTOR_WEIGHT:
            w.loc[sec == sname] *= MAX_SECTOR_WEIGHT / tot

    w = pd.Series(np.clip(w.values, 0, CORE_CAP_PER_NAME), index=w.index)
    s = float(w.sum())
    if s > 0:
        w /= s
    return w


# ==============================================================
# RESIDUAL MOMENTUM
# ==============================================================


def compute_residual_momentum(
    stk_hist: pd.DataFrame, spy_hist: pd.Series, lookback: int = 26
) -> pd.Series:
    if len(stk_hist) <= lookback + 2 or len(spy_hist) <= lookback + 2:
        return pd.Series(dtype=float)

    stk_lb = stk_hist.pct_change(lookback).dropna()
    spy_lb = spy_hist.pct_change(lookback).dropna()
    if stk_lb.empty or spy_lb.empty:
        return pd.Series(dtype=float)

    last_ret = stk_lb.iloc[-1]
    spy_last = float(spy_lb.iloc[-1])

    r_stock = stk_hist.pct_change().dropna()
    r_mkt = spy_hist.pct_change().reindex(r_stock.index).dropna()

    resids: Dict[str, float] = {}
    for t in r_stock.columns:
        s = r_stock[t].dropna()
        jj = s.index.intersection(r_mkt.index)
        if len(jj) < 52 or t not in last_ret.index:
            continue
        X = np.column_stack([np.ones(len(jj)), r_mkt.loc[jj].values])
        y = s.loc[jj].values
        beta = np.linalg.lstsq(X, y, rcond=None)[0][1]
        resids[t] = float(last_ret[t] - beta * spy_last)

    return pd.Series(resids).dropna()


# ==============================================================
# FEATURES / ML
# ==============================================================

FEATURE_COLS = ["r4", "r13", "r26", "r52", "vol13", "vol26", "spy4", "spy13", "spy26"]


def make_features(stk_px: pd.DataFrame, spy_px: pd.Series, i: int) -> pd.DataFrame:
    if i < 53:
        return pd.DataFrame()
    rows: Dict[str, List[float]] = {}
    spy_hist = spy_px.iloc[: i + 1]
    if len(spy_hist) < 53:
        return pd.DataFrame()

    spy4 = (spy_hist.iloc[-1] / spy_hist.iloc[-5]) - 1
    spy13 = (spy_hist.iloc[-1] / spy_hist.iloc[-14]) - 1
    spy26 = (spy_hist.iloc[-1] / spy_hist.iloc[-27]) - 1

    for t in stk_px.columns:
        s = stk_px[t].iloc[: i + 1]
        if len(s) < 53:
            continue
        r4 = (s.iloc[-1] / s.iloc[-5]) - 1
        r13 = (s.iloc[-1] / s.iloc[-14]) - 1
        r26 = (s.iloc[-1] / s.iloc[-27]) - 1
        r52 = (s.iloc[-1] / s.iloc[-53]) - 1
        rs = s.pct_change().dropna()
        vol13 = rs.tail(13).std() * np.sqrt(52)
        vol26 = rs.tail(26).std() * np.sqrt(52)

        vals = [r4, r13, r26, r52, float(vol13), float(vol26), spy4, spy13, spy26]
        if np.any(pd.isna(vals)) or np.any(~np.isfinite(vals)):
            continue
        rows[t] = vals

    if not rows:
        return pd.DataFrame()
    return pd.DataFrame.from_dict(rows, orient="index", columns=FEATURE_COLS)


def build_feature_cache(stk_px: pd.DataFrame, spy_px: pd.Series) -> Dict[int, pd.DataFrame]:
    cache: Dict[int, pd.DataFrame] = {}
    dates = stk_px.index
    for i in tqdm(range(53, len(dates) - 5), desc="Building feature cache"):
        f = make_features(stk_px, spy_px, i)
        if not f.empty:
            cache[i] = f
    return cache


def train_xgb_walkforward_cached(
    feature_cache: Dict[int, pd.DataFrame],
    stk_px: pd.DataFrame,
    tickers: List[str],
    end_idx: int,
) -> Optional[XGBRegressor]:
    feats: List[np.ndarray] = []
    targets: List[float] = []
    last = min(end_idx, len(stk_px.index) - 5)

    for j in range(52, last):
        f = feature_cache.get(j)
        if f is None:
            continue
        idx_tks = f.index.intersection(tickers)
        if len(idx_tks) == 0:
            continue
        for t in idx_tks:
            s = stk_px[t]
            if j + 4 >= len(s):
                continue
            fwd = (s.iloc[j + 4] / s.iloc[j]) - 1.0
            if np.isfinite(fwd):
                feats.append(f.loc[t].values)
                targets.append(float(fwd))

    if not feats:
        return None

    model = XGBRegressor(
        n_estimators=180,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=1.0,
        objective="reg:squarederror",
        random_state=42,
        n_jobs=-1,
    )
    model.fit(np.array(feats), np.array(targets))
    return model


# ==============================================================
# QUARTERLY UNIVERSE (SURVIVORSHIP-SAFeR)
# ==============================================================


def build_quarterly_universe(stk_px: pd.DataFrame, wk_vol: pd.DataFrame) -> Dict[pd.Timestamp, List[str]]:
    """
    Eligibility gate at each rebalance date:
      - has at least 52 weeks price history
      - has rolling ADV >= MIN_DOLLAR_VOL (if volume exists)
    """
    dv = stk_px * wk_vol.reindex(stk_px.index)
    dv_roll = dv.rolling(LIQ_LOOKBACK_W).mean()

    eligible_by_date: Dict[pd.Timestamp, List[str]] = {}
    for dt in stk_px.index:
        if dt.month not in CORE_REBAL_MONTHS:
            continue

        adv_row = dv_roll.loc[dt] if dt in dv_roll.index else pd.Series(dtype=float)
        eligible: List[str] = []

        for t in UNIVERSE:
            if t not in stk_px.columns:
                continue

            s = stk_px[t].loc[:dt].dropna()
            if len(s) < 52:
                continue

            adv_ok = True
            if t in adv_row.index and np.isfinite(adv_row[t]):
                adv_ok = bool(float(adv_row[t]) >= MIN_DOLLAR_VOL)
            else:
                adv_ok = True

            if not adv_ok:
                continue

            eligible.append(t)

        eligible_by_date[dt] = sorted(set(eligible))

    return eligible_by_date


# ==============================================================
# SIGNAL-WEIGHTED HRP
# ==============================================================


def _cluster_variance(cov: pd.DataFrame, cluster: List[str]) -> float:
    sub = cov.loc[cluster, cluster]
    w = np.ones(len(cluster)) / len(cluster)
    return float(w @ sub.values @ w)


def _cluster_signal(scores: pd.Series, cluster: List[str]) -> float:
    sc = scores.reindex(cluster).dropna()
    if sc.empty:
        return 1.0
    return float(sc.mean())


def hrp_signal_allocation(
    returns: pd.DataFrame,
    scores: pd.Series,
    alpha: float = HRP_SIGNAL_ALPHA,
) -> pd.Series:
    assets = list(returns.columns)
    if len(assets) == 0:
        return pd.Series(dtype=float)

    cov = returns.cov()
    corr = returns.corr().fillna(0.0).clip(-1.0, 1.0)

    dist = np.sqrt(0.5 * (1.0 - corr))
    dist_condensed = squareform(dist.values, checks=False)
    Z = linkage(dist_condensed, method="average")
    order = leaves_list(Z)
    ordered_assets = [assets[i] for i in order]

    sc = scores.reindex(ordered_assets).copy()
    med = float(sc.median()) if np.isfinite(sc.median()) else 0.5
    sc = sc.fillna(med)
    sc_min, sc_max = float(sc.min()), float(sc.max())
    if sc_max > sc_min:
        sc_norm = (sc - sc_min) / (sc_max - sc_min)
    else:
        sc_norm = pd.Series(0.5, index=sc.index)
    sc_norm = sc_norm.clip(lower=1e-3)

    w = pd.Series(1.0, index=ordered_assets)
    clusters: List[List[str]] = [ordered_assets]

    while clusters:
        cluster = clusters.pop(0)
        if len(cluster) <= 1:
            continue
        split = len(cluster) // 2
        left, right = cluster[:split], cluster[split:]

        var_l = _cluster_variance(cov, left)
        var_r = _cluster_variance(cov, right)

        sig_l = _cluster_signal(sc_norm, left)
        sig_r = _cluster_signal(sc_norm, right)

        eff_l = var_l / (sig_l**alpha + 1e-6)
        eff_r = var_r / (sig_r**alpha + 1e-6)

        w_l = 1.0 - eff_l / (eff_l + eff_r)
        w_r = 1.0 - w_l

        w[left] *= w_l
        w[right] *= w_r

        clusters.extend([left, right])

    w = w / w.sum()
    return w


# ==============================================================
# REBALANCE ENGINE (TARGET WEIGHTS + TRADE SHEET)
# ==============================================================


@dataclass
class Holdings:
    cash_usd: float
    shares: pd.Series  # index=ticker, values=shares


def cash_only_holdings(cash_usd: float = INIT_CASH) -> Holdings:
    return Holdings(cash_usd=float(cash_usd), shares=pd.Series(dtype=float))


def compute_nav_from_holdings(holdings: Holdings, prices: pd.Series) -> float:
    if holdings.shares.empty:
        return float(holdings.cash_usd)
    px = prices.reindex(holdings.shares.index).dropna()
    pos_val = float((holdings.shares.reindex(px.index) * px).sum())
    return float(holdings.cash_usd + pos_val)


def build_signals_at_date(
    stk_px: pd.DataFrame,
    spy_px: pd.Series,
    dt: pd.Timestamp,
    i: int,
    eligible: List[str],
    feature_cache: Dict[int, pd.DataFrame],
    use_ml: bool,
) -> Tuple[pd.Series, pd.DataFrame]:
    mom26_all = stk_px.pct_change(26)
    mom26 = mom26_all.iloc[i].dropna()
    mom = mom26.reindex(eligible).dropna()

    res_mom = compute_residual_momentum(stk_px[eligible].loc[:dt], spy_px.loc[:dt])
    resid = res_mom.reindex(eligible).dropna()

    names = mom.index.intersection(resid.index) if not resid.empty else mom.index
    if len(names) == 0:
        return pd.Series(dtype=float), pd.DataFrame()

    mom_rank = mom.loc[names].rank(pct=True)
    resid_rank = resid.loc[names].rank(pct=True) if not resid.empty else pd.Series(0.5, index=names)

    ml_rank = pd.Series(0.5, index=names)
    if use_ml:
        feats = feature_cache.get(i)
        if feats is not None:
            feats_sel = feats.reindex(names).dropna()
            if not feats_sel.empty:
                model = train_xgb_walkforward_cached(feature_cache, stk_px[eligible], eligible, i)
                if model is not None:
                    preds = pd.Series(model.predict(feats_sel.values), index=feats_sel.index)
                    ml_rank = preds.rank(pct=True).reindex(names).fillna(0.5)

    score = (W_MOM * mom_rank) + (W_RESID * resid_rank) + (W_ML * ml_rank)
    dbg = (
        pd.DataFrame(
            {
                "mom26": mom.loc[names],
                "resid_mom": resid.reindex(names),
                "mom_rank": mom_rank,
                "resid_rank": resid_rank,
                "ml_rank": ml_rank,
                "score": score,
            }
        )
        .sort_values("score", ascending=False)
        .copy()
    )

    return score.sort_values(ascending=False), dbg


def build_target_weights(ret_slice: pd.DataFrame, scores: pd.Series) -> pd.Series:
    top = scores.sort_values(ascending=False).head(CORE_TOP_K)
    ret_sel = ret_slice[top.index].dropna(how="all")
    if ret_sel.shape[0] < 26:
        return pd.Series(dtype=float)

    w = hrp_signal_allocation(ret_sel, top, alpha=HRP_SIGNAL_ALPHA)
    w = apply_sector_and_cap_constraints(w)
    return w


def generate_trade_sheet(
    dt: pd.Timestamp,
    holdings: Holdings,
    prices: pd.Series,
    target_w: pd.Series,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    nav = compute_nav_from_holdings(holdings, prices)
    invest_val = nav * TARGET_CORE_FRACT

    cur_px = prices.reindex(holdings.shares.index).dropna()
    cur_val = holdings.shares.reindex(cur_px.index) * cur_px if not holdings.shares.empty else pd.Series(dtype=float)
    cur_w = (cur_val / nav).fillna(0.0) if nav > 0 else pd.Series(dtype=float)

    tickers = sorted(set(target_w.index).union(cur_w.index))
    px = prices.reindex(tickers).dropna()
    target_w = target_w.reindex(px.index).fillna(0.0)

    target_val = target_w * invest_val
    target_sh = target_val / px

    cur_sh = holdings.shares.reindex(px.index).fillna(0.0)
    delta_sh = target_sh - cur_sh
    delta_notional = delta_sh * px

    keep = delta_notional.abs() >= MIN_TRADE_USD
    delta_sh = delta_sh[keep]
    delta_notional = delta_notional[keep]
    px2 = px.reindex(delta_sh.index)

    if ROUND_SHARES:
        delta_sh_rounded = delta_sh.round(0)
        delta_notional = delta_sh_rounded * px2
        delta_sh = delta_sh_rounded

        keep2 = delta_sh != 0
        delta_sh = delta_sh[keep2]
        delta_notional = delta_notional[keep2]
        px2 = px2.reindex(delta_sh.index)

    est_tc = delta_notional.abs() * (EQUITY_TC_BPS + SLIPPAGE_BPS) + (
        delta_notional.abs()
        * (IMPACT_COEFF * 0.5 * np.sqrt(np.maximum(delta_notional.abs(), 1.0) / 1e9))
    )

    side = np.where(delta_sh.values > 0, "BUY", "SELL")
    trades_df = (
        pd.DataFrame(
            {
                "date": dt,
                "side": side,
                "ticker": delta_sh.index,
                "shares": delta_sh.values,
                "price": px2.values,
                "notional_usd": delta_notional.values,
                "est_cost_usd": est_tc.values,
            }
        )
        .sort_values(["side", "notional_usd"], ascending=[True, False])
        .reset_index(drop=True)
    )

    tgt_w_full = target_w.reindex(tickers).fillna(0.0)
    cur_w_full = cur_w.reindex(tickers).fillna(0.0)
    turnover = float((tgt_w_full - cur_w_full).abs().sum())

    summary_df = pd.DataFrame(
        [
            {
                "date": dt,
                "nav_usd": float(nav),
                "cash_usd": float(holdings.cash_usd),
                "invest_target_usd": float(invest_val),
                "turnover_est": float(turnover),
                "num_trades": int(len(trades_df)),
                "est_total_cost_usd": float(trades_df["est_cost_usd"].sum()) if len(trades_df) else 0.0,
            }
        ]
    )

    return trades_df, summary_df


# ==============================================================
# RUN MODE: CASH-ONLY LIVE PLAN ✅
# ==============================================================


def run_live_plan_cash_only(
    cash_usd: float = INIT_CASH,
    use_ml: bool = True,
    asof_date: Optional[pd.Timestamp] = None,
) -> Tuple[pd.Series, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    LIVE PLAN MODE (CASH ONLY):
      - Starts from cash only (no holdings CSV)
      - Uses the latest available weekly bar (or asof_date if provided)
      - Outputs:
          target_weights.csv
          signal_debug.csv
          trades.csv
          summary.csv
    """
    print("Downloading data...")
    stk_wk_px, wk_vol = download_weekly(UNIVERSE, START, END)
    spy_wk_px, _ = download_weekly([INDEX_TKR], START, END)

    if INDEX_TKR not in spy_wk_px.columns:
        raise ValueError(f"Index ticker {INDEX_TKR} not found in downloaded data.")

    spy_px = spy_wk_px[INDEX_TKR]

    stk_wk_px, spy_px = align_on_common_index(stk_wk_px, spy_px)
    wk_vol = wk_vol.reindex(stk_wk_px.index).ffill()
    print(f"Loaded weekly data: {stk_wk_px.shape}")

    print("Building quarterly universe...")
    eligible_by_date = build_quarterly_universe(stk_wk_px, wk_vol)

    print("Building feature cache...")
    feature_cache = build_feature_cache(stk_wk_px, spy_px)

    dates = stk_wk_px.index
    if asof_date is None:
        asof_date = dates[-1]
    asof_date = pd.Timestamp(asof_date)

    rebalance_dates = [d for d in eligible_by_date.keys() if d <= asof_date]
    if not rebalance_dates:
        raise ValueError("No rebalance dates available before asof_date.")
    dt = max(rebalance_dates)

    idx_arr = np.where(dates == dt)[0]
    if len(idx_arr) == 0:
        raise ValueError("Rebalance date not found in price index (unexpected alignment issue).")
    i = int(idx_arr[0])

    eligible = eligible_by_date.get(dt, [])
    if len(eligible) < CORE_TOP_K:
        raise ValueError(f"Eligible universe too small at {dt.date()}: {len(eligible)}")

    print(f"Rebalance date selected: {dt.date()} | eligible: {len(eligible)} | use_ml={use_ml}")

    scores, dbg = build_signals_at_date(stk_wk_px, spy_px, dt, i, eligible, feature_cache, use_ml)
    if scores.empty:
        raise ValueError("No signals produced; check data / eligibility thresholds.")

    ret_wk = stk_wk_px.pct_change()
    ret_slice = ret_wk.iloc[max(0, i - 52) : i]
    target_w = build_target_weights(ret_slice, scores)
    if target_w.empty:
        raise ValueError("Target weights empty (likely insufficient return history window).")

    # cash-only holdings
    holdings = cash_only_holdings(cash_usd=cash_usd)

    px_now = stk_wk_px.loc[dt].dropna()
    trades, summary = generate_trade_sheet(dt, holdings, px_now, target_w)

    target_w.to_csv("target_weights.csv", header=True)
    dbg.to_csv("signal_debug.csv")
    trades.to_csv("trades.csv", index=False)
    summary.to_csv("summary.csv", index=False)

    print("\nSaved:")
    print(" - target_weights.csv")
    print(" - signal_debug.csv")
    print(" - trades.csv")
    print(" - summary.csv")

    print("\nTop target weights:")
    print(target_w.sort_values(ascending=False).head(10).round(4))

    print("\nTrade sheet preview:")
    print(trades.head(12))

    print("\nSummary:")
    print(summary.round(4))

    return target_w, dbg, trades, summary


if __name__ == "__main__":
    # Cash-only live plan
    run_live_plan_cash_only(cash_usd=10_000.0, use_ml=True, asof_date=None)
