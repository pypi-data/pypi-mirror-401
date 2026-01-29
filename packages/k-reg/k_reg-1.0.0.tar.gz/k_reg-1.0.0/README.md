# ⚡ K-Reg (KRegressor)

**The Linear Regression Killer.**
Faster than C-optimized linear algebra. More accurate thanks to non-linearity. Stable on small data.

`KRegressor` is a drop-in replacement for Scikit-Learn's `LinearRegression`.

## 🚀 Benchmark

| Dataset Size | Model | Time | R² Score |
|--------------|-------|------|----------|
| **Small (N=50)** | LinearRegression | 1.0ms | 0.87 |
| | **KRegressor** | **0.5ms** | **0.97** |
| **Huge (N=500k)** | LinearRegression | 380ms | 0.75 |
| | **KRegressor** | **80ms** | **0.92** |

## 📦 Installation

```bash
pip install k-reg