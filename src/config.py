from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "outputs"
DATA_FILE = DATA_DIR / "resale_data.csv"
ORIGINAL_DATA_FILE = DATA_DIR / "original_milestone_resale_data.csv"
CARD_BASELINES_FILE = DATA_DIR / "card_value_baselines.csv"

FEATURE_COLUMNS = [
    "grade",
    "asking_price",
    "simple_market_value",
    "weighted_market_value",
    "difference_percent",
    "sale_count",
    "volatility_percent",
]

# Final project scope: exactly 13 players.
# Keeping this scope tight makes the UI easier to demo and the dataset easier to explain.
APP_PLAYERS = [
    "Connor Bedard",
    "Auston Matthews",
    "Sidney Crosby",
    "Wayne Gretzky",
    "Victor Wembanyama",
    "LeBron James",
    "Michael Jordan",
    "Kobe Bryant",
    "Shohei Ohtani",
    "Tom Brady",
    "Patrick Mahomes",
    "Lionel Messi",
    "Cristiano Ronaldo",
]

DEFAULT_PLAYER = "Connor Bedard"
DEFAULT_CARD = "Upper Deck Young Guns RC"
DEFAULT_GRADE = 9

SPORT_MAP = {
    "Connor Bedard": "Hockey",
    "Auston Matthews": "Hockey",
    "Sidney Crosby": "Hockey",
    "Wayne Gretzky": "Hockey",
    "Victor Wembanyama": "Basketball",
    "LeBron James": "Basketball",
    "Michael Jordan": "Basketball",
    "Kobe Bryant": "Basketball",
    "Shohei Ohtani": "Baseball",
    "Tom Brady": "Football",
    "Patrick Mahomes": "Football",
    "Lionel Messi": "Soccer",
    "Cristiano Ronaldo": "Soccer",
}

RECOMMENDATIONS = {
    "Good Deal": "Buy",
    "Fair Price": "Watch / Negotiate",
    "Overpriced": "Avoid",
}

APP_NAME = "Resale Tracker"
TEAM_MEMBERS = ["Sharnpreet Sidhu", "Ariful Shayun", "Raj Chowdhury", "Justin Huang"]
