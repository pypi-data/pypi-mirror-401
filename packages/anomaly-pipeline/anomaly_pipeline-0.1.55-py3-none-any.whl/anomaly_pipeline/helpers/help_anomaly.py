import pandas as pd
import numpy as np
import plotly.graph_objects as go
from IPython.display import display, Markdown
import logging
import warnings
warnings.filterwarnings("ignore")
from .percentile import detect_outliers_percentile
from .STD import detect_outliers_sd
from .MAD import detect_outliers_mad
from .IQR import detect_outliers_iqr
from .iso_forest_general import detect_outliers_isf_general
from .ewma import ewma_with_anomalies_rolling_group
from .fb_prophet import detect_time_series_anomalies_fb_walkforward
from .iso_forest_timeseries import detect_time_series_anomalies_isoforest
from .DB_scan import detect_time_series_anomalies_dbscan
from .Preprocessing import create_full_calendar_and_interpolate, print_anomaly_stats, calculate_ensemble_scores
from .evaluation_plots import anomaly_eval_plot, anomaly_percentile_plot,anomaly_sd_plot, anomaly_mad_plot, anomaly_iqr_plot, anomaly_ewma_plot, anomaly_fb_plot, anomaly_dbscan_plot, anomaly_isolation_forest_plot


group_columns=["key", "channel"]
variable="views"
eval_period = 12
date_column = "week_start"
min_records = 52
max_records = 156
mad_threshold = 2
mad_scale_factor = 0.6745
alpha=.3
sigma=1.5
prophet_CI = .95
freq = 'W-MON'


def help_anomaly(topic=None):
    
    #example_df = get_example_df()

    if topic == None:
        help_overview()
    elif topic.lower()[:7] == 'percent':
        help_percentile()
    elif topic.lower() == 'iqr':
        help_iqr()
    elif topic.lower()[:2] == 'fb' or topic.lower()[:5] == 'proph':
        help_fb()
    elif topic.lower() == 'ewma':
        help_ewma()
    elif topic.lower()[:2] == 'db':
        help_dbscan()
    elif topic.lower()[:3] == 'iso':
        help_isofor()
    elif topic.lower()[:2] in ['st', 'sd']:
        help_sd()
    elif topic.lower()[:3] == 'mad':
        help_mad()


