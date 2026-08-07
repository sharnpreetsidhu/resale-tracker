import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "resale_data.csv"

df = pd.read_csv(DATA_FILE)

print("Available sample cards:")
print(df[["player", "year", "card_name", "grade"]].drop_duplicates().to_string(index=False))

player = input("\nPlayer name: ").strip()
card_name = input("Card name: ").strip()
grade = int(input("Grade: ").strip())

matches = df[
    (df["player"].str.lower() == player.lower()) &
    (df["card_name"].str.lower() == card_name.lower()) &
    (df["grade"] == grade)
].copy()

if matches.empty:
    print("No matching sales found.")
else:
    matches["sale_date"] = pd.to_datetime(matches["sale_date"])
    matches = matches.sort_values("sale_date")

    estimated_value = matches["sale_price"].mean()

    print("\nMatching sales:")
    print(matches[["sale_date", "site", "sale_price"]].to_string(index=False))
    print(f"\nEstimated Market Value: ${estimated_value:.2f}")

    plt.figure()
    plt.plot(matches["sale_date"], matches["sale_price"], marker="o")
    plt.axhline(estimated_value, linestyle="--", label=f"Average: ${estimated_value:.2f}")
    plt.title(f"{player} - {card_name} Grade {grade} Recent Sales")
    plt.xlabel("Sale Date")
    plt.ylabel("Sale Price")
    plt.legend()
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()