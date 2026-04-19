"""
train.py — Train digit_classifier_v1.pkl

Trains a LogisticRegression pipeline on MNIST digits 1–9 (class 0 intentionally excluded).
Produces: digit_classifier_v1.pkl

Usage:
    python train.py

Output:
    models/digit_classifier_v1.pkl
    Prints per-class accuracy on the test set.

Requirements:
    pip install scikit-learn joblib

Notes:
    - MNIST downloads automatically (~50 MB on first run)
    - Training takes ~30 seconds on CPU
    - Class 0 is withheld so students can add it in the optional v2 challenge
"""

import os
import numpy as np
import joblib
from sklearn.datasets import fetch_openml
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score


def binarize(X):
    """Binarize pixel values: > 128 → 1.0, else → 0.0"""
    return (X > 128).astype(np.float64)


def main():
    print("=" * 60)
    print("PixelWise Model Training — v1 (digits 1–9)")
    print("=" * 60)

    # --- 1. Load MNIST ---
    print("\n[1/5] Loading MNIST dataset...")
    X, y = fetch_openml("mnist_784", version=1, return_X_y=True, as_frame=False)
    y = y.astype(int)
    print(f"      Loaded {len(X)} samples, {len(np.unique(y))} classes")

    # --- 2. Filter out class 0 ---
    print("[2/5] Filtering out class 0 (withheld for v2)...")
    mask = y != 0
    X = X[mask]
    y = y[mask]

    # Remap labels to strings matching CLASSES constant
    y_str = y.astype(str)
    classes = sorted(np.unique(y_str))
    print(f"      Remaining: {len(X)} samples, classes: {classes}")

    # --- 3. Train/test split ---
    print("[3/5] Splitting into train/test (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_str, test_size=0.2, random_state=42, stratify=y_str
    )
    print(f"      Train: {len(X_train)}, Test: {len(X_test)}")

    # --- 4. Build and train pipeline ---
    print("[4/5] Training LogisticRegression pipeline...")
    pipeline = Pipeline([
        ("binarize", FunctionTransformer(binarize)),
        ("clf", LogisticRegression(
            max_iter=300,
            solver="lbfgs",
            multi_class="multinomial",
            random_state=42,
            n_jobs=-1,
        )),
    ])
    pipeline.fit(X_train, y_train)
    print("      Training complete.")

    # --- 5. Evaluate ---
    print("[5/5] Evaluating on test set...\n")
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Overall accuracy: {acc:.4f}\n")
    print(classification_report(y_test, y_pred, digits=3))

    # Verify classes match expected CLASSES constant
    expected_classes = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    assert list(pipeline.classes_) == expected_classes, (
        f"Classes mismatch: {list(pipeline.classes_)} != {expected_classes}"
    )
    print(f"Model classes: {list(pipeline.classes_)}")

    # --- Save ---
    output_dir = "models"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "digit_classifier_v1.pkl")
    joblib.dump(pipeline, output_path)
    print(f"\nModel saved to: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
