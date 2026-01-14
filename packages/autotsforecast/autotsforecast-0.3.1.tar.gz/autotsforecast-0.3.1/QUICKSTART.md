# AutoTSForecast Quick Reference

## Installation

```bash
# Basic installation
pip install autotsforecast

# With all features including v0.3.0 additions
pip install "autotsforecast[all]"
```

## What's New in v0.3.0

| Feature | Description | Example |
|---------|-------------|---------|
| **Prediction Intervals** | Conformal prediction | `PredictionIntervals(method='conformal')` |
| **Calendar Features** | Time-based feature extraction | `CalendarFeatures(cyclical_encoding=True)` |
| **Visualization** | Static & interactive plots | `plot_forecast()`, `plot_forecast_interactive()` |
| **Parallel Processing** | Multi-series speedup | `ParallelForecaster(n_jobs=4)` |
| **Progress Tracking** | Rich progress bars | `ProgressTracker.track(items)` |

## Basic Usage

### 1. Simple Multivariate Forecasting

```python
from autotsforecast import MovingAverageForecaster
import pandas as pd

# Your data: DataFrame with multiple columns (multivariate)
df = pd.DataFrame({
    'North': [...],
    'South': [...],
    'East': [...]
}, index=pd.date_range('2023-01-01', periods=200, freq='D'))

# Split data
y_train, y_test = df.iloc[:150], df.iloc[150:]

# Create and fit model
model = MovingAverageForecaster(horizon=30, window=7)
model.fit(y_train)

# Predict
predictions = model.predict()
```

### 2. AutoForecaster (Automatic Model Selection)

```python
from autotsforecast import (
    AutoForecaster,
    MovingAverageForecaster,
    VARForecaster,
    RandomForestForecaster,
    XGBoostForecaster
)

# Define candidate models
candidate_models = [
    MovingAverageForecaster(horizon=30, window=7),
    VARForecaster(horizon=30, lags=7),
    RandomForestForecaster(horizon=30, n_estimators=100),
    XGBoostForecaster(horizon=30, n_estimators=100)
]

# Automatic selection via backtesting
auto = AutoForecaster(
    candidate_models=candidate_models,
    metric='rmse',
    n_splits=3,
    test_size=10
)

auto.fit(y_train)
forecasts = auto.forecast()

print(f"Best model: {auto.best_model_name_}")
```

### 3. Using Covariates (External Features)

```python
# Covariates with categorical and numerical features
X = pd.DataFrame({
    'day_name': dates.day_name(),  # CATEGORICAL
    'temperature': [...],           # NUMERICAL
    'is_weekend': [...]             # NUMERICAL
}, index=dates)

# Split covariates
X_train, X_test = X.iloc[:150], X.iloc[150:]

# Fit with covariates (automatic preprocessing)
model = RandomForestForecaster(horizon=50)
model.fit(y_train, X_train)

# Predict with future covariates
predictions = model.predict(X_test)
```

### 3.1 Per-Series Covariates (Different Features per Series)

When different series are driven by different factors:

```python
from autotsforecast import AutoForecaster
from autotsforecast.models.external import RandomForestForecaster, ProphetForecaster

# Product A: Weather-sensitive (uses temperature, advertising)
# Product B: Price-sensitive (uses competitor price, promotions)

X_train_dict = {
    'product_a_sales': pd.DataFrame({
        'temperature': [...],
        'advertising_spend': [...]
    }, index=dates_train),
    'product_b_sales': pd.DataFrame({
        'competitor_price': [...],
        'promotion_active': [...]
    }, index=dates_train)
}

X_test_dict = {
    'product_a_sales': X_product_a_test,
    'product_b_sales': X_product_b_test
}

# AutoForecaster with per-series covariates
auto = AutoForecaster(
    candidate_models=[
        RandomForestForecaster(horizon=14, n_lags=7),
        ProphetForecaster(horizon=14)
    ],
    per_series_models=True,
    metric='rmse'
)

# Each series uses its own covariates
auto.fit(y_train, X=X_train_dict)
forecasts = auto.forecast(X=X_test_dict)

print(auto.best_model_names_)  # e.g., {'product_a_sales': 'RandomForest', 'product_b_sales': 'Prophet'}
```