def get_example_df():
    
    # Check if example_df already exists in the notebook
    global_vars = globals()
    exists = ('example_df' in global_vars) and isinstance(global_vars['example_df'], pd.DataFrame)

    # If it doesn't exist, create it
    if exists == False:
        
        global example_df
        
        views = [223006, 145101, 136508, 119284, 151332, 169419, 158795, 163725, 161911, 153131, 178292, 188910, 192736, 165486, 157370, 151250, 151699,
            144465, 167651, 185210, 172594, 176735, 158885, 140992, 184203, 235889, 203074, 203714, 162486, 227249, 243952, 241711, 213386, 183171,
            176070, 185944, 191282, 180852, 219299, 271454, 216265, 150586, 123755, 126039, 117597, 103758, 133977, 144088, 143186, 247731, 267901,
            289105, 378025, 221419, 119153, 117262, 135635, 157462, 158551, 162637, 157246, 144626, 129089, 153280, 145880, 130291, 114119, 112931,
            110593, 120172, 185307, 213343, 164825, 153140, 127525, 128465, 180317, 232471, 229766, 129962, 98732, 181722, 198247, 222167, 175792,
            131070, 154662, 158707, 152083, 151097, 194114, 230775, 195828, 150668, 119488, 118110, 165357, 150681, 151303, 137414, 126470, 223347,
            222285, 244610, 277318]

        example_df = pd.DataFrame({
            'key': ['PLP>appliances>refrigerators'] * len(views),
            'channel': ['raw_desktop_views'] * len(views),
            'week_start': pd.date_range(start='2023-11-27', end='2025-11-24', freq='W-MON'),
            'views': views})
        
        
        example_df = create_full_calendar_and_interpolate(example_df, group_columns, variable, date_column, freq, min_records, max_records)[0]
        
        logging.getLogger('fbprophet').setLevel(logging.ERROR)
        logging.getLogger('cmdstanpy').disabled = True
        
        # tmp_model = Prophet(
        #     weekly_seasonality=True,
        #     yearly_seasonality=True,
        #     daily_seasonality=False
        # )
        # tmp_model.fit(example_df[['week_start', 'views']].rename(columns={'week_start': 'ds', 'views': 'y'}))
        
        df_percentile = detect_outliers_percentile(example_df, variable, date_column, eval_period)
        df_iqr = detect_outliers_iqr(example_df, variable, date_column, eval_period)
        df_mad = detect_outliers_mad(example_df, variable, date_column, mad_threshold, mad_scale_factor, eval_period)
        df_std = detect_outliers_sd(example_df, variable, date_column, eval_period)
        df_ewma = ewma_with_anomalies_rolling_group(example_df, group_columns, variable, date_column, alpha, sigma, eval_period)
        df_fb = detect_time_series_anomalies_fb_walkforward(example_df, variable, date_column, eval_period,prophet_CI)
        df_isofor = detect_time_series_anomalies_isoforest(example_df,variable, date_column, eval_period)
        for col in df_isofor.columns.tolist():
            if col.endswith('_timeseries'):
                df_isofor = df_isofor.rename(columns={col: col.replace('_timeseries', '')})
        df_dbscan = detect_time_series_anomalies_dbscan(example_df, variable, date_column, eval_period)
        
        orig_columns = example_df.columns.to_list()
        example_df = pd.concat([
            example_df,
            df_percentile.drop(columns=orig_columns, errors='ignore'),
            df_iqr.drop(columns=orig_columns, errors='ignore'),
            df_mad.drop(columns=orig_columns, errors='ignore'),
            df_std.drop(columns=orig_columns, errors='ignore'),
            df_ewma.drop(columns=orig_columns, errors='ignore'),
            df_fb.drop(columns=orig_columns, errors='ignore'),
            df_isofor.drop(columns=orig_columns, errors='ignore'),
            df_dbscan.drop(columns=orig_columns, errors='ignore')
        ], axis=1)
        
        example_df = calculate_ensemble_scores(example_df, 'views')
    
    globals()['anomaly_example_df'] = example_df
    return example_df


def help_overview():
    display(Markdown(overview_msg))
    example_df = get_example_df()
    display(example_df[['key', 'channel', 'week_start', 'views']].tail(12))
    display(Markdown(overview_msg2))
    anomaly_eval_plot(example_df, group_columns, variable, date_column, eval_period, show_anomaly_scores_on_main_plot=False)


def help_percentile():
    display(Markdown(percentile_msg))
    example_df = get_example_df()
    anomaly_percentile_plot(example_df, group_columns, variable, date_column, eval_period, final_anomalies=False)


def help_iqr():
    display(Markdown(iqr_msg))
    example_df = get_example_df()
    anomaly_iqr_plot(example_df, group_columns, variable, date_column, eval_period, final_anomalies=False)


def help_mad():
    display(Markdown(mad_msg))
    example_df = get_example_df()
    anomaly_mad_plot(example_df, group_columns, variable, date_column, eval_period, final_anomalies=False)

    
def help_sd():
    display(Markdown(sd_msg))
    example_df = get_example_df()
    anomaly_sd_plot(example_df, group_columns, variable, date_column, eval_period, final_anomalies=False)

    
def help_ewma():
    display(Markdown(ewma_msg))
    example_df = get_example_df()
    anomaly_ewma_plot(example_df, group_columns, variable, date_column, eval_period, final_anomalies=False)


def help_fb():
    display(Markdown(fb_msg))
    example_df = get_example_df()
    anomaly_fb_plot(example_df, group_columns, variable, date_column, eval_period, final_anomalies=False)


def help_dbscan():
    display(Markdown(dbscan_msg))
    example_df = get_example_df()
    anomaly_dbscan_plot(example_df, group_columns, variable, date_column, eval_period, final_anomalies=False)


def help_isofor():
    display(Markdown(isofor_msg))
    example_df = get_example_df()
    anomaly_isolation_forest_plot(example_df, group_columns, variable, date_column, eval_period, final_anomalies=False)


