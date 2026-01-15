# Analysis3054

Analysis3054 is a unified analytics and forecasting toolkit for energy, commodities, and demand planning. The goal is to make advanced forecasting, diagnostics, and data acquisition feel like one cohesive workflow. A key example is `LA_refinery`, which automates Louisiana DNR SONRIS refinery activity downloads and returns a clean pandas DataFrame so analysts can get reliable refinery data without manual portal work.

## Key capabilities
- LA DNR refinery scraping via `LA_refinery` (Selenium + optional Playwright fallback).
- Classical stats, ML, DL, and foundation-model forecasting (Chronos-2, TimesFM, Chronos Bolt).
- Intraday burn forecasting with covariates and quantile intervals.
- Fast API ingestion with async HTTP/2, retries, and background execution.
- Holiday calendars and market-holiday lookups for energy and finance workflows.
- Plotly-based visualization for forecasts, bands, and diagnostics.

## Installation

```bash
pip install analysis3054
```

Optional extras:

```bash
pip install "analysis3054[stats]"    # pmdarima + arch
pip install "analysis3054[ml]"       # scikit-learn + boosted trees
pip install "analysis3054[dl]"       # tensorflow
pip install "analysis3054[prophet]"  # prophet + neuralprophet
pip install "analysis3054[tbats]"    # tbats
pip install "analysis3054[physics]"  # torch + torchdiffeq + PyWavelets
pip install "analysis3054[autogluon]"# AutoGluon
pip install "analysis3054[seleniumbase]"# SeleniumBase (uc mode) for LA_refinery
pip install "analysis3054[playwright]"# Playwright fallback for LA_refinery
pip install "analysis3054[test]"     # pytest + pytest-anyio
pip install "analysis3054[all]"      # everything
```

Playwright (optional fallback for `LA_refinery`):

```bash
pip install playwright
playwright install
```

## Quickstart (LA_refinery)

```python
from analysis3054 import LA_refinery

# Scrape Louisiana DNR SONRIS refinery activity
# Use SeleniumBase uc-mode if you hit recaptcha blocks.
df = LA_refinery(start_date="01-JAN-2018", headless=False, engine="seleniumbase")
print(df.head())
```

## Louisiana Refinery Snapshot

Download: [analysis3054/data/la_refinery_latest.csv](analysis3054/data/la_refinery_latest.csv)

```python
import pandas as pd

df = pd.read_csv("analysis3054/data/la_refinery_latest.csv")
print(df.head())
```

If the bundled LA snapshot is empty, refresh it with:

```python
from analysis3054 import update_la_refinery_cache

update_la_refinery_cache(start_date="01-JAN-2018", headless=False)
```

## Port Statistics Snapshots

Port of LA container statistics:

Download: [analysis3054/data/port_of_la_container_stats_2021_present.csv](analysis3054/data/port_of_la_container_stats_2021_present.csv)

Port of Long Beach TEU archive:

Download: [analysis3054/data/port_long_beach_teu.csv](analysis3054/data/port_long_beach_teu.csv)

Port Houston container performance statistics:

Download: [analysis3054/data/port_houston_teu.csv](analysis3054/data/port_houston_teu.csv)

Port of Savannah Monthly TEU Throughput:

Download: [analysis3054/data/port_savannah_teu.csv](analysis3054/data/port_savannah_teu.csv)

Port of NY/NJ monthly TEU volumes:

Download: [analysis3054/data/port_ny_teu.csv](analysis3054/data/port_ny_teu.csv)

## EIA Electricity Raw Data (Annual)

EIA-860 2024 raw tabs:

- Generator Operable: [analysis3054/data/eia860_2024_generator_operable.csv](analysis3054/data/eia860_2024_generator_operable.csv)
- Generator Proposed: [analysis3054/data/eia860_2024_generator_proposed.csv](analysis3054/data/eia860_2024_generator_proposed.csv)
- Generator Retired/Canceled: [analysis3054/data/eia860_2024_generator_retired_canceled.csv](analysis3054/data/eia860_2024_generator_retired_canceled.csv)
- Multifuel Operable: [analysis3054/data/eia860_2024_multifuel_operable.csv](analysis3054/data/eia860_2024_multifuel_operable.csv)
- Multifuel Proposed: [analysis3054/data/eia860_2024_multifuel_proposed.csv](analysis3054/data/eia860_2024_multifuel_proposed.csv)
- Multifuel Retired/Canceled: [analysis3054/data/eia860_2024_multifuel_retired_canceled.csv](analysis3054/data/eia860_2024_multifuel_retired_canceled.csv)

