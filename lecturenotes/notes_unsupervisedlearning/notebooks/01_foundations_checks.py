"""Auto-checker helpers for Chapter 1 notebook."""

import numpy as np

_OK = "\u2705"
_FAIL = "\u274c"
_NONE = "\u2b1c"
_TOL = 0.01


def _close(a, b, tol=_TOL):
    try:
        return abs(float(a) - float(b)) < tol
    except (TypeError, ValueError):
        return False


# ---------------------------------------------------------------------------
# Euclidean
# ---------------------------------------------------------------------------

def check_euclidean(fn, x, y):
    got = fn(x, y)
    expected = np.sqrt(np.sum((x - y) ** 2))

    if got is None:
        print(f"  {_NONE} Euclidean: not implemented yet (expected {expected:.4f})")
        return

    if _close(got, expected):
        print(f"  {_OK} Euclidean d = {got:.4f}")
        return

    no_sqrt = np.sum((x - y) ** 2)
    manhattan = np.sum(np.abs(x - y))

    if _close(got, no_sqrt):
        print(f"  {_FAIL} Euclidean d = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: that is the squared distance. Don't forget np.sqrt().")
    elif _close(got, manhattan):
        print(f"  {_FAIL} Euclidean d = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: that is the Manhattan distance. You need to square the")
        print(f"       differences, not take the absolute value.")
    elif _close(got, -expected):
        print(f"  {_FAIL} Euclidean d = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: the sign is flipped. Distance should be non-negative.")
    else:
        print(f"  {_FAIL} Euclidean d = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: revisit the formula. The steps are: subtract, square, sum, root.")


# ---------------------------------------------------------------------------
# Manhattan
# ---------------------------------------------------------------------------

def check_manhattan(fn, x, y):
    got = fn(x, y)
    expected = np.sum(np.abs(x - y))

    if got is None:
        print(f"  {_NONE} Manhattan: not implemented yet (expected {expected:.4f})")
        return

    if _close(got, expected):
        print(f"  {_OK} Manhattan d = {got:.4f}")
        return

    euclidean = np.sqrt(np.sum((x - y) ** 2))
    no_abs = np.sum(x - y)
    squared_sum = np.sum((x - y) ** 2)

    if _close(got, euclidean):
        print(f"  {_FAIL} Manhattan d = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: that is the Euclidean distance. For Manhattan, use absolute")
        print(f"       values instead of squaring, and no square root at the end.")
    elif _close(got, no_abs):
        print(f"  {_FAIL} Manhattan d = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: differences can be negative. Wrap them in np.abs().")
    elif _close(got, squared_sum):
        print(f"  {_FAIL} Manhattan d = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: you are squaring the differences. Manhattan uses absolute")
        print(f"       values, not squares.")
    else:
        print(f"  {_FAIL} Manhattan d = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: revisit the formula. The steps are: subtract, abs, sum.")


# ---------------------------------------------------------------------------
# Cosine
# ---------------------------------------------------------------------------

def check_cosine_sim(fn, x, y):
    got = fn(x, y)
    expected = np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))

    if got is None:
        print(f"  {_NONE} Cosine similarity: not implemented yet (expected {expected:.4f})")
        return

    if _close(got, expected):
        print(f"  {_OK} Cosine similarity = {got:.4f}")
        return

    raw_dot = float(np.dot(x, y))
    distance = 1 - expected

    if _close(got, raw_dot):
        print(f"  {_FAIL} Cosine similarity = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: that is the raw dot product. You need to divide by the")
        print(f"       product of the two vector norms to normalize it.")
    elif _close(got, distance):
        print(f"  {_FAIL} Cosine similarity = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: that is the cosine distance (1 - similarity).")
        print(f"       This function should return the similarity, not the distance.")
    elif got is not None and (float(got) > 1.0 or float(got) < -1.0):
        print(f"  {_FAIL} Cosine similarity = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: cosine similarity should be between -1 and +1.")
        print(f"       Check that you are dividing by both norms.")
    else:
        print(f"  {_FAIL} Cosine similarity = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: numerator = dot product, denominator = norm(x) * norm(y).")


def check_cosine_dist(fn, x, y):
    got = fn(x, y)
    sim = np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
    expected = 1.0 - sim

    if got is None:
        print(f"  {_NONE} Cosine distance: not implemented yet (expected {expected:.4f})")
        return

    if _close(got, expected):
        print(f"  {_OK} Cosine distance = {got:.4f}")
        return

    if _close(got, sim):
        print(f"  {_FAIL} Cosine distance = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: that is the similarity, not the distance.")
        print(f"       Cosine distance = 1 - similarity.")
    else:
        print(f"  {_FAIL} Cosine distance = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: cosine distance = 1 - cosine_similarity(x, y).")


# ---------------------------------------------------------------------------
# Mahalanobis
# ---------------------------------------------------------------------------