overview_msg = """
# 🏗️ The Anomaly Detection Function
---

FYI, you can see information about specific models used in the anomaly pipeline with any of the following commands:


```python
help_anomaly('percentile')
help_anomaly('iqr')
help_anomaly('mad')
help_anomaly('std')
help_anomaly('ewma')
help_anomaly('prophet')
help_anomaly('dbscan')
help_anomaly('iso') # For information on isolation forest
```

---

The `run_pipeline` function handles end-to-end processing — from data cleaning and interpolation to executing multiple machine learning models in parallel and aggregating their results into a final "Consensus" anomaly flag.

## 📋 Functional Overview
The pipeline takes raw master data, partitions it into groups by unique ID, applies a suite of 8 different anomaly detection methods, and then flags observations as anomalies where at least half of the models consider the observation an anomaly.

The master data DataFrame that you pass into the anomaly detection pipeline needs to have at least 3 columns - unique ID, date, and a target variable. The unique ID can be defined by multiple columns.

Here is an example of a DataFrame that has two columns that comprise the unique ID `['key', 'channel']`, `week_start` is the date column, and `views` is the target variable:"""


overview_msg2 = """
## 🧠 Core Execution Stages

### 1. Preprocessing & Interpolation
Before modeling, the function interpolates target variable values for missing dates
* Fill gaps in the `variable` column to prevent model crashes.

### 2. Statistical Baseline Models (Local Execution)
The pipeline first runs four computationally light models sequentially on each group:
* **Percentile & IQR:** Non-parametric bounds detection.
* **SD (Standard Deviation) & MAD (Median Absolute Deviation):** Variance-based detection.

### 3. Parallel Machine Learning Suite (`process_group`)
To maximize performance, the pipeline uses `joblib.Parallel` to run intensive models across all available CPU cores. The `process_group` utility acts as a **router**, sending data to the correct engine based on the model key:
* **FB (Prophet):** Walk-forward time-series forecasting.
* **EWMA:** Exponentially weighted moving averages.
* **ISF (Isolation Forest):** Unsupervised isolation of anomalies.
* **DBSCAN:** Density-based spatial clustering.

### 4. Majority Voting (Ensemble Logic)
The power of this pipeline lies in its **Consensus Model**. After all models finish, the pipeline calculates:
> **`Anomaly_Votes`**: The sum of flags across all 8-9 methods.
>
> **`is_Anomaly`**: A final boolean set to **True** only if at least **4 models** agree that the point is an outlier.

## 📤 Key Output Columns
* **`refresh_date`**: The timestamp of when the pipeline was executed.
* **`Anomaly_Votes`**: Total count of models that flagged the row.
* **`is_Anomaly`**: The final "Gold Standard" anomaly flag.
* **Individual Model Flags**: Columns like `is_FB_anomaly`, `is_IQR_anomaly`, etc., for granular auditing.

## 💡 Usage Context
Use `run_pipeline` when you need a **highly reliable, automated output**. By combining statistical, forecasting, and clustering models, the pipeline reduces "false positives" often generated by single-model approaches.

---
### ⚙️ Primary Hyperparameters
| Parameter | Default | Description |
| :--- | :--- | :--- |
| **`eval_period`** | `12` | The number of recent weeks to evaluate for anomalies. |
| **`alpha` / `sigma`** | `0.3` / `1.5` | Sensitivity settings for the EWMA model. |
| **`prophet_CI`** | `0.90` | The confidence interval for the Prophet (FB) model. |
| **`n_jobs`** | `-1` | Utilizes all available processor cores for parallelization. |


---
## 📊 Evaluation Plot
The plot below shows an example of anomalies identified by the process:
"""


