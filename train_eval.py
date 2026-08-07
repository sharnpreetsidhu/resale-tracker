from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.config import DATA_FILE, OUTPUT_DIR
from src.data_loader import load_resale_data
from src.modeling import train_and_compare_models


def save_confusion_matrix(cm: np.ndarray, labels: list[str], output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    image = ax.imshow(cm)
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_yticklabels(labels)
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("Actual label")
    ax.set_title("Best Model Confusion Matrix")

    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, cm[i, j], ha="center", va="center", color="white" if cm[i, j] > cm.max() / 2 else "black")

    fig.colorbar(image, ax=ax)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_resale_data(DATA_FILE)
    results = train_and_compare_models(df)

    print("=== AI Resale Market Tracker: Final Model Evaluation ===")
    print(f"Dataset rows: {len(df):,}")
    print(f"Training examples: {len(results['training_df']):,}")
    print(f"Feature columns: {', '.join(results['feature_columns'])}")
    print("\nModel comparison:")
    for name, score in results["scores"].items():
        print(f"- {name}: {score * 100:.2f}% accuracy")

    print(f"\nBest model: {results['best_name']}")
    print("\nClassification report for best model:")
    print(results["reports"][results["best_name"]])

    matrix_path = OUTPUT_DIR / "confusion_matrix.png"
    save_confusion_matrix(results["confusion_matrix"], results["labels"], matrix_path)
    print(f"Saved confusion matrix to: {matrix_path}")
