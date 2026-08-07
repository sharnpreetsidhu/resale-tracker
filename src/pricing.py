from __future__ import annotations

import numpy as np
import pandas as pd

from .config import RECOMMENDATIONS


def weighted_average_price(matches: pd.DataFrame) -> float:
    """Recency-weighted average where newer sales count more."""
    if matches.empty:
        return 0.0
    ordered = matches.sort_values("sale_date")
    weights = np.arange(1, len(ordered) + 1)
    return float(np.average(ordered["sale_price"], weights=weights))


def simple_average_price(matches: pd.DataFrame) -> float:
    return 0.0 if matches.empty else float(matches["sale_price"].mean())


def volatility_percent(matches: pd.DataFrame) -> float:
    simple = simple_average_price(matches)
    if matches.empty or simple == 0:
        return 0.0
    return float(matches["sale_price"].std(ddof=0) / simple * 100)


def market_gap_percent(weighted_market_value: float, asking_price: float) -> float:
    if weighted_market_value == 0:
        return 0.0
    return float((weighted_market_value - asking_price) / weighted_market_value * 100)


def label_from_gap(gap: float) -> str:
    if gap >= 12:
        return "Good Deal"
    if gap <= -12:
        return "Overpriced"
    return "Fair Price"


def recommendation_from_label(label: str) -> str:
    return RECOMMENDATIONS.get(label, "Watch")


def deal_score_from_gap(gap: float) -> int:
    """Converts market gap into a reseller-friendly 1-99 score."""
    return int(np.clip(50 + gap * 2.2, 1, 99))


def signal_name(label: str, score: int) -> str:
    if label == "Good Deal" and score >= 85:
        return "Strong Buy"
    if label == "Good Deal":
        return "Buy"
    if label == "Fair Price":
        return "Watch / Negotiate"
    return "Avoid"


def summarize_market(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (player, card_name, grade), group in df.groupby(["player", "card_name", "grade"]):
        simple = simple_average_price(group)
        weighted = weighted_average_price(group)
        latest = group.sort_values("sale_date").iloc[-1]
        rows.append({
            "player": player,
            "card_name": card_name,
            "grade": int(grade),
            "simple_market_value": simple,
            "weighted_market_value": weighted,
            "sale_count": int(len(group)),
            "volatility_percent": volatility_percent(group),
            "last_sale_price": float(latest["sale_price"]),
            "last_sale_date": latest["sale_date"],
        })
    return pd.DataFrame(rows)


def build_prediction_features(grade: int, asking_price: float, matches: pd.DataFrame) -> pd.DataFrame:
    simple = simple_average_price(matches)
    weighted = weighted_average_price(matches)
    gap = market_gap_percent(weighted, asking_price)
    return pd.DataFrame([{
        "grade": grade,
        "asking_price": asking_price,
        "simple_market_value": simple,
        "weighted_market_value": weighted,
        "difference_percent": gap,
        "sale_count": int(len(matches)),
        "volatility_percent": volatility_percent(matches),
    }])


def explain_recommendation(label: str, gap: float, simple: float, weighted: float, site_summary: pd.DataFrame, volatility: float) -> list[str]:
    best_site = site_summary.sort_values("sale_price", ascending=False).iloc[0]
    reasons = [
        f"The asking price is {abs(gap):.2f}% {'below' if gap >= 0 else 'above'} the recency-weighted market estimate.",
        f"Recent comparable sales average ${simple:,.2f}, while the recency-weighted estimate is ${weighted:,.2f}.",
        f"The strongest marketplace signal is {best_site['site']} with an average sale price of ${best_site['sale_price']:,.2f}.",
        f"Price volatility is {volatility:.2f}%, which helps estimate how stable the recent market is.",
    ]
    if label == "Good Deal":
        reasons.insert(0, "This listing is below current comps, giving a reseller potential room for profit before fees and shipping.")
    elif label == "Fair Price":
        reasons.insert(0, "This listing is close to market value, so it may be worth watching or negotiating lower.")
    else:
        reasons.insert(0, "This listing is above current comps, so the expected resale upside is weak.")
    return reasons