**Key Benefits:**
- ✅ Each series uses only relevant features
- ✅ Reduces noise from irrelevant covariates
- ✅ Handles heterogeneous product portfolios
- ✅ Backward compatible with single DataFrame

## Advanced Features

### 4. Standalone Backtesting (Independent Feature)

BacktestValidator works with ANY forecasting model independently:

```python
from autotsforecast.backtesting import BacktestValidator
from autotsforecast import RandomForestForecaster

# Create any forecasting model
model = RandomForestForecaster(horizon=14, n_lags=7)

# Create backtesting validator
validator = BacktestValidator(
    model=model,
    n_splits=5,           # 5 cross-validation folds
    test_size=14,         # 14-day test windows
    window_type='expanding'  # or 'rolling'
)

# Run backtesting
metrics = validator.run(y_train, X_train)
print(f"Overall RMSE: {metrics['rmse']:.2f}")
print(f"Overall MAPE: {metrics['mape']:.2f}%")
print(f"Overall R²: {metrics['r2']:.4f}")

# Get detailed fold-by-fold results
fold_results = validator.get_fold_results()
print(fold_results[['fold', 'train_size', 'test_size', 'rmse', 'mape']])

# Get summary statistics (mean, std, min, max)
summary = validator.get_summary()
print(summary)

# Visualize results automatically
validator.plot_results()

# Extract predictions for custom analysis
actuals, predictions = validator.get_predictions()
errors = actuals - predictions
```

### 5. Hierarchical Reconciliation

For time series with hierarchical structure (e.g., Total = Region1 + Region2):

```python
from autotsforecast.hierarchical import HierarchicalReconciler

# Get base forecasts for all levels
base_forecasts = pd.DataFrame({
    'Total': [...],
    'North': [...],
    'South': [...],
    'East': [...]
})

# Define hierarchy
hierarchy = {
    'Total': ['North', 'South', 'East']
}

# Create reconciler
reconciler = HierarchicalReconciler(base_forecasts, hierarchy)

# Reconcile using different methods
reconciled_bu = reconciler.reconcile(method='bottom_up')
reconciled_ols = reconciler.reconcile(method='ols')

print("Reconciliation methods:")
print("- bottom_up: Aggregate from lowest level (keeps bottom forecasts)")
print("- top_down: Disaggregate from highest level using proportions")
print("- ols: OLS optimal reconciliation (minimizes total squared error)")
```

### 6. SHAP Model Interpretability

Explain model predictions using SHAP values:

```python
from autotsforecast.interpretability import DriverAnalyzer

# Fit a model first
model = XGBoostForecaster(horizon=30)
model.fit(y_train, X_train)

# Create analyzer
analyzer = DriverAnalyzer(model, feature_names=X_train.columns.tolist())

# Calculate SHAP values (requires both X and y for lag reconstruction)
shap_values = analyzer.calculate_shap_values(
    X_train,
    y_train,
    max_samples=100
)

# Get SHAP feature importance
shap_importance = analyzer.get_shap_feature_importance(shap_values)
print(shap_importance)

# Visualize SHAP summary plot
import shap
import matplotlib.pyplot as plt

# Extract values for a specific series
shap_array = shap_values['North']  # or target name
shap.summary_plot(shap_array, X_train[['temperature', 'promotion']], plot_type='bar')
```
```

### 7. Traditional Feature Importance

For comparison with SHAP:

```python
# Coefficient-based (linear models only)
importance = analyzer.calculate_feature_importance(
    X_train, y_train,
    method='coefficients'
)

# Permutation importance (model-agnostic)
importance = analyzer.calculate_feature_importance(
    X_train, y_train,
    method='permutation'
)

# Sensitivity analysis
importance = analyzer.calculate_feature_importance(
    X_train, y_train,
    method='sensitivity'
)

# Visualize
analyzer.plot_importance(importance, top_n=10)
```

## v0.3.0 Features

### 8. Prediction Intervals (Uncertainty Quantification)

Generate prediction intervals with conformal prediction:

```python
from autotsforecast.uncertainty.intervals import PredictionIntervals