EIA-923 2024 raw tabs:

- Page 1 Generation & Fuel: [analysis3054/data/eia923_2024_page1_generation_fuel.csv](analysis3054/data/eia923_2024_page1_generation_fuel.csv)
- Page 3 Boiler Fuel: [analysis3054/data/eia923_2024_page3_boiler_fuel.csv](analysis3054/data/eia923_2024_page3_boiler_fuel.csv)
- Page 4 Generator Data: [analysis3054/data/eia923_2024_page4_generator_data.csv](analysis3054/data/eia923_2024_page4_generator_data.csv)
- Page 5 Fuel Receipts & Costs: [analysis3054/data/eia923_2024_page5_fuel_receipts_costs.csv](analysis3054/data/eia923_2024_page5_fuel_receipts_costs.csv)
- DFO generator inventory: [analysis3054/data/dfo_generators_inventory.csv](analysis3054/data/dfo_generators_inventory.csv)
- DFO fuel receipts/costs: [analysis3054/data/dfo_generators_costs.csv](analysis3054/data/dfo_generators_costs.csv)

## Spain (CORES) Raw Data

- Oil products (All): [analysis3054/data/Spain_content_oil_products_all.csv](analysis3054/data/Spain_content_oil_products_all.csv)
- Crude oil balance & refinery output: [analysis3054/data/Spain_content_crude_oil_balance_refinery_output.csv](analysis3054/data/Spain_content_crude_oil_balance_refinery_output.csv)
- Gas consumption (market): [analysis3054/data/Spain_content_gas_consumption_by_market.csv](analysis3054/data/Spain_content_gas_consumption_by_market.csv)
- Gas consumption (pressure): [analysis3054/data/Spain_content_gas_consumption_by_pressure_bracket.csv](analysis3054/data/Spain_content_gas_consumption_by_pressure_bracket.csv)

## UK Oil Products (Energy Trends Section 3)

- ET 3.12 Monthly (Refinery throughput & output): [analysis3054/data/UK_content_et_3_12_month.csv](analysis3054/data/UK_content_et_3_12_month.csv)
- ET 3.13 Monthly (Deliveries for inland consumption): [analysis3054/data/UK_content_et_3_13_month.csv](analysis3054/data/UK_content_et_3_13_month.csv)

## Europe Energy Rollup

- Spain + UK long-form series: [analysis3054/data/europe_energy_long.csv](analysis3054/data/europe_energy_long.csv)

## FRED Diesel Macro Snapshots

- Monthly: [analysis3054/data/fred_diesel_monthly.csv](analysis3054/data/fred_diesel_monthly.csv)
- Quarterly: [analysis3054/data/fred_diesel_quarterly.csv](analysis3054/data/fred_diesel_quarterly.csv)
- Macro focus (monthly): [analysis3054/data/fred_macro_focus_monthly.csv](analysis3054/data/fred_macro_focus_monthly.csv)
- Macro focus (monthly YoY): [analysis3054/data/fred_macro_focus_monthly_yoy.csv](analysis3054/data/fred_macro_focus_monthly_yoy.csv)
- Macro focus (quarterly): [analysis3054/data/fred_macro_focus_quarterly.csv](analysis3054/data/fred_macro_focus_quarterly.csv)
- Macro focus (quarterly YoY): [analysis3054/data/fred_macro_focus_quarterly_yoy.csv](analysis3054/data/fred_macro_focus_quarterly_yoy.csv)
- Macro focus (annual): [analysis3054/data/fred_macro_focus_annual.csv](analysis3054/data/fred_macro_focus_annual.csv)
- Macro focus (annual YoY): [analysis3054/data/fred_macro_focus_annual_yoy.csv](analysis3054/data/fred_macro_focus_annual_yoy.csv)

