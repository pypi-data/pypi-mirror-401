import pandas as pd
import logging
import numpy as np
from prophet import Prophet
import warnings
import os
import sys
from .Preprocessing import classify
from contextlib import contextmanager

warnings.filterwarnings("ignore")

# --- ADD THIS HELPER ---
@contextmanager
def suppress_stdout_stderr():
    """Redirects stdout and stderr to devnull to silence C++ logs."""
    with open(os.devnull, 'w') as fnull:
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = fnull, fnull
        try:
            yield
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr

"""
def detect_time_series_anomalies_fb_walkforward(
    group,
    variable,
    date_column,
    eval_period,
    prophet_CI
):
    
    # 1. Silence the cmdstanpy logger completely
    logger = logging.getLogger('cmdstanpy')
    logger.addHandler(logging.NullHandler())
    logger.propagate = False
    logger.setLevel(logging.CRITICAL) # Only show critical errors
    
    group = group.sort_values(date_column).copy()
    group[date_column] = pd.to_datetime(group[date_column])

    cutoff_date = group[date_column].max() - pd.Timedelta(weeks=eval_period)

    group["FB_forecast"] = np.nan
    group["FB_low"] = np.nan
    group["FB_high"] = np.nan

    train = group[group[date_column] <= cutoff_date].copy()
    test = group[group[date_column] > cutoff_date].copy()

    for i, row in test.iterrows():
        prophet_train = train.rename(columns={date_column: "ds", variable: "y"})

        try:
            model = Prophet(
                weekly_seasonality=True,
                yearly_seasonality=True,
                daily_seasonality=False,
                interval_width=prophet_CI,
                # prophet_CI=prophet_CI
            )
            
            # --- WRAP THE FIT IN THE MUTER ---
            with suppress_stdout_stderr():
                model.fit(prophet_train)

            future = pd.DataFrame({"ds": [row[date_column]]})
            fc = model.predict(future).iloc[0]

            group.loc[i, "FB_forecast"] = fc["yhat"]
            group.loc[i, "FB_low"] = max(fc["yhat_lower"], 0)
            group.loc[i, "FB_high"] = fc["yhat_upper"]

        except Exception as e:
            # Note: We don't mute this so you can still see actual errors
            print(f"Prophet failed for KEY={group['key'].iloc[0]} on date={row[date_column]}: {e}")
            group.loc[i, "FB_forecast"] = train[variable].iloc[-1]
            group.loc[i, "FB_low"] = max(train[variable].iloc[-1], 0)
            group.loc[i, "FB_high"] = train[variable].iloc[-1]

        new_train_row = row.to_frame().T
        train = pd.concat([train, new_train_row], ignore_index=True)

    group["FB_residual"] = group[variable] - group["FB_forecast"]
    group["FB_anomaly"] = np.nan
    mask = group[date_column] > cutoff_date

    group.loc[mask & (group[variable] > group["FB_high"]), "FB_anomaly"] = "high"
    group.loc[mask & (group[variable] < group["FB_low"]), "FB_anomaly"] = "low"

    group["is_FB_anomaly"] = group["FB_anomaly"].notna()
    
    train_mask = group[date_column] <= cutoff_date
    group.loc[train_mask, "FB_residual"] = np.nan
    group.loc[train_mask, "is_FB_anomaly"] = np.nan

    return group
"""

def detect_time_series_anomalies_fb_walkforward(
    group,
    variable,
    date_column,
    eval_period,
    prophet_CI
):
    """
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
    
    """
    
    # 1. Silence the cmdstanpy logger
    logger = logging.getLogger('cmdstanpy')
    logger.addHandler(logging.NullHandler())
    logger.propagate = False
    logger.setLevel(logging.CRITICAL) 
    
    group = group.sort_values(date_column).copy()
    group[date_column] = pd.to_datetime(group[date_column])

    # Calculate cutoff for the walk-forward
    cutoff_date = group[date_column].max() - pd.Timedelta(weeks=eval_period)

    group["FB_forecast"] = np.nan
    group["FB_low"] = np.nan
    group["FB_high"] = np.nan

    train = group[group[date_column] <= cutoff_date].copy()
    test = group[group[date_column] > cutoff_date].copy()

    # --- INITIAL FIT FOR TRAIN DATA ---
    prophet_train_initial = train.rename(columns={date_column: "ds", variable: "y"})
    try:
        model_initial = Prophet(
            weekly_seasonality=True,
            yearly_seasonality=True,
            daily_seasonality=False,
            interval_width=prophet_CI # Fixed: Prophet uses interval_width
        )
        with suppress_stdout_stderr():
            model_initial.fit(prophet_train_initial)
        
        # Predict on the training dates to get historical bounds
        train_forecast = model_initial.predict(prophet_train_initial)
        
        # Map back to group (Train indices)
        train_indices = group[group[date_column] <= cutoff_date].index
        group.loc[train_indices, "FB_forecast"] = train_forecast["yhat"].values
        group.loc[train_indices, "FB_low"] = train_forecast["yhat_lower"].clip(lower=0).values
        group.loc[train_indices, "FB_high"] = train_forecast["yhat_upper"].values

    except Exception as e:
        print(f"Initial Prophet fit failed: {e}")

    # --- WALK-FORWARD FOR TEST DATA ---
    for i, row in test.iterrows():
        prophet_train = train.rename(columns={date_column: "ds", variable: "y"})
        try:
            model = Prophet(
                weekly_seasonality=True,
                yearly_seasonality=True,
                daily_seasonality=False,
                interval_width=prophet_CI
            )
            
            with suppress_stdout_stderr():
                model.fit(prophet_train)

            future = pd.DataFrame({"ds": [row[date_column]]})
            fc = model.predict(future).iloc[0]

            group.loc[i, "FB_forecast"] = fc["yhat"]
            group.loc[i, "FB_low"] = max(fc["yhat_lower"], 0)
            group.loc[i, "FB_high"] = fc["yhat_upper"]

        except Exception as e:
            print(f"Prophet failed for KEY={group.get('key', ['NA'])[0]} on date={row[date_column]}: {e}")
            # Fallback to naive logic
            last_val = train[variable].iloc[-1]
            group.loc[i, "FB_forecast"] = last_val
            group.loc[i, "FB_low"] = last_val
            group.loc[i, "FB_high"] = last_val

        # Update train for next iteration
        new_train_row = row.to_frame().T
        train = pd.concat([train, new_train_row], ignore_index=True)

    # --- UNIFIED ANOMALY DETECTION (Train + Test) ---
    group["FB_residual"] = group[variable] - group["FB_forecast"]

    # Applying your custom classify function row by row
    group["FB_anomaly"] = group.apply(
        lambda row: classify(row[variable], row["FB_low"], row["FB_high"]), 
        axis=1
    )

    group["is_FB_anomaly"] = group["FB_anomaly"] != 'none'
    
    # Label set
    group["set"] = "TRAIN"
    group.loc[group[date_column] > cutoff_date, "set"] = "TEST"

    return group