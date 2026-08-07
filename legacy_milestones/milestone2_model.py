import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

DATA_FILE = "resale_data.csv"

df = pd.read_csv(DATA_FILE)

# Create estimated market value for each card/grade group
df["estimated_market_value"] = df.groupby(["player", "card_name", "grade"])["sale_price"].transform("mean")

# Simulate asking prices around market value for training
training_rows = []

for _, row in df.iterrows():
    market_value = row["estimated_market_value"]

    examples = [
        (market_value * 0.80, "Good Deal"),
        (market_value * 1.00, "Fair Price"),
        (market_value * 1.20, "Overpriced"),
    ]

    for asking_price, label in examples:
        difference_percent = ((market_value - asking_price) / market_value) * 100

        training_rows.append({
            "grade": row["grade"],
            "asking_price": asking_price,
            "estimated_market_value": market_value,
            "difference_percent": difference_percent,
            "deal_label": label
        })

training_df = pd.DataFrame(training_rows)

X = training_df[["grade", "asking_price", "estimated_market_value", "difference_percent"]]
y = training_df["deal_label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("=== Milestone 2 ML Classification Model ===")
print(f"Training examples: {len(training_df)}")
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nExample Prediction:")
example = pd.DataFrame([{
    "grade": 9,
    "asking_price": 190,
    "estimated_market_value": 225,
    "difference_percent": ((225 - 190) / 225) * 100
}])

prediction = model.predict(example)[0]
print(example.to_string(index=False))
print(f"Predicted Deal Label: {prediction}")