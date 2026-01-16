import pandas as pd
import numpy as np
from .Preprocessing import classify

def detect_outliers_sd(group, variable, date_column, eval_period):
    
    """
    # 📈 Standard-Deviation–Based Outlier Detection (Expanding Window)

    ## **Function:** `detect_outliers_sd`

    This function detects anomalies in a time series using a mean ± 2 standard deviation (SD) rule, applied in a train–test, expanding-window framework.

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
    - **is_SD_anomaly**"""
    
    n = len(group)
    # checking the min_size requirements
    if n < 10:
        return pd.DataFrame(columns=group.columns)

    group = group.copy()
    # Explicitly ensure date_column is datetime right at the start
    group[date_column] = pd.to_datetime(group[date_column])
    train_size = n - eval_period

    # --- 1. HANDLE TRAINING DATA (Initial Block) ---
    # Calculate baseline IQR using all data available before eval_period
    initial_train = group[variable].iloc[:train_size]
    
     # SD-based bounds
    mean = initial_train.mean()
    std = initial_train .std()
    
    lower_2sd = max(mean - 2*std,0)
    upper_2sd = mean + 2*std

    # Assign initial bounds to the training rows
    group.loc[group.index[:train_size], "Mean"] = mean
    group.loc[group.index[:train_size], 'SD'] = std
    group.loc[group.index[:train_size], 'SD2_low'] = lower_2sd 
    group.loc[group.index[:train_size], 'SD2_high'] = upper_2sd
    group.loc[group.index[:train_size], 'set'] = "TRAIN"
    group.loc[group.index[:train_size], 'SD_anomaly'] = group[variable].iloc[:train_size].apply(
        lambda x: classify(x, lower_2sd , upper_2sd)
    )
    group.loc[group.index[:train_size], 'is_SD_anomaly'] = (
        (group[variable].iloc[:train_size] < lower_2sd) | 
        (group[variable].iloc[:train_size] > upper_2sd)
    )

    
    # --- 2. HANDLE EVALUATION DATA (Expanding Window) ---
    # Iterate through the eval period, increasing the training set one point at a time
    for i in range(train_size, n):
        # Data available up to this point (expanding)
        current_train = group[variable].iloc[:i]
        
        MEAN = current_train.mean()
        STD = current_train.std()
        
        LOWER_2SD = max(MEAN - 2*STD,0)
        UPPER_2SD = MEAN + 2*STD
        
        # Test the current point i
        current_val = group[variable].iloc[i]
        group.iloc[i, group.columns.get_loc("Mean")] = MEAN
        group.iloc[i, group.columns.get_loc('SD')] = STD
        group.iloc[i, group.columns.get_loc('SD2_low')] = LOWER_2SD
        group.iloc[i, group.columns.get_loc('SD2_high')] = UPPER_2SD
        group.iloc[i, group.columns.get_loc('set')] = "TEST"
        group.iloc[i, group.columns.get_loc('SD_anomaly')] = classify(current_val, LOWER_2SD, UPPER_2SD)
        group.iloc[i, group.columns.get_loc('is_SD_anomaly')] = (current_val < LOWER_2SD) or (current_val > UPPER_2SD)

    # Cast boolean column properly
    group['is_SD_anomaly'] = group['is_SD_anomaly'].astype(bool)
    # FINAL SAFETY CHECK
    group[date_column] = pd.to_datetime(group[date_column])
    
    return group
   