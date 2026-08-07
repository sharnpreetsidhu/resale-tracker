from __future__ import annotations

from datetime import datetime, timedelta
import random
import re

import numpy as np
import pandas as pd

from src.config import DATA_FILE, DATA_DIR

RANDOM_SEED = 27
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# Final project dataset scope: 13 players, real card identities, many realistic comps per card.
# The rows are generated around approximate price-guide-style baselines for a reproducible prototype.
# Do not describe every row as a verified live sale unless you replace it with manually logged sold listings.
CARDS = [{'player': 'Connor Bedard', 'card_name': 'Upper Deck Young Guns RC', 'sport': 'Hockey', 'year': 2023, 'base_psa9': 220, 'rarity': 'Rare', 'autograph': 'No'}, {'player': 'Connor Bedard', 'card_name': 'Upper Deck Canvas Young Guns', 'sport': 'Hockey', 'year': 2023, 'base_psa9': 80, 'rarity': 'Rare', 'autograph': 'No'}, {'player': 'Connor Bedard', 'card_name': 'SP Authentic Future Watch Auto', 'sport': 'Hockey', 'year': 2023, 'base_psa9': 1200, 'rarity': 'Ultra Rare', 'autograph': 'Yes'}, {'player': 'Auston Matthews', 'card_name': 'Upper Deck Young Guns RC', 'sport': 'Hockey', 'year': 2016, 'base_psa9': 170, 'rarity': 'Rare', 'autograph': 'No'}, {'player': 'Auston Matthews', 'card_name': 'O-Pee-Chee Platinum Rookie', 'sport': 'Hockey', 'year': 2016, 'base_psa9': 110, 'rarity': 'Rare', 'autograph': 'No'}, {'player': 'Sidney Crosby', 'card_name': 'Upper Deck Young Guns RC', 'sport': 'Hockey', 'year': 2005, 'base_psa9': 550, 'rarity': 'Rare', 'autograph': 'No'}, {'player': 'Sidney Crosby', 'card_name': 'SP Authentic Future Watch Auto', 'sport': 'Hockey', 'year': 2005, 'base_psa9': 1800, 'rarity': 'Ultra Rare', 'autograph': 'Yes'}, {'player': 'Wayne Gretzky', 'card_name': 'O-Pee-Chee Rookie', 'sport': 'Hockey', 'year': 1979, 'base_psa9': 27000, 'rarity': 'Iconic', 'autograph': 'No'}, {'player': 'Wayne Gretzky', 'card_name': 'Topps Rookie', 'sport': 'Hockey', 'year': 1979, 'base_psa9': 6500, 'rarity': 'Iconic', 'autograph': 'No'}, {'player': 'Victor Wembanyama', 'card_name': 'Panini Prizm Rookie', 'sport': 'Basketball', 'year': 2023, 'base_psa9': 180, 'rarity': 'Rare', 'autograph': 'No'}, {'player': 'Victor Wembanyama', 'card_name': 'Donruss Rated Rookie', 'sport': 'Basketball', 'year': 2023, 'base_psa9': 60, 'rarity': 'Uncommon', 'autograph': 'No'}, {'player': 'Victor Wembanyama', 'card_name': 'NBA Hoops Rookie', 'sport': 'Basketball', 'year': 2023, 'base_psa9': 35, 'rarity': 'Common', 'autograph': 'No'}, {'player': 'LeBron James', 'card_name': 'Topps Chrome Rookie', 'sport': 'Basketball', 'year': 2003, 'base_psa9': 2200, 'rarity': 'Rare', 'autograph': 'No'}, {'player': 'LeBron James', 'card_name': 'Topps Rookie', 'sport': 'Basketball', 'year': 2003, 'base_psa9': 900, 'rarity': 'Rare', 'autograph': 'No'}, {'player': 'LeBron James', 'card_name': 'Upper Deck Rookie Exclusives', 'sport': 'Basketball', 'year': 2003, 'base_psa9': 380, 'rarity': 'Uncommon', 'autograph': 'No'}, {'player': 'Michael Jordan', 'card_name': 'Fleer Rookie', 'sport': 'Basketball', 'year': 1986, 'base_psa9': 18000, 'rarity': 'Iconic', 'autograph': 'No'}, {'player': 'Kobe Bryant', 'card_name': 'Topps Rookie', 'sport': 'Basketball', 'year': 1996, 'base_psa9': 500, 'rarity': 'Rare', 'autograph': 'No'}, {'player': 'Kobe Bryant', 'card_name': 'Finest Rookie', 'sport': 'Basketball', 'year': 1996, 'base_psa9': 900, 'rarity': 'Rare', 'autograph': 'No'}, {'player': 'Shohei Ohtani', 'card_name': 'Topps Chrome Rookie', 'sport': 'Baseball', 'year': 2018, 'base_psa9': 220, 'rarity': 'Rare', 'autograph': 'No'}, {'player': 'Shohei Ohtani', 'card_name': 'Topps Chrome Update Rookie', 'sport': 'Baseball', 'year': 2018, 'base_psa9': 240, 'rarity': 'Rare', 'autograph': 'No'}, {'player': 'Shohei Ohtani', 'card_name': 'Topps Update Rookie', 'sport': 'Baseball', 'year': 2018, 'base_psa9': 150, 'rarity': 'Rare', 'autograph': 'No'}, {'player': 'Tom Brady', 'card_name': 'Bowman Rookie', 'sport': 'Football', 'year': 2000, 'base_psa9': 800, 'rarity': 'Rare', 'autograph': 'No'}, {'player': 'Tom Brady', 'card_name': 'Bowman Chrome Rookie', 'sport': 'Football', 'year': 2000, 'base_psa9': 1800, 'rarity': 'Rare', 'autograph': 'No'}, {'player': 'Patrick Mahomes', 'card_name': 'Donruss Rated Rookie', 'sport': 'Football', 'year': 2017, 'base_psa9': 430, 'rarity': 'Uncommon', 'autograph': 'No'}, {'player': 'Patrick Mahomes', 'card_name': 'Panini Prizm Rookie', 'sport': 'Football', 'year': 2017, 'base_psa9': 700, 'rarity': 'Rare', 'autograph': 'No'}, {'player': 'Lionel Messi', 'card_name': 'Mega Cracks Rookie', 'sport': 'Soccer', 'year': 2004, 'base_psa9': 1100, 'rarity': 'Iconic', 'autograph': 'No'}, {'player': 'Cristiano Ronaldo', 'card_name': 'Panini Mega Cracks Rookie', 'sport': 'Soccer', 'year': 2002, 'base_psa9': 760, 'rarity': 'Iconic', 'autograph': 'No'}]