## Rail Traffic Snapshots (AAR)

- North American Rail Traffic: [analysis3054/data/rail_traffic_north_american.csv](analysis3054/data/rail_traffic_north_american.csv)
- U.S. Rail Traffic: [analysis3054/data/rail_traffic_us.csv](analysis3054/data/rail_traffic_us.csv)
- Canadian Rail Traffic: [analysis3054/data/rail_traffic_canada.csv](analysis3054/data/rail_traffic_canada.csv)
- Mexican Rail Traffic: [analysis3054/data/rail_traffic_mexico.csv](analysis3054/data/rail_traffic_mexico.csv)

## Dashboards

- Refinery product mix dashboard: [analysis3054/data/refinery_dashboard.html](analysis3054/data/refinery_dashboard.html)
- Refinery product mix dashboard (exportable): [analysis3054/data/refinery_dashboard_export.html](analysis3054/data/refinery_dashboard_export.html)
- Rail traffic analyzer: [analysis3054/data/rail_traffic_dashboard.html](analysis3054/data/rail_traffic_dashboard.html)
- Port TEU dashboard: [analysis3054/data/port_teu_dashboard.html](analysis3054/data/port_teu_dashboard.html)
- TX refinery receipts & deliveries: [analysis3054/data/tx_refineries_transfers_dashboard.html](analysis3054/data/tx_refineries_transfers_dashboard.html)
- Macro drivers dashboard: [analysis3054/data/macro_dashboard.html](analysis3054/data/macro_dashboard.html)
- Europe energy dashboard: [analysis3054/data/europe_energy_dashboard.html](analysis3054/data/europe_energy_dashboard.html)
- DFO generator dashboard: [analysis3054/data/dfo_generators_dashboard.html](analysis3054/data/dfo_generators_dashboard.html)

## Refinery Workflow (TX + LA)

This section covers the end-to-end refinery workflow: refresh data, run Chronos2 forecasts, add outage covariates, and rebuild the dashboard. Run commands from the repo root.

### 1) One-time setup (env + deps)
1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install the local package so scripts use the repo code:
   ```bash
   pip install -e .
   ```
3. Set API keys for the TX refinery PDF extraction (Gemini):
   ```bash
   export GOOGLE_API_KEY="your_key_here"
   # or: export GOOGLE_AI_API_KEY="your_key_here"
   ```
4. (Optional) Persist defaults in `~/.analysis3054_env` so monthly refreshes pick them up automatically:
   ```bash
   cat > ~/.analysis3054_env <<'EOF'
   export GOOGLE_API_KEY="your_key_here"
   export TX_REPULL_MAX_WORKERS=6
   export TX_REPULL_TIMEOUT=2400
   export TX_REFRESH_MONTHS=5
   export TX_TRANSFERS_REFRESH_MONTHS=3
   export REFINERY_UPDATE_MIN_DAYS=0
   EOF
   ```
   `scripts/update_refinery_snapshots.py` reads this file on startup.

### 2) Refresh refinery data
You can either run the full monthly pipeline or do targeted repulls.

Full pipeline (TX + LA + forecasts + dashboard):
```bash
python scripts/update_refinery_snapshots.py
```
What it does:
- Refreshes LA refinery data (`analysis3054/data/la_refinery_latest.csv`).
- Repulls TX refinery PDFs for the last `TX_REFRESH_MONTHS` months and writes `analysis3054/data/tx_refineries_2021_present.csv`.
- Updates TX receipts/deliveries snapshots.
- Rebuilds the Chronos2 product forecasts.
- Rebuilds the refinery dashboard HTML files.

Targeted TX repull (specific facility IDs, specific date range):
```bash
python scripts/repull_tx_facilities.py \
  --facility-ids "03-0012,03-0138" \
  --start-year 2021 --start-month 1 \
  --end-year 2025 --end-month 9 \
  --max-workers 6 \
  --timeout 2400
```
Notes:
- Facility IDs are normalized, so `03-0012` and `3-12` are treated the same.
- The script merges new rows into `analysis3054/data/tx_refineries_2021_present.csv`.
- The TX parser also standardizes `Name of Material` to lowercase by code mapping.

