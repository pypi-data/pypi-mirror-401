"""
KRegressor: A High-Performance Additive Quantized Regressor.
Compatible with scikit-learn API.
"""
import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from numba import njit, prange

# --- MOTEUR JIT (Monolithique pour réduire l'overhead Python) ---
@njit(fastmath=True, parallel=True, cache=True)
def _fast_fit_numba(X, y, n_bins, n_features, n_samples):
    bin_sums = np.zeros((n_features, n_bins), dtype=np.float32)
    bin_counts = np.zeros((n_features, n_bins), dtype=np.float32)
    
    mins = np.zeros(n_features, dtype=np.float32)
    maxs = np.zeros(n_features, dtype=np.float32)
    
    # 1. Min/Max Calculation (Inside JIT to avoid Numpy overhead on small data)
    for j in range(n_features):
        mins[j] = X[0, j]
        maxs[j] = X[0, j]
        
    for i in range(n_samples):
        for j in range(n_features):
            val = X[i, j]
            if val < mins[j]: mins[j] = val
            if val > maxs[j]: maxs[j] = val
            
    # 2. Scales
    scales = np.empty(n_features, dtype=np.float32)
    for j in range(n_features):
        rng = maxs[j] - mins[j]
        if rng < 1e-9: rng = 1.0
        scales[j] = (n_bins - 1) / rng

    # 3. Histogramming
    for i in prange(n_samples):
        for j in range(n_features):
            bin_idx = int((X[i, j] - mins[j]) * scales[j])
            if bin_idx < 0: bin_idx = 0
            elif bin_idx >= n_bins: bin_idx = n_bins - 1
            
            bin_sums[j, bin_idx] += y[i]
            bin_counts[j, bin_idx] += 1
            
    return bin_sums, bin_counts, mins, scales

@njit(fastmath=True, parallel=True, cache=True)
def _fast_calibration_stats(X, y_centered, lookup_table, mins, scales):
    n_samples, n_features = X.shape
    n_bins = lookup_table.shape[1]
    
    numerator = 0.0
    denominator = 0.0
    
    for i in prange(n_samples):
        local_pred = 0.0
        for j in range(n_features):
            bin_idx = int((X[i, j] - mins[j]) * scales[j])
            if bin_idx < 0: bin_idx = 0
            elif bin_idx >= n_bins: bin_idx = n_bins - 1
            local_pred += lookup_table[j, bin_idx]
            
        numerator += y_centered[i] * local_pred
        denominator += local_pred * local_pred
        
    return numerator, denominator

@njit(fastmath=True, parallel=False, cache=True)
def _fast_predict_raw_serial(X, lookup_table, mins, scales, n_samples, n_features):
    predictions = np.zeros(n_samples, dtype=np.float32)
    n_bins = lookup_table.shape[1]
    for i in range(n_samples):
        local_sum = 0.0
        for j in range(n_features):
            bin_idx = int((X[i, j] - mins[j]) * scales[j])
            if bin_idx < 0: bin_idx = 0
            elif bin_idx >= n_bins: bin_idx = n_bins - 1
            local_sum += lookup_table[j, bin_idx]
        predictions[i] = local_sum
    return predictions

@njit(fastmath=True, parallel=True, cache=True)
def _fast_predict_raw(X, lookup_table, mins, scales, n_samples, n_features):
    predictions = np.zeros(n_samples, dtype=np.float32)
    n_bins = lookup_table.shape[1]
    for i in prange(n_samples):
        local_sum = 0.0
        for j in range(n_features):
            bin_idx = int((X[i, j] - mins[j]) * scales[j])
            if bin_idx < 0: bin_idx = 0
            elif bin_idx >= n_bins: bin_idx = n_bins - 1
            local_sum += lookup_table[j, bin_idx]
        predictions[i] = local_sum
    return predictions

class KRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, n_bins='auto', smoothing=1.0, fit_intercept=True):
        self.n_bins = n_bins
        self.smoothing = smoothing
        self.fit_intercept = fit_intercept
        self.lookup_table_ = None
        self.mins_ = None
        self.scales_ = None
        self.global_mean_ = 0.0
        self.calibrator_ = 1.0
        
    def fit(self, X, y):
        X = np.asarray(X, dtype=np.float32, order='C')
        y = np.asarray(y, dtype=np.float32)
        
        n_samples, n_features = X.shape
        
        # Automatic Parameter Selection
        if self.n_bins == 'auto':
            if n_samples < 10000:
                effective_n_bins = 16
            elif n_samples < 100000:
                effective_n_bins = 32
            else:
                effective_n_bins = 64
        else:
            effective_n_bins = int(self.n_bins)
        
        if self.fit_intercept:
            self.global_mean_ = np.mean(y)
        else:
            self.global_mean_ = 0.0
            
        y_centered = y - self.global_mean_
        
        # 1. Fast Histogramming & Scale Calc (Single JIT Call)
        # This reduces Python overhead for small datasets compared to numpy calls
        sums, counts, self.mins_, self.scales_ = _fast_fit_numba(
            X, y_centered, effective_n_bins, n_features, n_samples
        )
        
        # 2. Bayesian Smoothing
        with np.errstate(divide='ignore', invalid='ignore'):
            self.lookup_table_ = sums / (counts + self.smoothing)
        self.lookup_table_ = np.nan_to_num(self.lookup_table_)
        
        # 3. Calibration (Fused Kernel)
        num, den = _fast_calibration_stats(
            X, y_centered, self.lookup_table_, self.mins_, self.scales_
        )
        
        if den == 0:
            self.calibrator_ = 0.0
        else:
            self.calibrator_ = num / den
            
        return self
    
    def predict(self, X):
        X = np.asarray(X, dtype=np.float32, order='C')
        n_samples, n_features = X.shape
        
        if n_samples < 1000:
            raw_preds = _fast_predict_raw_serial(
                X, self.lookup_table_, self.mins_, self.scales_, n_samples, n_features
            )
        else:
            raw_preds = _fast_predict_raw(
                X, self.lookup_table_, self.mins_, self.scales_, n_samples, n_features
            )
        
        return self.global_mean_ + (raw_preds * self.calibrator_)