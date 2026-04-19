"""
test_classifier.py — Boilerplate tests for app/classifier.py

Provided as starter code for Block 8 (CI/CD).
Students do not write these tests — they are used to demonstrate
the CI pipeline feedback loop: push → tests run → green or red.

Run with:
    pytest tests/test_classifier.py -v
"""

import numpy as np
import pytest
from app.classifier import classify_batch, classify, CLASSES


class TestClassifyBatch:
    """Tests for the batch inference interface."""

    def test_returns_correct_number_of_results(self):
        """classify_batch with N images returns N result dicts."""
        images = np.zeros((3, 28, 28), dtype=np.uint8)
        results = classify_batch(images)
        assert len(results) == 3

    def test_single_image_batch(self):
        """classify_batch with a single image returns a list of one dict."""
        images = np.zeros((1, 28, 28), dtype=np.uint8)
        results = classify_batch(images)
        assert len(results) == 1

    def test_result_has_required_keys(self):
        """Each result dict must contain prediction, confidence, and scores."""
        images = np.zeros((1, 28, 28), dtype=np.uint8)
        result = classify_batch(images)[0]
        assert "prediction" in result
        assert "confidence" in result
        assert "scores" in result

    def test_prediction_is_valid_class(self):
        """The predicted class must be an element of CLASSES."""
        images = np.random.randint(0, 256, (2, 28, 28), dtype=np.uint8)
        results = classify_batch(images)
        for r in results:
            assert r["prediction"] in CLASSES

    def test_confidence_is_between_0_and_1(self):
        """Confidence must be a float in [0, 1]."""
        images = np.random.randint(0, 256, (2, 28, 28), dtype=np.uint8)
        results = classify_batch(images)
        for r in results:
            assert 0.0 <= r["confidence"] <= 1.0

    def test_scores_keys_match_classes(self):
        """The scores dict keys must match CLASSES exactly."""
        images = np.zeros((1, 28, 28), dtype=np.uint8)
        result = classify_batch(images)[0]
        assert set(result["scores"].keys()) == set(CLASSES)

    def test_scores_sum_to_approximately_one(self):
        """Class probabilities should sum to ~1.0."""
        images = np.random.randint(0, 256, (1, 28, 28), dtype=np.uint8)
        result = classify_batch(images)[0]
        total = sum(result["scores"].values())
        assert abs(total - 1.0) < 1e-5

    def test_rejects_wrong_shape_2d(self):
        """classify_batch must reject a 2D array (missing batch dimension)."""
        with pytest.raises(ValueError, match="Expected"):
            classify_batch(np.zeros((28, 28), dtype=np.uint8))

    def test_rejects_wrong_spatial_shape(self):
        """classify_batch must reject images that are not 28×28."""
        with pytest.raises(ValueError, match="Expected"):
            classify_batch(np.zeros((1, 27, 27), dtype=np.uint8))


class TestClassify:
    """Tests for the single-image convenience wrapper."""

    def test_returns_single_dict(self):
        """classify returns a dict, not a list."""
        image = np.zeros((28, 28), dtype=np.uint8)
        result = classify(image)
        assert isinstance(result, dict)
        assert "prediction" in result

    def test_matches_batch_result(self):
        """classify(img) should return the same result as classify_batch([img])[0]."""
        image = np.random.randint(0, 256, (28, 28), dtype=np.uint8)
        single = classify(image)
        batch = classify_batch(image[np.newaxis])[0]
        assert single["prediction"] == batch["prediction"]
        assert abs(single["confidence"] - batch["confidence"]) < 1e-10