percentile_msg = """# 📈 PERCENTILE MODEL
---

The `detect_outliers_percentile` function is a robust anomaly detection tool designed to identify **statistical outliers** in
time series or grouped data using a dynamic, **expanding window percentile approach**.

## 📋 Functional Overview
The function operates by partitioning the data into an initial training set and a subsequent evaluation period. It establishes
**"normal" behavior** based on the 5th and 95th percentiles of the available historical data, flagging any value that falls
outside these bounds as an anomaly.

## 🧠 Core Logic Stages

### 1. Data Preparation and Validation
> **Minimum Threshold:** The function requires at least **10 data points** to run; otherwise, it returns an empty DataFrame to
prevent statistically insignificant results.
>
> **Copying:** It creates a copy of the input group to ensure the original data remains unaltered during the calculation process.

### 2. Initial Training Block
* **Static Baseline:** For the first part of the data (everything before the `eval_period`), the function calculates a single
static baseline using the 5th and 95th percentiles of the entire training block.
* **Classification:** It applies these fixed bounds to the training rows, labeling them using a helper `classify` function and
assigning a boolean `is_Percentile_anomaly` flag.

### 3. Expanding Window Evaluation
* **Sequential Testing:** For each data point in the evaluation period (the last *n* points specified by `eval_period`), the
function recalculates the percentiles using **all previously seen data points**.
* **Dynamic Adaptation:** As the loop progresses, the "training set" grows. This allows the model to adapt to gradual shifts in
the data distribution, as the thresholds for the current point are informed by every point that came before it.
* **Real-time Simulation:** By calculating the bounds for point $i$ based only on points $0$ to $i-1$, the function simulates how
the model would perform in a live environment.

## 📤 Key Output Columns
The function appends the following columns to the returned DataFrame:
* **`Percentile_low` / `Percentile_high`**: The specific thresholds used to evaluate that row.
* **`Percentile_anomaly`**: A categorical label (likely "High," "Low," or "Normal") generated by the external `classify` function.
* **`is_Percentile_anomaly`**: A boolean flag indicating whether the value was outside the 5%–95% range.

## 💡 Usage Context
This function is particularly useful for detecting spikes or drops in metrics where the underlying distribution might **drift
slowly over time**. By using percentiles rather than standard deviations, it is more resilient to extreme historical outliers
that might otherwise skew a mean-based threshold.

---
## 📊 Evaluation Plot
The plot below shows an example of how the Percentile model sets bounds and anomaly regions:
"""

iqr_msg = iqr_msg = """
# 📊 IQR MODEL (Interquartile Range)
---

The `detect_outliers_iqr` function is a statistical anomaly detection tool that identifies outliers by calculating the **Interquartile Range (IQR)** through a dynamic, **expanding window approach**.

## 🔍 Functional Overview
The function partitions data into a baseline **"training" set** and an **"evaluation" period**. It identifies **"normal" data** as values falling within:
> $$[Q1 - 1.5 \\times IQR, Q3 + 1.5 \\times IQR]$$

Any data point exceeding these calculated boundaries is flagged as a statistical anomaly.

## 🧠 Core Logic Stages

### 1. Data Preparation and Validation
* **Minimum Threshold:** To ensure statistical significance, the function requires at least **10 data points**; if the threshold isn't met, it returns an empty DataFrame.
* **Safe Copying:** It operates on a **copy** of the input group to protect the original dataset from unintended modifications.

### 2. Initial Training Block
* **Static Baseline:** For the initial block (all data before the `eval_period`), the function calculates a single set of baseline quartiles ($Q1$ and $Q3$) and the resulting $IQR$.
* **Fixed Boundaries:** The lower bound is set to $max(Q1 - 1.5 \\times IQR, 0)$ and the upper bound to $Q3 + 1.5 \\times IQR$.
* **Batch Classification:** These fixed bounds are applied to all rows in the training set, assigning them a **"TRAIN"** label and a boolean `is_IQR_anomaly` flag.

### 3. Expanding Window Evaluation
* **Incremental Recalculation:** For every point in the evaluation period (the last $n$ points), the function recalculates $Q1$, $Q3$, and $IQR$ using **all previously observed data**.
* **Dynamic Adaptation:** As the loop iterates, the training window **"expands."** This allows the model to adjust its expectations of "normal" as more data becomes available.
* **Live Simulation:** By testing point $i$ against thresholds derived from points $0$ to $i-1$, the function accurately simulates how the outlier detection would behave in a production environment.

## 📤 Key Output Columns
The function appends several analytical columns to the returned DataFrame:
* **`Q1` / `Q3` / `IQR`**: The specific quartiles and range used for that row's calculation.
* **`IQR_low` / `IQR_high`**: The calculated "fences" (bounds). The lower bound is clipped at zero.
* **`set`**: Categorizes the row as either **"TRAIN"** or **"TEST"**.
* **`IQR_anomaly`**: A descriptive label (e.g., "High," "Low," or "Normal").
* **`is_IQR_anomaly`**: A boolean flag identifying if the value is an outlier.

## 💡 Usage Context
The IQR method is a **classic, non-parametric approach** to anomaly detection. It is particularly effective for datasets where you **cannot assume a normal (Gaussian) distribution**.

By using the expanding window, this function is more robust than a simple static boxplot, as it accounts for a growing history of data while remaining less sensitive to extreme outliers than mean-based methods (like Z-Score).

---
## 📊 Evaluation Plot
The plot below shows an example of how the IQR model sets bounds and anomaly regions:
"""


