"""k_reg.core

K-Reg v2.0.0: v19 non-linear regressor with interaction autopilot.

Key points:
- Automatically selects active features (linear + energy score)
- Adds interaction features (A+B, A-B) for top parents
- Quantized lookup table with bilinear interpolation
- Ridge solver for final assembly
- predict_mode='stream' by default (no X_aug allocation)
"""

import numpy as np
from numba import njit, prange
from sklearn.base import BaseEstimator, RegressorMixin


@njit(fastmath=True, parallel=True, cache=True)
def _jit_fill_bins(X, y_centered, sums, counts, mins, scales):
    n_samples, n_features = X.shape
    n_bins = sums.shape[1]
    for i in prange(n_samples):
        for j in range(n_features):
            pos = (X[i, j] - mins[j]) * scales[j]
            idx = int(pos)

            if idx < 0:
                idx = 0
                d = 0.0
            elif idx >= n_bins - 1:
                idx = n_bins - 2
                d = 1.0
            else:
                d = pos - idx

            sums[j, idx] += y_centered[i] * (1.0 - d)
            counts[j, idx] += (1.0 - d)
            sums[j, idx + 1] += y_centered[i] * d
            counts[j, idx + 1] += d


@njit(fastmath=True, parallel=True, cache=True)
def _jit_transform_matrix(X, table, mins, scales):
    n_samples, n_features = X.shape
    n_bins = table.shape[1]
    P = np.empty((n_samples, n_features), dtype=np.float32)

    for i in prange(n_samples):
        for j in range(n_features):
            pos = (X[i, j] - mins[j]) * scales[j]
            idx = int(pos)

            if idx < 0:
                idx = 0
                d = 0.0
            elif idx >= n_bins - 1:
                idx = n_bins - 2
                d = 1.0
            else:
                d = pos - idx

            P[i, j] = table[j, idx] * (1.0 - d) + table[j, idx + 1] * d
    return P


@njit(fastmath=True, parallel=True, cache=True)
def _jit_expand_dynamic(X, parents, inter_i, inter_j, inter_sign):
    n_samples = X.shape[0]
    n_parents = parents.shape[0]
    n_inter = inter_i.shape[0]
    X_aug = np.empty((n_samples, n_parents + n_inter), dtype=np.float32)

    for r in prange(n_samples):
        for p in range(n_parents):
            X_aug[r, p] = X[r, parents[p]]

        base = n_parents
        for k in range(n_inter):
            a = parents[inter_i[k]]
            b = parents[inter_j[k]]
            X_aug[r, base + k] = X[r, a] + (np.float32(inter_sign[k]) * X[r, b])

    return X_aug


@njit(fastmath=True, parallel=False, cache=True)
def _jit_predict_direct_serial(X, table, mins, scales, coefs):
    n_samples, n_features = X.shape
    n_bins = table.shape[1]
    out = np.empty(n_samples, dtype=np.float32)

    for i in range(n_samples):
        acc = 0.0
        for j in range(n_features):
            pos = (X[i, j] - mins[j]) * scales[j]
            idx = int(pos)
            if idx < 0:
                idx = 0
                d = 0.0
            elif idx >= n_bins - 1:
                idx = n_bins - 2
                d = 1.0
            else:
                d = pos - idx
            val = table[j, idx] * (1.0 - d) + table[j, idx + 1] * d
            acc += val * coefs[j]
        out[i] = acc
    return out


@njit(fastmath=True, parallel=True, cache=True)
def _jit_predict_direct_parallel(X, table, mins, scales, coefs):
    n_samples, n_features = X.shape
    n_bins = table.shape[1]
    out = np.empty(n_samples, dtype=np.float32)

    for i in prange(n_samples):
        acc = 0.0
        for j in range(n_features):
            pos = (X[i, j] - mins[j]) * scales[j]
            idx = int(pos)
            if idx < 0:
                idx = 0
                d = 0.0
            elif idx >= n_bins - 1:
                idx = n_bins - 2
                d = 1.0
            else:
                d = pos - idx
            val = table[j, idx] * (1.0 - d) + table[j, idx + 1] * d
            acc += val * coefs[j]
        out[i] = acc
    return out


