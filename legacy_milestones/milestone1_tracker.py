import pandas as pd

DATA_FILE = "resale_data.csv"


def load_data():
    """Load resale data from CSV."""
    try:
        return pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        print(f"Error: {DATA_FILE} was not found.")
        print("Make sure resale_data.csv is in the same folder as this Python file.")
        raise SystemExit


def get_matching_sales(df, player, card_name, grade):
    """Filter the dataset for matching player, card, and grade."""
    return df[
        (df["player"].str.lower() == player.lower()) &
        (df["card_name"].str.lower() == card_name.lower()) &
        (df["grade"] == grade)
    ]


def classify_deal(estimated_value, asking_price):
    """
    Classify deal quality.

    Good Deal: asking price is at least 15% below market value
    Fair Price: asking price is within 15% above/below market value
    Overpriced: asking price is more than 15% above market value
    """
    if asking_price <= estimated_value * 0.85:
        return "Good Deal", "Buy"
    elif asking_price <= estimated_value * 1.15:
        return "Fair Price", "Hold / Consider"
    else:
        return "Overpriced", "Avoid"


def main():
    df = load_data()

    print("\n=== AI Resale Market Tracker: Milestone 1 Baseline ===")
    print("\nAvailable sample cards:")
    print(df[["player", "year", "card_name", "grade"]].drop_duplicates().to_string(index=False))

    print("\nEnter an item from the list above.")
    player = input("Player name: ").strip()
    card_name = input("Card name: ").strip()

    try:
        grade = int(input("Grade: ").strip())
        asking_price = float(input("Asking price: $").strip())
    except ValueError:
        print("\nInvalid number entered. Grade must be a whole number and asking price must be numeric.")
        return

    matches = get_matching_sales(df, player, card_name, grade)

    if matches.empty:
        print("\nNo matching sales found for that item.")
        print("Try copying the player/card name exactly from the sample list.")
        return

    # Milestone 1 baseline method: average recent sale prices
    estimated_value = matches["sale_price"].mean()
    difference_percent = ((estimated_value - asking_price) / estimated_value) * 100
    deal_rating, recommendation = classify_deal(estimated_value, asking_price)

    print("\n--- Matching Recent Sales ---")
    print(matches[["sale_date", "site", "sale_price"]].to_string(index=False))

    print("\n--- Resale Tracker Result ---")
    print(f"Estimated Market Value: ${estimated_value:.2f}")
    print(f"Asking Price: ${asking_price:.2f}")
    print(f"Difference From Market: {difference_percent:.2f}%")
    print(f"Deal Rating: {deal_rating}")
    print(f"Recommendation: {recommendation}")


if __name__ == "__main__":
    main()
