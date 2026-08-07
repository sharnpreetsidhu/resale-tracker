from __future__ import annotations

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from .config import FEATURE_COLUMNS
from .pricing import label_from_gap, summarize_market


def build_training_examples(df: pd.DataFrame) -> pd.DataFrame:
    """Create supervised examples from market-value thresholds for this prototype."""
    summary = summarize_market(df)
    rows = []
    multipliers = [0.68, 0.78, 0.88, 0.97, 1.03, 1.12, 1.22, 1.35]

    for _, row in summary.iterrows():
        market = float(row["weighted_market_value"])
        for mult in multipliers:
            asking = float(market * mult)
            gap = float((market - asking) / market * 100)
            rows.append({
                "grade": row["grade"],
                "asking_price": asking,
                "simple_market_value": row["simple_market_value"],
                "weighted_market_value": row["weighted_market_value"],
                "difference_percent": gap,
                "sale_count": row["sale_count"],
                "volatility_percent": row["volatility_percent"],
                "deal_label": label_from_gap(gap),
            })
    return pd.DataFrame(rows)


def train_and_compare_models(df: pd.DataFrame, random_state: int = 42) -> dict:
    training_df = build_training_examples(df)
    X = training_df[FEATURE_COLUMNS]
    y = training_df["deal_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=random_state,
        stratify=y,
    )

    candidates = {
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=random_state),
        "Random Forest": RandomForestClassifier(n_estimators=160, max_depth=7, random_state=random_state),
    }

    fitted = {}
    scores = {}
    reports = {}

    for name, model in candidates.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        fitted[name] = model
        scores[name] = accuracy_score(y_test, y_pred)
        reports[name] = classification_report(y_test, y_pred, zero_division=0)

    best_name = max(scores, key=scores.get)
    best_model = fitted[best_name]
    labels = sorted(y.unique())
    best_pred = best_model.predict(X_test)

    return {
        "training_df": training_df,
        "feature_columns": FEATURE_COLUMNS,
        "models": fitted,
        "scores": scores,
        "reports": reports,
        "best_name": best_name,
        "best_model": best_model,
        "labels": labels,
        "confusion_matrix": confusion_matrix(y_test, best_pred, labels=labels),
        "X_test": X_test,
        "y_test": y_test,
        "y_pred": best_pred,
    }