# Fit model first
model = RandomForestForecaster(horizon=14, n_lags=7)
model.fit(y_train, X=X_train)
forecasts = model.predict(X=X_test)

# Create prediction intervals
pi = PredictionIntervals(method='conformal', coverage=[0.80, 0.95])
pi.fit(model, y_train)
intervals = pi.predict(forecasts)

# Access intervals
print(f"Point: {intervals['point'].iloc[0, 0]:.1f}")
print(f"80% CI: [{intervals['lower_80'].iloc[0, 0]:.1f}, {intervals['upper_80'].iloc[0, 0]:.1f}]")
print(f"95% CI: [{intervals['lower_95'].iloc[0, 0]:.1f}, {intervals['upper_95'].iloc[0, 0]:.1f}]")
```

### 9. Calendar Features (Time-Based Feature Extraction)

```python
from autotsforecast.features.calendar import CalendarFeatures

# Auto-detect features with cyclical encoding
cal = CalendarFeatures(cyclical_encoding=True)
features = cal.fit_transform(y_train)

# Custom features with Fourier terms
cal = CalendarFeatures(
    features=['dayofweek', 'month', 'is_weekend'],
    fourier_terms={'weekly': (7, 2), 'yearly': (365.25, 3)},
    cyclical_encoding=True
)
custom_features = cal.fit_transform(y_train)

# Generate future calendar features
future_features = cal.transform_future(horizon=30)
```

### 10. Visualization (Static & Interactive)

```python
from autotsforecast.visualization.plots import plot_forecast, plot_model_comparison

# Static matplotlib plot with prediction intervals
fig = plot_forecast(
    y_train=y_train['series_a'],
    y_test=y_test['series_a'],
    forecast=forecasts['series_a'],
    lower=intervals['lower_95']['series_a'],
    upper=intervals['upper_95']['series_a'],
    title='Forecast with 95% PI'
)
plt.show()

# Model comparison
results = {'ARIMA': 12.5, 'XGBoost': 10.2, 'Prophet': 11.8}
fig = plot_model_comparison(results)
plt.show()

# Interactive Plotly plot (requires plotly)
try:
    from autotsforecast.visualization.plots import plot_forecast_interactive
    fig = plot_forecast_interactive(y_train, y_test, forecast)
    fig.show()
except ImportError:
    print("pip install plotly for interactive plots")
```

### 11. Parallel Processing (Speed Improvements)

```python
from autotsforecast.utils.parallel import ParallelForecaster, parallel_map

# Parallel multi-series forecasting
pf = ParallelForecaster(n_jobs=4)  # Use 4 parallel workers (-1 for all CPUs)

# Fit each series in parallel using model factory
fitted_models = pf.parallel_series_fit(
    model_factory=lambda: RandomForestForecaster(horizon=14, n_lags=7),
    y=y_train,
    X=X_train
)

# Generic parallel map
def process_item(x):
    return x ** 2

results = parallel_map(process_item, [1, 2, 3, 4, 5], n_jobs=2)
```

### 12. Progress Tracking

```python
from autotsforecast.visualization.progress import ProgressTracker

# Context manager
with ProgressTracker(total=100, description="Processing") as pbar:
    for i in range(100):
        # Do work
        pbar.update(1)

# Iterator wrapper
for item in ProgressTracker.track(items, description="Iterating"):
    # Process item
    pass