Backfill missing months (if any are reported in `analysis3054/data/tx_refineries_missing_months.csv`):
```bash
python scripts/backfill_tx_refineries_missing.py
```

### 3) Add refinery outage / maintenance data
Create `analysis3054/data/refinery_maintenance.csv` to supply outage covariates and populate the maintenance panel.

Required columns:
- `refinery_name`: must match the dashboard label (use values in `analysis3054/data/tx_refineries_2021_present.csv` and `analysis3054/data/la_refinery_latest.csv`).
- `date`: monthly timestamp (YYYY-MM-01).

All other columns are treated as numeric covariates (planned/unplanned outages, capacity offline, unit status, etc.). Unit keywords in the column name are mapped to chart labels (e.g., `fcc_planned`, `coker_unplanned`, `distill_planned`).

Example:
```csv
refinery_name,date,fcc_planned,coker_unplanned,distill_planned
Baytown Refinery,2025-09-01,0,1,0
Marathon El Paso,2025-06-01,0,0,1
```

After updating this file, rebuild forecasts and the dashboard so the maintenance chart is updated. The current product-level forecast ignores covariates; outage data is used in the maintenance chart and the aggregate `build_refinery_forecast` path.

### 4) Run Chronos2 forecasts
The dashboard uses `analysis3054/data/refinery_product_forecast.csv`, which is produced by `build_refinery_product_forecast` (Chronos2 multivariate per refinery).

Run the product-level forecast (default horizon = 6 months):
```bash
python - <<'PY'
from analysis3054.refinery_forecast import build_refinery_product_forecast

build_refinery_product_forecast(horizon_default=6)
PY
```

Run a direct Chronos2 multivariate forecast from the TX CSV (single refinery example):
```python
import pandas as pd
from analysis3054.forecasting import chronos2_multivariate_forecast

tx = pd.read_csv("analysis3054/data/tx_refineries_2021_present.csv")
tx = tx[tx["refinery_name"].str.lower() == "marathon el paso"]
tx["statement_date"] = pd.to_datetime(tx["statement_date"], errors="coerce")
tx = tx[tx["statement_date"].notna()].copy()

def clean_numeric(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("(", "-", regex=False)
        .str.replace(")", "", regex=False)
        .replace({"": "0", "nan": "0"})
        .astype(float)
    )

tx["days_in_month"] = tx["statement_date"].dt.daysinmonth
tx["production_kbd"] = clean_numeric(tx["Products Manufactured"]) / tx["days_in_month"] / 1000.0
tx["crude_kbd"] = clean_numeric(tx["Input Runs to Stills and/or Blends"]) / tx["days_in_month"] / 1000.0

pivot = (
    tx.pivot_table(
        index="statement_date",
        columns="Name of Material",
        values="production_kbd",
        aggfunc="sum",
    )
    .sort_index()
)
pivot["crude_kbd"] = tx.groupby("statement_date")["crude_kbd"].sum()
pivot = pivot.asfreq("MS", fill_value=0.0).reset_index().rename(columns={"statement_date": "date"})

target_cols = [col for col in pivot.columns if col != "date"]
res = chronos2_multivariate_forecast(
    pivot,
    date_col="date",
    target_cols=target_cols,
    prediction_length=6,
    quantile_levels=[0.5],
    device_map="cpu",
)
print(res.forecasts.tail())
```

If you want outage covariates to influence aggregate metrics (total output/yield), run:
```bash
python - <<'PY'
from analysis3054.refinery_forecast import build_refinery_forecast

build_refinery_forecast(horizon_default=6)
PY
```
This writes `analysis3054/data/refinery_forecast.csv` and `analysis3054/data/refinery_data.csv`.

### 5) Build and refresh the refinery dashboard
```bash
python scripts/build_refinery_dashboard.py
```
This generates:
- `analysis3054/data/refinery_dashboard.html` (standard Plotly assets)
- `analysis3054/data/refinery_dashboard_export.html` (self-contained, shareable)

