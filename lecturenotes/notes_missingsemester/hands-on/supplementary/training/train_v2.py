"""
train_v2.py — Train digit_classifier_v2.pkl

Trains a LogisticRegression pipeline on ALL MNIST digits 0–9 (10 classes).
This is the "optional challenge" model from Block 4, deployed via the
Block 8 feature flag.

Usage:
    python train_v2.py

Output:
    models/digit_classifier_v2.pkl
    Prints per-class accuracy on the test set.

Requirements:
    pip install scikit-learn joblib
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
    print("PixelWise Model Training — v2 (digits 0–9)")
    print("=" * 60)

    # --- 1. Load MNIST ---
    print("\n[1/4] Loading MNIST dataset...")
    X, y = fetch_openml("mnist_784", version=1, return_X_y=True, as_frame=False)
    y_str = y.astype(int).astype(str)
    classes = sorted(np.unique(y_str))
    print(f"      Loaded {len(X)} samples, classes: {classes}")

    # --- 2. Train/test split ---
    print("[2/4] Splitting into train/test (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_str, test_size=0.2, random_state=42, stratify=y_str
    )
    print(f"      Train: {len(X_train)}, Test: {len(X_test)}")

    # --- 3. Build and train pipeline ---
    print("[3/4] Training LogisticRegression pipeline...")
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

    # --- 4. Evaluate ---
    print("[4/4] Evaluating on test set...\n")
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Overall accuracy: {acc:.4f}\n")
    print(classification_report(y_test, y_pred, digits=3))

    # Verify classes match expected CLASSES constant for v2
    expected_classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    assert list(pipeline.classes_) == expected_classes, (
        f"Classes mismatch: {list(pipeline.classes_)} != {expected_classes}"
    )
    print(f"Model classes: {list(pipeline.classes_)}")

    # --- Save ---
    output_dir = "models"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "digit_classifier_v2.pkl")
    joblib.dump(pipeline, output_path)
    print(f"\nModel saved to: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.0f} KB")

    # --- Compare with v1 if available ---
    v1_path = os.path.join(output_dir, "digit_classifier_v1.pkl")
    if os.path.exists(v1_path):
        print("\n--- Comparison with v1 ---")
        v1 = joblib.load(v1_path)
        print(f"v1 classes: {list(v1.classes_)}")
        print(f"v2 classes: {list(pipeline.classes_)}")
        # Evaluate v1 on v2's test set (only on digits 1-9)
        mask_19 = np.isin(y_test, [str(d) for d in range(1, 10)])
        if mask_19.any():
            v1_acc = accuracy_score(y_test[mask_19], v1.predict(X_test[mask_19]))
            v2_acc = accuracy_score(y_test[mask_19], pipeline.predict(X_test[mask_19]))
            print(f"v1 accuracy (digits 1-9 only): {v1_acc:.4f}")
            print(f"v2 accuracy (digits 1-9 only): {v2_acc:.4f}")


if __name__ == "__main__":
    main()