fb_msg = """
# 🚀 Facebook Prophet Walk-Forward Model
---

The `detect_time_series_anomalies_fb_walkforward` function is a sophisticated forecasting tool designed for **iterative anomaly detection**. It utilizes the Facebook Prophet library to perform a **walk-forward validation**, forecasting one data point at a time and expanding the training set as it progresses.

## 📋 Functional Overview
Unlike standard batch forecasting, this function operates by simulating a real-world scenario where the model is updated as soon as new data arrives. It establishes a **cutoff date** based on the specified `eval_period`, then iteratively predicts the next point, compares it to the observed value, and incorporates that value back into the training history.

## 🧠 Core Logic Stages

### 1. Data Preparation and Cutoff
* **Standardization:** The input data is sorted by date and converted to **datetime objects** to ensure proper time-series alignment.
* **Partitioning:** The dataset is split into an **Initial Training Set** (all data before the cutoff) and an **Evaluation Set** (the rolling forecast window).

### 2. Walk-Forward Loop (Sequential Testing)
* **Model Fitting:** For every point in the evaluation set, a new **Prophet model** is initialized with weekly and yearly seasonality enabled.
* **One-Step Forecast:** The model generates a prediction (`yhat`) and an uncertainty interval (`yhat_lower`, `yhat_upper`) specifically for the **next single point**.
* **Dynamic Training Expansion:** After each prediction, the actual observed value is appended to the training data. This ensures the model learns from the most recent information before making the next prediction.
* **Robust Error Handling:** If the Prophet fit fails, the function falls back to a **baseline persistence model** (last observed value) to prevent pipeline failure.

### 3. Anomaly Classification
* **Uncertainty Bounds:** Anomalies are defined by the `prophet_CI` parameter. Any observation falling outside the predicted upper or lower bounds is flagged.
* **Residual Calculation:** The function computes the **FB_residual** (Actual - Forecast) to quantify the magnitude of deviations.

## 📤 Key Output Columns
The function appends the following columns to the returned DataFrame:
* **`FB_forecast`**: The point estimate predicted by Prophet for that date.
* **`FB_low` / `FB_high`**: The dynamic boundaries based on the specified uncertainty interval.
* **`FB_residual`**: The difference between the actual observed metric and the forecast.
* **`FB_anomaly`**: A categorical label designating the deviation as **"high"** or **"low"**.
* **`is_FB_anomaly`**: A boolean flag identifying outliers in the evaluation region.


## 💡 Usage Context
This approach is highly effective for metrics with **strong seasonality and complex trends**. Because it uses a walk-forward loop, it is significantly more accurate than a static forecast for long evaluation periods, as it corrects itself based on the most recent trends. It is ideal for detecting "sudden" shifts that standard statistical models (like Z-Score) might miss.

---
### 📊 Evaluation Strategy
This function strictly ignores the training region for anomaly reporting, ensuring that all reported anomalies are based on "out-of-sample" performance where the model had no prior knowledge of the specific data point being tested.

---
## 📊 Evaluation Plot
The plot below shows an example of how the FB Prophet model sets bounds and anomaly regions:
"""