Option B: build with CSVs on another system (and skip Chronos2 refresh):
```bash
python scripts/build_refinery_dashboard.py \
  --tx-csv /path/to/tx_refineries_2021_present.csv \
  --la-csv /path/to/la_refinery_latest.csv \
  --forecast-csv /path/to/refinery_product_forecast.csv \
  --maintenance-csv /path/to/refinery_maintenance.csv \
  --name-map-csv /path/to/tx_refinery_name_map.csv \
  --output-html /path/to/refinery_dashboard.html \
  --export-html /path/to/refinery_dashboard_export.html \
  --skip-forecast-refresh
```
Notes:
- The standard HTML expects `plotly-<version>.min.js` in the same folder as `--output-html`; the script will download it there.
- The export HTML is fully self-contained, so you can share it without extra assets.

Open the dashboard in Edge:
```bash
python scripts/open_refinery_dashboard.py --export --browser edge
```

### 6) Monthly automation (optional)
Use a cron or scheduler to run the full pipeline once a month. Example:
```bash
crontab -e
```
```bash
0 6 1 * * cd /path/to/Analysis3054-Codex && python scripts/update_refinery_snapshots.py
```

## Additional examples

### Forecasting engine
```python
import pandas as pd
from analysis3054 import build_default_engine

engine = build_default_engine()
res = engine.forecast(
    df=dataframe,
    date_col="date",
    target_cols=["demand"],
    horizon=14,
    model="harmonic",
)
print(res.forecasts.tail())
```

### API ingestion
```python
from analysis3054 import fetch_apis_to_dataframe

endpoints = [
    "https://api.example.com/v1/events",
    {"url": "https://api.example.com/v1/users", "params": {"page": 1}},
]

frame = fetch_apis_to_dataframe(
    endpoints,
    max_workers=16,
    sort_by="timestamp",
    transform=lambda df: df.assign(volume_pct=df["volume"] / df["volume"].sum()),
)
print(frame.head())
```

## Public API reference (functions and classes)

### Core plotting
- `five_year_plot` (EIA-style 5-year band plot)
- `forecast_plot`, `cumulative_return_plot`, `max_drawdown`, `acf_pacf_plot`

### Data utilities (`analysis3054.utils`)
- `conditional_column_merge`, `conditional_row_merge`, `nearest_key_merge`, `coalesce_merge`
- `rolling_fill`, `add_time_features`, `resample_time_series`, `winsorize_columns`
- `add_lag_features`, `scale_columns`, `rolling_window_features`
- `data_quality_report`, `df_split`, `get_padd`
- `ensure_env_variables`, `configure_snowflake_connector`, `EnvVariableRequest`

### Forecast engine
- `ForecastEngine`, `EngineForecastResult`, `build_default_engine`

### Auto-ML forecasting (`analysis3054.auto_ml_forecasting`)
- `auto_generate_features`, `FeatureEngineeringResult`, `MLForecastResult`
- `chronos2_auto_covariate_forecast`
- `gradient_boosting_covariate_forecast`, `random_forest_covariate_forecast`, `ridge_covariate_forecast`
- `elastic_net_covariate_forecast`, `bayesian_ridge_covariate_forecast`, `huber_covariate_forecast`
- `pls_covariate_forecast`, `fourier_ridge_seasonal_forecast`, `hist_gradient_direct_forecast`
- `svr_high_frequency_forecast`, `xgboost_covariate_forecast`, `lightgbm_covariate_forecast`
- `catboost_covariate_forecast`, `stacked_meta_ensemble_forecast`

### Forecasting (classical + advanced)
- Statistical: `arima_forecast`, `auto_arima_forecast`, `ets_forecast`, `var_forecast`, `vecm_forecast`
- Regime/structural: `markov_switching_forecast`, `unobserved_components_forecast`, `dynamic_factor_forecast`
- Volatility: `garch_forecast`
- Seasonal/other: `theta_forecast`, `sarimax_forecast`
- ML/DL: `lstm_forecast`, `tcn_forecast`, `transformer_forecast`
- Boosted/trees: `xgboost_forecast`, `lightgbm_forecast`, `catboost_forecast`, `knn_forecast`
- Others: `bats_forecast`, `neuralprophet_forecast`, `elastic_net_forecast`, `svr_forecast`
- Hybrids: `stl_fourier_kalman_forecast`, `regime_switching_forecast`, `quantile_projection_forecast`,
  `wavelet_multiresolution_forecast`, `latent_factor_state_forecast`