```

## Model Comparison

| Model | Supports Multivariate | Supports Covariates | Speed | Interpretability |
|-------|----------------------|---------------------|-------|------------------|
| MovingAverage | ✅ | ❌ | ⭐⭐⭐ | ⭐⭐⭐ |
| VAR | ✅ | ❌ | ⭐⭐ | ⭐⭐ |
| Linear | ✅ | ✅ | ⭐⭐⭐ | ⭐⭐⭐ |
| RandomForest | ✅ | ✅ | ⭐⭐ | ⭐⭐ (SHAP) |
| XGBoost | ✅ | ✅ | ⭐⭐ | ⭐⭐ (SHAP) |
| Prophet | ✅ | ✅ | ⭐⭐ | ⭐⭐ |
| ARIMA | ✅ | ✅ | ⭐ | ⭐⭐ |
| ETS | ✅ | ❌ | ⭐⭐ | ⭐⭐ |
| LSTM | ✅ | ✅ | ⭐ | ⭐ |

## Common Parameters

For complete parameter documentation, see **[API_REFERENCE.md](API_REFERENCE.md)**.

### Model Initialization
- `horizon`: Number of steps to forecast (required)
- `window`: 3-30 for moving average (MovingAverage only)
- `lags`: 1-21 for VAR, 7-30 for RF/XGBoost
- `n_lags`: Same as lags (used by RF, XGBoost, LSTM)
- `n_estimators`: 100-500 trees (RF, XGBoost)
- `max_depth`: 5-10 or None for unlimited (RF, XGBoost)
- `learning_rate`: 0.01-0.3 (XGBoost only)
- `seasonal_periods`: 7 (weekly), 12 (monthly) for ETS
- `order`: (p, d, q) where p,q: 1-5, d: 0-2 (ARIMA)
- `seasonal_order`: (P, D, Q, s) where s = seasonal period (ARIMA)

### AutoForecaster
- `candidate_models`: List of model instances to compare
- `metric`: Selection metric (`'rmse'`, `'mae'`, `'mape'`, `'mse'`)
- `n_splits`: 2-5 cross-validation splits (more = better selection, slower)
- `test_size`: Validation window size (typically = horizon)
- `window_type`: `'expanding'` (recommended) or `'rolling'`
- `per_series_models`: `True` (per-series selection) or `False` (global model)
- `n_jobs`: `1` (sequential, default) or `-1` for all CPU cores

### Covariates (X parameter)
- **Single DataFrame**: `X=pd.DataFrame(...)` — Same features for all series
- **Per-Series Dictionary**: `X={'series_a': df_a, 'series_b': df_b}` — Different features per series
  - Keys must match series names in `y`
  - Each DataFrame must have same index as `y`
  - Use with `per_series_models=True` for best results

### HierarchicalReconciler
- `method`: 
  - `'bottom_up'`: Aggregate from bottom level (keeps bottom forecasts)
  - `'top_down'`: Disaggregate from top using historical proportions
  - `'ols'`: OLS optimal reconciliation (minimizes total squared error)

### CovariatePreprocessor
- `encoding`: `'onehot'` (default) or `'label'` for categorical features
- `scale_numerical`: `True` or `False` (standardize numerical features)
- `handle_missing`: `'forward_fill'`, `'backward_fill'`, `'mean'`, `'drop'`
- `max_categories`: 50 (threshold for switching to label encoding)

## Tips

1. **Start simple**: Try MovingAverage or VAR first before complex models
2. **Use AutoForecaster**: Let it find the best model for your data
3. **Covariates**: Add external features to improve accuracy
4. **Per-Series Covariates**: Use different features for different series when they have different drivers
5. **SHAP for understanding**: Use SHAP to understand which features drive predictions
6. **Hierarchical reconciliation**: Ensures forecasts are coherent across levels
7. **Horizon**: Balance between forecast accuracy (shorter) and planning needs (longer)

## Troubleshooting

### ImportError: shap not installed
```bash
pip install shap
```

### ImportError: xgboost not installed
```bash
pip install xgboost
```

### Data size issues with XGBoost
- XGBoost creates lagged features, reducing effective sample size
- Use smaller horizon or more training data
- Consider RandomForest as alternative

### Hierarchical reconciliation errors
- Ensure all hierarchy nodes exist in forecasts
- Check for cycles in hierarchy definition
- Verify bottom-level series are properly identified

## Support

For issues and questions:
- **[API Reference](API_REFERENCE.md)**: Complete parameter documentation
- **[Tutorial](examples/autotsforecast_tutorial.ipynb)**: Comprehensive hands-on guide
- **[GitHub Issues](https://github.com/weibinxu86/autotsforecast/issues)**: Bug reports and questions
- **[Installation Guide](INSTALL.md)**: Detailed setup instructions