dbscan_msg = """
# 🌀 DBSCAN Walk-Forward Anomaly Detection
---

The `detect_time_series_anomalies_dbscan` function implements a **density-based clustering** approach for time-series anomaly detection. It utilizes an **iterative walk-forward validation** strategy to identify data points that exist in "low-density" regions of the feature space.

## 📋 Functional Overview
This function transforms a univariate time series into a high-dimensional feature space using **dynamic lags** and **rolling statistics**. It then applies the **DBSCAN** (Density-Based Spatial Clustering of Applications with Noise) algorithm to distinguish between dense clusters of "normal" behavior and sparse "noise" points (anomalies).



## 🧠 Core Logic & Helper Utilities

### 1. Dynamic Feature Engineering (`get_dynamic_lags`)
Instead of using fixed lags, the function uses the **Autocorrelation Function (ACF)** to find the 10 most significant seasonal patterns in the data.
* **Baseline:** Always includes lags 1, 2, and 3 to capture immediate momentum.
* **Significance:** Uses a 75% confidence interval ($\\\\alpha=0.25$) to identify meaningful historical dependencies.

### 2. Automated Parameter Tuning (`find_optimal_epsilon`)
DBSCAN is highly sensitive to the **Epsilon ($\\\\epsilon$)** parameter (the neighborhood radius). 
* **Proxy Elbow Method:** The function automatically calculates $\\\\epsilon$ by analyzing the distance to the $k$-th nearest neighbor for all training points.
* **Density Threshold:** It sets $\\\\epsilon$ at the **95th percentile** of these distances, ensuring that 95% of training data is considered "dense" while the most isolated 5% are candidates for noise.

### 3. Walk-Forward Iteration
For each period in the `eval_period`:
* **Feature Construction:** Builds a matrix containing the variable, its dynamic lags, rolling means, rolling standard deviations, and a linear trend component.
* **Scaling:** Fits a `StandardScaler` **only on training data** to prevent data leakage.
* **Novelty Detection:** Since DBSCAN cannot "predict" on new points, the function uses a **Nearest Neighbors proxy**. If the distance from a new test point to its $k$-th neighbor in the training set is greater than the trained $\\\\epsilon$, it is flagged as an anomaly.

## 📤 Key Output Columns
* **`dbscan_score`**: The distance from the point to the $\\\\epsilon$ boundary (positive values indicate anomalies).
* **`is_DBSCAN_anomaly`**: A boolean flag identifying outliers.
* **Generated Features**: Includes all dynamic lags (`lagX`) and rolling statistics (`roll_mean_W`) used during the fit.

## 💡 Usage Context
DBSCAN is exceptionally powerful for detecting **contextual anomalies**—points that might look "normal" in value but are "weird" given their recent history or seasonal context. Because it is density-based, it can find anomalies in non-linear or multi-modal distributions where simple percentile or Z-score methods would fail.

---
### ⚠️ Performance Note
This model is computationally more intensive than statistical methods due to the iterative re-fitting of the `NearestNeighbors` and `DBSCAN` models. It is best suited for high-priority metrics where accuracy is more critical than processing speed.

---
## 📊 Evaluation Plot
The plot below shows an example of how the DBSCAN model flags anomalies:
"""