def check_mahalanobis(fn, x, y, cov):
    got = fn(x, y, cov)
    delta = x - y
    cov_inv = np.linalg.inv(cov)
    expected = np.sqrt(delta @ cov_inv @ delta)

    if got is None:
        print(f"  {_NONE} Mahalanobis: not implemented yet (expected {expected:.4f})")
        return

    if _close(got, expected):
        print(f"  {_OK} Mahalanobis d = {got:.4f}")
        return

    squared = delta @ cov_inv @ delta
    euclidean = np.sqrt(np.sum(delta ** 2))
    no_inv = np.sqrt(delta @ cov @ delta)

    if _close(got, squared):
        print(f"  {_FAIL} Mahalanobis d = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: that is the squared Mahalanobis distance.")
        print(f"       Don't forget to take the square root at the end.")
    elif _close(got, euclidean):
        print(f"  {_FAIL} Mahalanobis d = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: that is the Euclidean distance. You need to transform the")
        print(f"       difference vector through the inverse covariance matrix.")
    elif _close(got, no_inv):
        print(f"  {_FAIL} Mahalanobis d = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: you are using the covariance matrix directly. You need its")
        print(f"       inverse: np.linalg.inv(cov).")
    else:
        print(f"  {_FAIL} Mahalanobis d = {got:.4f}  (expected {expected:.4f})")
        print(f"       Hint: the steps are: delta = x - y, invert cov, then")
        print(f"       sqrt(delta @ cov_inv @ delta).")


# ---------------------------------------------------------------------------
# Z-score normalization
# ---------------------------------------------------------------------------

def check_zscore(result, data):
    if result is None:
        print(f"  {_NONE} Z-score: not implemented yet")
        return

    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    expected = (data - mu) / sigma

    if np.allclose(result, expected, atol=_TOL):
        print(f"  {_OK} Z-score normalization correct (mean\u22480, std\u22481)")
        return

    # show what the first row should look like for reference
    ref = f"expected row 0: [{expected[0,0]:.3f}, {expected[0,1]:.3f}, {expected[0,2]:.3f}]"

    centered = data - mu
    if np.allclose(result, centered, atol=_TOL):
        print(f"  {_FAIL} You subtracted the mean but forgot to divide by the")
        print(f"       standard deviation. ({ref})")
        return

    scaled = data / sigma
    if np.allclose(result, scaled, atol=_TOL):
        print(f"  {_FAIL} You divided by the standard deviation but forgot to")
        print(f"       subtract the mean first. ({ref})")
        return

    by_var = (data - mu) / (sigma ** 2)
    if np.allclose(result, by_var, atol=_TOL):
        print(f"  {_FAIL} You divided by the variance instead of the standard deviation.")
        print(f"       Use np.std(), not np.var(). ({ref})")
        return

    means = result.mean(axis=0)
    stds = result.std(axis=0)

    if not np.allclose(means, 0, atol=_TOL):
        print(f"  {_FAIL} Column means are {means.round(4)}, expected ~0.")
        print(f"       Hint: subtract np.mean(data, axis=0) before dividing. ({ref})")
    elif not np.allclose(stds, 1, atol=_TOL):
        print(f"  {_FAIL} Column stds are {stds.round(4)}, expected ~1.")
        print(f"       Hint: divide by np.std(data, axis=0). ({ref})")
    else:
        print(f"  {_FAIL} Values don't match expected output.")
        print(f"       Hint: z = (data - mean) / std, applied per column (axis=0). ({ref})")


# ---------------------------------------------------------------------------
# Min-max normalization
# ---------------------------------------------------------------------------

def check_minmax(result, data):
    if result is None:
        print(f"  {_NONE} Min-max: not implemented yet")
        return

    dmin = np.min(data, axis=0)
    dmax = np.max(data, axis=0)
    expected = (data - dmin) / (dmax - dmin)

    if np.allclose(result, expected, atol=_TOL):
        print(f"  {_OK} Min-max scaling correct (min\u22480, max\u22481)")
        return

    ref = f"expected row 0: [{expected[0,0]:.3f}, {expected[0,1]:.3f}, {expected[0,2]:.3f}]"

    no_shift = data / (dmax - dmin)
    if np.allclose(result, no_shift, atol=_TOL):
        print(f"  {_FAIL} You divided by the range but forgot to subtract the minimum.")
        print(f"       ({ref})")
        return

    by_max = (data - dmin) / dmax
    if np.allclose(result, by_max, atol=_TOL):
        print(f"  {_FAIL} You divided by the max instead of the range (max - min).")
        print(f"       ({ref})")
        return

    by_max_only = data / dmax
    if np.allclose(result, by_max_only, atol=_TOL):
        print(f"  {_FAIL} You divided by max without subtracting min.")
        print(f"       The formula is (x - min) / (max - min). ({ref})")
        return

    mins = result.min(axis=0)
    maxs = result.max(axis=0)

    if not np.allclose(mins, 0, atol=_TOL):
        print(f"  {_FAIL} Column mins are {mins.round(4)}, expected ~0.")
        print(f"       Hint: subtract np.min(data, axis=0) in the numerator. ({ref})")
    elif not np.allclose(maxs, 1, atol=_TOL):
        print(f"  {_FAIL} Column maxs are {maxs.round(4)}, expected ~1.")
        print(f"       Hint: divide by (max - min), not just max. ({ref})")
    else:
        print(f"  {_FAIL} Values don't match expected output.")
        print(f"       Hint: (data - min) / (max - min), per column (axis=0). ({ref})")