SITES = ["eBay Sold", "130point", "PWCC", "Goldin", "Card Ladder", "Marketplace", "Card Show"]
SITE_MULTIPLIER = {
    "eBay Sold": 1.00,
    "130point": 1.02,
    "PWCC": 1.05,
    "Goldin": 1.08,
    "Card Ladder": 1.01,
    "Marketplace": 0.94,
    "Card Show": 0.97,
}
SITE_WEIGHTS = [42, 20, 7, 4, 8, 14, 5]
GRADE_MULTIPLIER = {6: 0.28, 7: 0.42, 8: 0.65, 9: 1.00, 10: 1.85}
START_DATE = datetime(2026, 2, 1)
SALES_PER_CARD_GRADE = 72


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")


def build_dataset() -> pd.DataFrame:
    rows = []

    for card in CARDS:
        for grade, grade_multiplier in GRADE_MULTIPLIER.items():
            baseline = card["base_psa9"] * grade_multiplier
            total_trend = random.uniform(-0.06, 0.08)

            for _ in range(SALES_PER_CARD_GRADE):
                sale_date = START_DATE + timedelta(days=random.randint(0, 175))
                age_factor = (sale_date - START_DATE).days / 175
                site = random.choices(SITES, weights=SITE_WEIGHTS, k=1)[0]

                volatility = 0.08 if card["base_psa9"] < 500 else 0.10 if card["base_psa9"] < 2000 else 0.13
                variation = random.gauss(1 + total_trend * age_factor, volatility)
                variation = max(0.65, min(1.45, variation))

                rows.append({
                    "sale_id": f"RT-{len(rows) + 1:06d}",
                    "player": card["player"],
                    "year": card["year"],
                    "card_name": card["card_name"],
                    "sport": card["sport"],
                    "grade": grade,
                    "rarity": card["rarity"],
                    "autograph": card["autograph"],
                    "rookie_card": "Yes",
                    "condition": f"Graded {grade}",
                    "sale_price": round(baseline * SITE_MULTIPLIER[site] * variation, 2),
                    "site": site,
                    "sale_date": sale_date.strftime("%Y-%m-%d"),
                    "baseline_psa9_value": card["base_psa9"],
                    "value_note": "Real card identity; approximate price-guide-style baseline with generated comparable-sales variation for prototype testing",
                })

    return (
        pd.DataFrame(rows)
        .sort_values(["sport", "player", "card_name", "grade", "sale_date"])
        .reset_index(drop=True)
    )


def build_baseline_table() -> pd.DataFrame:
    baseline_df = pd.DataFrame(CARDS)
    baseline_df["image_filename_png"] = baseline_df.apply(
        lambda row: f"{slugify(row['player'])}-{slugify(row['card_name'])}.png",
        axis=1,
    )
    baseline_df["image_filename_jpg"] = baseline_df.apply(
        lambda row: f"{slugify(row['player'])}-{slugify(row['card_name'])}.jpg",
        axis=1,
    )
    baseline_df["data_note"] = (
        "Real card identity; baseline value is an approximate price-guide-style seed "
        "for prototype comps, not a verified live sale."
    )
    return baseline_df


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    data = build_dataset()
    baselines = build_baseline_table()

    data.to_csv(DATA_FILE, index=False)
    baselines.to_csv(DATA_DIR / "card_value_baselines.csv", index=False)

    print("Generated Resale Tracker dataset")
    print(f"Rows: {len(data):,}")
    print(f"Cards: {data[['player', 'card_name']].drop_duplicates().shape[0]}")
    print(f"Players: {data['player'].nunique()}")
    print(f"Saved: {DATA_FILE}")
    print(f"Saved: {DATA_DIR / 'card_value_baselines.csv'}")
