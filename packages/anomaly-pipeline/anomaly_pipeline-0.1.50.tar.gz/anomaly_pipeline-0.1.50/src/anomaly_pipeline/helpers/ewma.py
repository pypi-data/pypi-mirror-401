import pandas as pd
import numpy as np
import statistics
from .Preprocessing import classify

# # EWMA functions

"""def ewma_forecast(train, alpha):
    Return last EWMA forecast value based on training data.
    ewma = train.ewm(alpha=alpha, adjust=False).mean()
    return ewma.iloc[-1]
"""

"""
def ew_std(series, alpha):
    
    Compute exponentially weighted standard deviation.
    Uses the same alpha as EWMA so recent points get more weight.

    Parameters
    ----------
    series : pandas Series of actual values
    alpha : float in (0,1)

    Returns
    -------
    float : exponentially weighted std deviation
    # mean
    
    mean = series.mean()
    #print(mean)

    # Squared deviation from the mean
    squared_diff = (series - mean) ** 2
    
    #print(squared_diff)

    # EWMA of squared deviation → variance
    ewma_var = squared_diff.ewm(alpha=alpha, adjust=False).mean()
    #print(ewma_var)
    #print(ewma_var.iloc[-1])

    # Std = sqrt(var)
    return np.sqrt(ewma_var.iloc[-1]) """

"""
def ewma_with_anomalies_rolling_group(group, group_columns, variable, date_column, alpha, sigma, eval_period):
    

    Rolling (expanding window) EWMA anomaly detection for a SINGLE GROUP ONLY.
    Expects `group` to already be filtered to one group.


    group = group.sort_values(date_column).reset_index(drop=True)
    n = len(group)

    train_size = n - eval_period  # rolling split

    # Build group key dictionary
    # group_columns can be list of multiple cols
    key_dict = {col: group[col].iloc[0] for col in group_columns}

    results = []

    for i in range(train_size, n):

        train = group.loc[:i-1, variable].astype(float)
        test_value = group.loc[i, variable]

        # --- EWMA + weighted STD ---
        ewma_train = train.ewm(alpha=alpha, adjust=False).mean()
        #last_std = ew_std(train, alpha)
        last_std = np.std(train)
        forecast = ewma_forecast(train, alpha)

        upper_limit = forecast + sigma * last_std
        lower_limit = max(forecast - sigma * last_std, 0)

        anomaly = True if (test_value > upper_limit or test_value < lower_limit) else False

        # TRAIN part (added only once)
        if i == train_size:
            train_part = pd.concat([
                group.loc[:i-1, group_columns].reset_index(drop=True),
                pd.DataFrame({
                    date_column: group.loc[:i-1, date_column].values,
                    "alpha": alpha,
                    "sigma":sigma,
                    "EWMA_forecast": ewma_train.values,
                    "STD": last_std,
                    "EWMA_high": np.nan,
                    "EWMA_low": np.nan,
                    "set": "TRAIN",
                    "is_EWMA_anomaly": pd.NA,
                })
            ], axis=1)

            results.append(train_part)

        # TEST row
        test_part = pd.DataFrame({
            **{col: [key_dict[col]] for col in key_dict},
            date_column: [pd.to_datetime(group.loc[i, date_column])],
            "alpha": [alpha],
            "sigma":[sigma],
            "EWMA_forecast": [forecast],
            "STD": [last_std],
            "EWMA_high": [upper_limit],
            "EWMA_low": [lower_limit],
            "set": ["TEST"],
            "is_EWMA_anomaly": [anomaly],
        })

        results.append(test_part)

    final_output = pd.concat(results, ignore_index=True)
    # Type Safety Check: Ensure the date column is always datetime before returning
    final_output[date_column] = pd.to_datetime(final_output[date_column])
    return final_output"""



def ewma_with_anomalies_rolling_group(group, group_columns, variable, date_column, alpha, sigma, eval_period):
    """
    Rolling (expanding window) EWMA anomaly detection for a SINGLE GROUP ONLY.
    Expects `group` to already be filtered to one group.

    # 📉 EWMA Rolling Anomaly Detection
    ---

    The `ewma_with_anomalies_rolling_group` function implements a **statistically weighted** approach to identifying outliers.
    It uses an **Expanding Window** (Walk-Forward) strategy to adapt to recent trends while maintaining a memory of historical data.

    ## 📋 Functional Overview
    This function calculates the **Exponentially Weighted Moving Average (EWMA)**, which assigns higher importance to recent observations.
    By combining this forecast with a dynamic standard deviation "envelope," the function identifies points that deviate significantly from the expected trend.



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
    EWMA is ideal for **streaming-style data** or metrics that exhibit **level shifts**.
    Because it weights recent data more heavily than a simple moving average, it is faster to adapt to new "normals" while still filtering out minor noise.

    ---
    ### ⚙️ Parameter Tuning
    * **`alpha`**: Adjust this to control how quickly the model "forgets" old data (Typical range: `0.1 - 0.3`).
    * **`sigma`**: Adjust this to control sensitivity. A **lower sigma** results in more anomalies, while a **higher sigma** (e.g., `3.0`) only flags extreme outliers.    
    """

    # 1. Prepare Data
    group = group.sort_values(date_column).reset_index(drop=True)
    vals = group[variable].astype(float)
    
    # 2. Calculate Statistics (Vectorized)
    # Shift(1) ensures we use history only (no data leakage)
    ewma_forecast = vals.ewm(alpha=alpha, adjust=False).mean().shift(1)
    std_expanding = vals.expanding().std().shift(1)
    
    # 3. Construct Output DataFrame
    results = group[group_columns + [date_column]].copy()
    results[variable] = vals
    results["alpha"] = alpha
    results["sigma"] = sigma
    
    # 4. Handle Nulls for the first two rows (The "Backfill" logic)
    # Backfilling allows us to have a baseline even for the very first point
    results["EWMA_forecast"] = ewma_forecast.bfill()
    results["STD"] = std_expanding.bfill().fillna(0) # fillna(0) in case there's only 1 row total
    
    # 5. Define Bounds (Now that nulls are handled)
    results["EWMA_high"] = results["EWMA_forecast"] + (sigma * results["STD"])
    results["EWMA_low"] = (results["EWMA_forecast"] - (sigma * results["STD"])).clip(lower=0)
    
    # 6. USE THE CLASSIFY FUNCTION
    # Note: Ensure 'classify' function is defined in your script!
    results["EWMA_anomaly"] = results.apply(
        lambda row: classify(row[variable], row["EWMA_low"], row["EWMA_high"]), 
        axis=1
    )
    
    # If the first row was backfilled, we should force it to 'none' 
    # to be safe since it's not a "real" statistical forecast.
    results.loc[0, "EWMA_anomaly"] = 'none'
    
    # 7. Final Flags and Labels
    results["is_EWMA_anomaly"] = results["EWMA_anomaly"] != 'none'
    results["EWMA_residual"] = vals - results["EWMA_forecast"]
    
    results["set"] = "TRAIN"
    if eval_period > 0 and len(results) >= eval_period:
        results.iloc[-eval_period:, results.columns.get_loc("set")] = "TEST"
        
    results[date_column] = pd.to_datetime(results[date_column])
    
    return results