"""
predict.py — CLI smoke test for the PixelWise classifier

Loads a few MNIST test images, runs them through classify_batch(),
and prints predictions vs. ground truth. This is the script students
write in Block 4 to verify the model works before building the API.

Usage (from project root):
    python predict.py

Requires:
    - MODEL_PATH set in .env (or defaults to models/digit_classifier_v1.pkl)
    - app/classifier.py with classify_batch and classify
    - scikit-learn, numpy, python-dotenv installed
"""

import os
import sys
import numpy as np

# Load .env before importing app modules (they read MODEL_PATH at import time)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv optional if MODEL_PATH is set in shell

from app.classifier import classify_batch, classify, CLASSES


def load_test_samples(n=10):
    """
    Load n MNIST test samples, one per class where possible.

    Returns (images, labels) where images is (n, 28, 28) uint8
    and labels is a list of string labels.
    """
    from sklearn.datasets import fetch_openml

    print("Loading MNIST dataset (cached after first download)...")
    X, y = fetch_openml("mnist_784", version=1, return_X_y=True, as_frame=False)
    y = y.astype(int).astype(str)

    # Pick one sample per class that the model knows about, then fill
    # the rest randomly from known classes
    selected_X = []
    selected_y = []

    for cls in CLASSES:
        idx = np.where(y == cls)[0]
        if len(idx) > 0:
            pick = np.random.RandomState(42).choice(idx)
            selected_X.append(X[pick].reshape(28, 28).astype(np.uint8))
            selected_y.append(cls)

    # If we need more samples, pick randomly from known classes
    known_mask = np.isin(y, CLASSES)
    known_idx = np.where(known_mask)[0]
    remaining = n - len(selected_X)
    if remaining > 0:
        extra = np.random.RandomState(123).choice(known_idx, size=remaining, replace=False)
        for i in extra:
            selected_X.append(X[i].reshape(28, 28).astype(np.uint8))
            selected_y.append(y[i])

    images = np.stack(selected_X[:n])
    labels = selected_y[:n]
    return images, labels


def main():
    print("=" * 60)
    print("PixelWise Smoke Test — predict.py")
    print("=" * 60)

    model_path = os.getenv("MODEL_PATH", "models/digit_classifier_v1.pkl")
    print(f"\nModel path: {model_path}")
    print(f"Classes:    {CLASSES}")
    print()

    # --- Load test samples ---
    images, true_labels = load_test_samples(n=10)
    print(f"Loaded {len(images)} test samples.\n")

    # --- Batch prediction ---
    print("--- Batch prediction (classify_batch) ---")
    results = classify_batch(images)
    correct = 0
    for i, (r, true_label) in enumerate(zip(results, true_labels)):
        match = "OK" if r["prediction"] == true_label else "MISS"
        if r["prediction"] == true_label:
            correct += 1
        print(
            f"  [{i+1:2d}] Predicted: {r['prediction']}  "
            f"(conf: {r['confidence']:.3f})  "
            f"True: {true_label}  [{match}]"
        )
    print(f"\nBatch accuracy: {correct}/{len(results)} = {correct/len(results):.1%}")

    # --- Single prediction (verify classify wrapper) ---
    print("\n--- Single prediction (classify) ---")
    single_result = classify(images[0])
    print(
        f"  Predicted: {single_result['prediction']}  "
        f"(conf: {single_result['confidence']:.3f})  "
        f"True: {true_labels[0]}"
    )

    # --- Verify scores sum to ~1.0 ---
    total = sum(single_result["scores"].values())
    print(f"  Scores sum: {total:.6f} (should be ~1.0)")

    # --- Summary ---
    print("\n" + "=" * 60)
    if correct == len(results):
        print("All predictions correct. Model is ready.")
    else:
        print(f"{correct}/{len(results)} correct. Review misses above.")
    print("=" * 60)


if __name__ == "__main__":
    main()