@njit(fastmath=True, parallel=False, cache=True)
def _jit_predict_stream_serial(X, table, mins, scales, coefs, parents, inter_i, inter_j, inter_sign):
    n_samples = X.shape[0]
    n_parents = parents.shape[0]
    n_inter = inter_i.shape[0]
    n_bins = table.shape[1]
    out = np.empty(n_samples, dtype=np.float32)

    for r in range(n_samples):
        acc = 0.0

        for p in range(n_parents):
            xval = X[r, parents[p]]
            pos = (xval - mins[p]) * scales[p]
            idx = int(pos)
            if idx < 0:
                idx = 0
                d = 0.0
            elif idx >= n_bins - 1:
                idx = n_bins - 2
                d = 1.0
            else:
                d = pos - idx
            val = table[p, idx] * (1.0 - d) + table[p, idx + 1] * d
            acc += val * coefs[p]

        base = n_parents
        for k in range(n_inter):
            a = parents[inter_i[k]]
            b = parents[inter_j[k]]
            xval = X[r, a] + (np.float32(inter_sign[k]) * X[r, b])

            fidx = base + k
            pos = (xval - mins[fidx]) * scales[fidx]
            idx = int(pos)
            if idx < 0:
                idx = 0
                d = 0.0
            elif idx >= n_bins - 1:
                idx = n_bins - 2
                d = 1.0
            else:
                d = pos - idx
            val = table[fidx, idx] * (1.0 - d) + table[fidx, idx + 1] * d
            acc += val * coefs[fidx]

        out[r] = acc
    return out


@njit(fastmath=True, parallel=True, cache=True)
def _jit_predict_stream_parallel(X, table, mins, scales, coefs, parents, inter_i, inter_j, inter_sign):
    n_samples = X.shape[0]
    n_parents = parents.shape[0]
    n_inter = inter_i.shape[0]
    n_bins = table.shape[1]
    out = np.empty(n_samples, dtype=np.float32)

    for r in prange(n_samples):
        acc = 0.0

        for p in range(n_parents):
            xval = X[r, parents[p]]
            pos = (xval - mins[p]) * scales[p]
            idx = int(pos)
            if idx < 0:
                idx = 0
                d = 0.0
            elif idx >= n_bins - 1:
                idx = n_bins - 2
                d = 1.0
            else:
                d = pos - idx
            val = table[p, idx] * (1.0 - d) + table[p, idx + 1] * d
            acc += val * coefs[p]

        base = n_parents
        for k in range(n_inter):
            a = parents[inter_i[k]]
            b = parents[inter_j[k]]
            xval = X[r, a] + (np.float32(inter_sign[k]) * X[r, b])

            fidx = base + k
            pos = (xval - mins[fidx]) * scales[fidx]
            idx = int(pos)
            if idx < 0:
                idx = 0
                d = 0.0
            elif idx >= n_bins - 1:
                idx = n_bins - 2
                d = 1.0
            else:
                d = pos - idx
            val = table[fidx, idx] * (1.0 - d) + table[fidx, idx + 1] * d
            acc += val * coefs[fidx]

        out[r] = acc
    return out