- Blends: `adaptive_forecast`, `dynamic_forecast_blend`, `auto_error_correcting_forecast`,
  `forecasting_playbook_examples`

### Chronos-2 / Chronos Bolt / TimesFM
- `chronos2_forecast`, `chronos2_univariate_forecast`, `chronos2_multivariate_forecast`,
  `chronos2_covariate_forecast`, `chronos2_weekly_implied_demand`, `chronos2_feature_generator`
- `chronos2_quantile_forecast`, `chronos2_anomaly_detection`, `chronos2_impute_missing`
- `chronos_bolt_forecast`, `chronos_bolt_backtest`, `chronos_bolt_hyperparam_search`,
  `chronos_bolt_multi_target_forecast`, `chronos_bolt_quantile_forecast`,
  `chronos_bolt_anomaly_detection`, `chronos_bolt_impute_missing`
- `timesfm_forecast`

### Intraday burn forecasting
- `intraday_load_burn_forecast`, `forecast_distillate_burn`, `intraday_gp_forecast`
- `intraday_sarimax_forecast`, `intraday_quantile_regression_forecast`
- `forecast_major_burn_days`, `hierarchical_reconciled_burn_forecast`, `load_weather_interaction_forecast`
- `hist_gradient_burn_forecast`

### AutoGluon forecasting
- `autogluon_tabular_burn_forecast`, `autogluon_tabular_burn_classifier`
- `autogluon_timeseries_forecast`, `autogluon_timeseries_forecast_general`
- `autogluon_chronos2_forecast`

### Statistics and diagnostics
- `hurst_exponent`, `dfa_exponent`, `rolling_sharpe_ratio`, `sample_entropy`, `higuchi_fractal_dimension`
- `rolling_zscore`, `mann_kendall_test`, `bollinger_bands`, `stationarity_tests`
- `trend_seasonality_strength`, `box_cox_transform`, `seasonal_adjust`
- `cross_correlation_plot`, `partial_autocorrelation_plot`, `pca_decomposition`, `granger_causality_matrix`

### Regression and ensembles
- `ols_regression`, `rolling_correlation`, `cusum_olsresid_test`
- `model_leaderboard`, `simple_ensemble`

### Finance
- `liquidity_adjusted_volatility`, `rolling_beta`

### Physics-inspired forecasting
- `multi_resolution_wavelet_decompose`
- `ODEFunc`, `NeuralODEBlock`, `SobolevLoss`
- `KoopmanSpectralDecomposer`, `rolling_hurst_router`
- `plot_scalogram`, `plot_phase_portrait`, `plot_forecast_trajectory`

### Calendars and holidays
- `available_holiday_calendars`, `get_holidays`, `get_holidays_between`
- `resolve_iso_code`, `get_market_code`, `is_holiday`, `is_financial_holiday`, `is_platts_holiday`

### Data ingestion and communications
- `fetch_apis_to_dataframe`
- `send_email`, `EmailContent`
- `InboxCleaner`, `ArchiveConfig`, `ConnectionConfig`, `KeywordRule`, `RetentionPolicy`, `InboxCleanReport`, `clean_inbox`

### External data clients
- `RefinedFuelsUSMDClient`, `request_access_token`
- `LA_refinery`, `fetch_la_refinery_data`, `ScraperError`

## Testing

```bash
pip install "analysis3054[test]"
pytest -q
```

## Texas Refinery Dataset (2021–present)

Download: [analysis3054/data/tx_refineries_2021_present.csv](analysis3054/data/tx_refineries_2021_present.csv)

```python
import pandas as pd

df = pd.read_csv("analysis3054/data/tx_refineries_2021_present.csv")
print(df.head())
```

## License
MIT
