from __future__ import annotations

from pathlib import Path
import pandas as pd

from .config import DATA_FILE, SPORT_MAP


def infer_rarity(card_name: str) -> str:
    """Infer a simple rarity label from the card name for feature/display use."""
    name = str(card_name).lower()
    if "national" in name or "patch" in name or "auto" in name:
        return "Ultra Rare"
    if "prizm" in name or "chrome" in name or "young guns" in name or "holo" in name:
        return "Rare"
    if "rated" in name or "select" in name or "silver" in name:
        return "Uncommon"
    return "Common"


def load_resale_data(path: Path | str = DATA_FILE) -> pd.DataFrame:
    """Load, validate, and lightly clean the resale dataset."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Could not find dataset at {path}")

    df = pd.read_csv(path)
    required = {"player", "year", "card_name", "grade", "sale_price", "site", "sale_date"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    df = df.copy()
    df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["grade"] = pd.to_numeric(df["grade"], errors="coerce")
    df["sale_price"] = pd.to_numeric(df["sale_price"], errors="coerce")
    df = df.dropna(subset=["player", "card_name", "year", "grade", "sale_price", "site", "sale_date"])
    df["year"] = df["year"].astype(int)
    df["grade"] = df["grade"].astype(int)

    df["player"] = df["player"].astype(str).str.strip()
    df["card_name"] = df["card_name"].astype(str).str.strip()
    df["site"] = df["site"].astype(str).str.strip()

    if "sport" not in df.columns:
        df["sport"] = df["player"].map(SPORT_MAP).fillna("Trading Cards")
    else:
        df["sport"] = df["sport"].fillna(df["player"].map(SPORT_MAP)).fillna("Trading Cards")

    if "rarity" not in df.columns:
        df["rarity"] = df["card_name"].apply(infer_rarity)
    else:
        df["rarity"] = df["rarity"].fillna(df["card_name"].apply(infer_rarity))

    if "autograph" not in df.columns:
        df["autograph"] = df["card_name"].str.contains("auto|patch", case=False, regex=True).map({True: "Yes", False: "No"})

    if "rookie_card" not in df.columns:
        df["rookie_card"] = "Yes"

    if "condition" not in df.columns:
        df["condition"] = "Graded"

    return df.sort_values(["player", "card_name", "grade", "sale_date"]).reset_index(drop=True)