class KRegressor(BaseEstimator, RegressorMixin):
    def __init__(
        self,
        n_bins=256,
        smoothing=1.0,
        fit_intercept=True,
        sensitivity=0.05,
        max_parents=48,
        lambda_ridge=None,
        predict_mode='stream',
    ):
        self.n_bins = n_bins
        self.smoothing = smoothing
        self.fit_intercept = fit_intercept
        self.sensitivity = sensitivity
        self.max_parents = max_parents
        self.lambda_ridge = lambda_ridge
        self.predict_mode = predict_mode

        self.is_initialized_ = False

    def _auto_select(self, X, y):
        X_cent = X - np.mean(X, axis=0)
        y_cent = y - np.mean(y)

        cov_lin = np.dot(y_cent, X_cent)
        score_lin = np.abs(cov_lin)
        score_lin /= (np.max(score_lin) + 1e-9)

        X_sq = X_cent ** 2
        y_sq = y_cent ** 2
        X_sq -= np.mean(X_sq, axis=0)
        y_sq -= np.mean(y_sq)
        cov_sq = np.dot(y_sq, X_sq)
        score_sq = np.abs(cov_sq)
        score_sq /= (np.max(score_sq) + 1e-9)

        total_score = score_lin + score_sq
        threshold = np.max(total_score) * float(self.sensitivity)
        candidates = np.where(total_score > threshold)[0]

        if len(candidates) > int(self.max_parents):
            scores_candidates = total_score[candidates]
            sorted_idx = np.argsort(scores_candidates)[::-1]
            candidates = candidates[sorted_idx][: int(self.max_parents)]

        return candidates.astype(np.int32)

    def _prepare_mapping(self, X, y):
        parents = self._auto_select(X, y)
        self.parents_ = parents

        if self.lambda_ridge is None:
            self.lambda_ridge_ = 0.01 * (len(parents) / 5.0)
        else:
            self.lambda_ridge_ = float(self.lambda_ridge)

        n_parents = int(parents.shape[0])
        limit_interact = min(n_parents, 16)

        if limit_interact >= 2:
            n_pairs = limit_interact * (limit_interact - 1) // 2
            n_inter = 2 * n_pairs
            inter_i = np.empty(n_inter, dtype=np.int32)
            inter_j = np.empty(n_inter, dtype=np.int32)
            inter_sign = np.empty(n_inter, dtype=np.int8)

            k = 0
            for i in range(limit_interact):
                for j in range(i + 1, limit_interact):
                    inter_i[k] = i
                    inter_j[k] = j
                    inter_sign[k] = 1
                    k += 1
                    inter_i[k] = i
                    inter_j[k] = j
                    inter_sign[k] = -1
                    k += 1
        else:
            inter_i = np.empty(0, dtype=np.int32)
            inter_j = np.empty(0, dtype=np.int32)
            inter_sign = np.empty(0, dtype=np.int8)

        self.inter_i_ = inter_i
        self.inter_j_ = inter_j
        self.inter_sign_ = inter_sign

    def _expand_dynamic(self, X):
        return _jit_expand_dynamic(
            X,
            self.parents_.astype(np.int32),
            self.inter_i_.astype(np.int32),
            self.inter_j_.astype(np.int32),
            self.inter_sign_.astype(np.int8),
        )

    def fit(self, X, y):
        X = np.asarray(X, dtype=np.float32, order='C')
        y = np.asarray(y, dtype=np.float32)

        n_samples = int(X.shape[0])
        if isinstance(self.n_bins, str) and self.n_bins == 'auto':
            if n_samples < 50_000:
                self.n_bins_ = 64
            elif n_samples < 500_000:
                self.n_bins_ = 128
            else:
                self.n_bins_ = 256
        else:
            self.n_bins_ = int(self.n_bins)

        if self.fit_intercept:
            self.mu_y_ = np.float32(np.mean(y))
        else:
            self.mu_y_ = np.float32(0.0)
        y_cent = y - self.mu_y_

        self._prepare_mapping(X, y)
        X_aug = self._expand_dynamic(X)

        self.mins_ = (np.min(X_aug, axis=0).astype(np.float32) - 0.05)
        self.maxs_ = (np.max(X_aug, axis=0).astype(np.float32) + 0.05)
        self.scales_ = (self.n_bins_ - 1) / (self.maxs_ - self.mins_ + 1e-9)

        n_aug = int(X_aug.shape[1])
        raw_sums = np.zeros((n_aug, self.n_bins_), dtype=np.float32)
        raw_counts = np.zeros((n_aug, self.n_bins_), dtype=np.float32)
        _jit_fill_bins(X_aug, y_cent, raw_sums, raw_counts, self.mins_, self.scales_)

        self.table_ = raw_sums / (raw_counts + float(self.smoothing))

        P = _jit_transform_matrix(X_aug, self.table_, self.mins_, self.scales_)
        reg = (P.T @ P) + (np.eye(P.shape[1], dtype=np.float32) * np.float32(self.lambda_ridge_))
        tgt = (P.T @ y_cent)
        self.coefs_ = np.linalg.solve(reg, tgt).astype(np.float32)

        self.is_initialized_ = True
        return self

    def predict(self, X):
        X = np.asarray(X, dtype=np.float32, order='C')
        if not self.is_initialized_:
            return np.zeros(X.shape[0], dtype=np.float32)

        if self.predict_mode == 'x_aug':
            X_aug = self._expand_dynamic(X)
            if X_aug.shape[0] < 1000:
                raw = _jit_predict_direct_serial(X_aug, self.table_, self.mins_, self.scales_, self.coefs_)
            else:
                raw = _jit_predict_direct_parallel(X_aug, self.table_, self.mins_, self.scales_, self.coefs_)
            return self.mu_y_ + raw

        parents = self.parents_.astype(np.int32)
        inter_i = self.inter_i_.astype(np.int32)
        inter_j = self.inter_j_.astype(np.int32)
        inter_sign = self.inter_sign_.astype(np.int8)

        if X.shape[0] < 1000:
            raw = _jit_predict_stream_serial(X, self.table_, self.mins_, self.scales_, self.coefs_, parents, inter_i, inter_j, inter_sign)
        else:
            raw = _jit_predict_stream_parallel(X, self.table_, self.mins_, self.scales_, self.coefs_, parents, inter_i, inter_j, inter_sign)

        return self.mu_y_ + raw