ewma_msg = """
# 📉 EWMA Rolling Anomaly Detection
---

The `ewma_with_anomalies_rolling_group` function implements a **statistically weighted** approach to identifying outliers. It uses an **Expanding Window** (Walk-Forward) strategy to adapt to recent trends while maintaining a memory of historical data.

## 📋 Functional Overview
This function calculates the **Exponentially Weighted Moving Average (EWMA)**, which assigns higher importance to recent observations. By combining this forecast with a dynamic standard deviation "envelope," the function identifies points that deviate significantly from the expected trend.



## 🧠 Core Logic Components

### 1. Forecast Engine (`ewma_forecast`)
* **Weighting Mechanism:** Uses an `alpha` parameter (between 0 and 1) to determine the "decay" of information. A **higher alpha** makes the model more sensitive to recent changes.
* **Calculation:** Employs the formula:
  $$EWMA_t = \\alpha \\cdot Y_t + (1 - \\alpha) \\cdot EWMA_{t-1}$$

### 2. The Rolling Anomaly Loop
The function partitions data into **TRAIN** and **TEST** sets and iterates through the evaluation period:
* **Expanding Training Set:** For every evaluation point, the function uses all preceding data to re-calculate the baseline.
* **Dynamic Thresholding:** * **Upper Limit:** `Forecast + (Sigma * Standard Deviation)`
    * **Lower Limit:** `max(Forecast - (Sigma * Standard Deviation), 0)`
* **Iterative Evaluation:** It forecasts exactly **one point ahead**, checks for an anomaly, and then moves that point into the training set for the next iteration.

## 📤 Key Output Columns
The function returns a concatenated DataFrame containing:
* **`EWMA_forecast`**: The predicted value for that timestamp.
* **`STD`**: The standard deviation used to calculate the threshold.
* **`EWMA_high` / `EWMA_low`**: The dynamic boundaries (the "envelope") for the test period.
* **`set`**: Labels data as either **"TRAIN"** (historical baseline) or **"TEST"** (anomaly detection window).
* **`is_EWMA_anomaly`**: A boolean flag indicating if the actual value fell outside the limits.

## 💡 Usage Context
EWMA is ideal for **streaming-style data** or metrics that exhibit **level shifts**. Because it weights recent data more heavily than a simple moving average, it is faster to adapt to new "normals" while still filtering out minor noise.

---
### ⚙️ Parameter Tuning
* **`alpha`**: Adjust this to control how quickly the model "forgets" old data (Typical range: `0.1 - 0.3`).
* **`sigma`**: Adjust this to control sensitivity. A **lower sigma** results in more anomalies, while a **higher sigma** (e.g., `3.0`) only flags extreme outliers.

---
## 📊 Evaluation Plot
The plot below shows an example of how the EWMA model sets bounds and anomaly regions:
"""


isofor_msg = """
# 🌲 Isolation Forest Time-Series Anomaly Detection
---

The `detect_time_series_anomalies_isoforest` function implements an **unsupervised machine learning** approach to outlier detection. Unlike traditional statistical models that define "normal" regions, this model explicitly identifies anomalies by **isolating** them in a high-dimensional feature space.

## 📋 Functional Overview
This function utilizes a **walk-forward validation** strategy. For every evaluation point, it dynamically engineers a unique feature set, fits a forest of decision trees, and determines if the current observation is an outlier based on how easily it can be isolated from historical data.



## 🧠 Core Logic & Helper Utilities

### 1. Dynamic Feature Engineering (`get_dynamic_lags`)
To capture the temporal structure of the data, the model doesn't just look at the raw value; it looks at the **context**.
* **Autocorrelation (ACF):** The function calculates the **10 most significant lags** based on the data's historical patterns.
* **Momentum:** It always includes lags 1, 2, and 3 to ensure immediate short-term trends are captured.
* **Rolling Statistics:** It automatically calculates **rolling means** and **standard deviations** at multiple scales (quarter-lag, half-lag, and full-lag intervals).

### 2. Isolation Forest Model Configuration
The model builds **200 trees** (`n_estimators`) to ensure a stable anomaly score.
* **Contamination:** A baseline assumption that **1%** of the data is inherently noisy.
* **Decision Function:** The model calculates an anomaly score where lower, more negative values indicate a higher likelihood of being an outlier.

### 3. Dual-Threshold Validation
To reduce "false positives," the function uses two layers of verification:
1.  **Contamination Anomaly:** The standard output from the sklearn model based on the 1% threshold.
2.  **Statistical Threshold:** A custom "safety" bound calculated as:
    > $$Mean(Positive Scores) - 3 \\times Std(Positive Scores)$$
**Result:** A point is only flagged as `True` if **both** the ML model and the statistical threshold agree it is an anomaly.

## 📤 Key Output Columns
* **`IsolationForest_timeseries_score`**: The decision score (anomaly score).
* **`is_IsolationForest_timeseries_anomaly`**: The final boolean flag for anomalies.
* **Engineered Features**: All `lagX`, `roll_meanX`, and `roll_stdX` columns created during the process.

## 💡 Usage Context
Isolation Forest is exceptionally powerful for **multi-dimensional anomalies**. Because it considers lags, rolling stats, and trend simultaneously, it can detect "subtle" anomalies where the value might look normal, but the **relationship** between the value and its recent history is broken.

---
### ⚙️ Implementation Strategy
The function handles the "test" points one-by-one in a loop. After each prediction, the training set expands to include the latest observed value, ensuring the forest is always aware of the most recent data trends before predicting the next point.

---
## 📊 Evaluation Plot
The plot below shows an example of how the Isolation Forest model flags anomalies:
"""


mad_msg = """
# 🛡️ MAD Anomaly Detection Model
---

Median Absolute Deviation with Expanding Window

The detect_outliers_mad function is a non-parametric outlier detection tool. Unlike methods based on the standard deviation, this model uses the Median and MAD, making it significantly more robust against data that contains extreme outliers or non-normal distributions.

## 📋 Functional Overview

The function identifies anomalies by calculating how far a data point deviates from the median. It utilizes an expanding window approach to ensure that as the dataset grows, the definition of "normal" behavior adapts dynamically to the historical context.

## 🧠 Core Logic Stages

1. Preprocessing & Validation
Sample Size Check: Requires a minimum of 10 data points. If the group is too small, it returns an empty DataFrame to avoid biased statistical results.
Deep Copy: Operates on a group.copy() to ensure the original input data remains untouched.

2. Initial Training Block
Baseline Calculation: For the first part of the series (pre-evaluation period), it establishes a static baseline.
The MAD Formula: > It calculates the Median Absolute Deviation: $MAD = median(|x_i - median(x)|)$.
Thresholding: It uses a mad_scale_factor (default 0.6745) to make the MAD comparable to a standard deviation for a normal distribution.
Bounds:
    MAD_high: $Median + (Threshold \times \frac{MAD}{Scale})$
    MAD_low: $max(Median - (Threshold \times \frac{MAD}{Scale}), 0)$

3. Expanding Window Evaluation
Incremental Testing: For each point in the evaluation period, the function recalculates the Median and MAD using all data available up to that point.
Real-time Simulation: This simulates a "production" environment where each new weekly point is tested against the entirety of its known history.
Zero-Variance Handling: If MAD is 0 (all historical values are identical), the bounds collapse to the median value to avoid division errors.

## 📤 Key Output Columns

## 💡 Usage Context

The MAD model is the "gold standard" for univariate outlier detection in robust statistics. It is highly recommended for:
- Data with large, extreme spikes that would skew a Mean-based (SD) model.
- Datasets that are not normally distributed.
- Scenarios where you need a conservative, reliable boundary that isn't easily shifted by a single bad data point.

---
## 📊 Evaluation Plot
The plot below shows an example of how the MAD model sets bounds and anomaly regions:
"""


sd_msg = """
# 📈 Standard-Deviation–Based Outlier Detection (Expanding Window)

## **Function:** `detect_outliers_sd`

This function detects **anomalies in a time series** using a **mean ± 2 standard deviation (SD)** rule, applied in a **train–test, expanding-window framework**.

---

## 🔍 **What the Function Does**

### **1. Minimum Data Requirement**
- Requires **at least 10 observations**
- Returns an empty DataFrame if insufficient data is provided

---

## 🏋️ **Training Phase**
*(Initial fixed window)*

- Uses all observations **prior to the evaluation period**
- Computes:
  - **Mean**
  - **Standard Deviation**
  - **Lower bound:** `max(mean − 2 × SD, 0)`
  - **Upper bound:** `mean + 2 × SD`
- Flags anomalies where values fall **outside the 2-SD range**
- Labels rows as **TRAIN**

---

## 🔁 **Evaluation Phase**
*(Expanding window)*

For each step in the evaluation period:
- Expands the training window to include all prior observations
- Recomputes **mean and SD dynamically**
- Recalculates anomaly bounds
- Tests the current observation against updated bounds
- Labels rows as **TEST**

---

## 🚨 **Anomaly Classification**

Each observation receives:
- **`SD_anomaly`** → categorical label via `classify()`
- **`is_SD_anomaly`** → boolean flag  
  - `True` if outside ±2 SD  
  - `False` otherwise

---

## 📊 **Output Columns Added**

- **Mean**
- **SD**
- **SD2_low**
- **SD2_high**
- **set** (`TRAIN` or `TEST`)
- **SD_anomaly**
- **is_SD_anomaly**

---
## 📊 Evaluation Plot
The plot below shows an example of how the STD model sets bounds and anomaly regions:
"""
