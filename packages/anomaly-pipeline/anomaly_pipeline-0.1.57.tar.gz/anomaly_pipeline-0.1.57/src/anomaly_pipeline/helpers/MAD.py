import pandas as pd
import numpy as np
from .Preprocessing import classify



def detect_outliers_mad(group, variable, date_column, mad_threshold, mad_scale_factor, eval_period):
    
    """
    # 🛡️ MAD Anomaly Detection Model
    ---

    Median Absolute Deviation with Expanding Window

    The detect_outliers_mad function is a non-parametric outlier detection tool.
    Unlike methods based on the standard deviation, this model uses the Median and MAD,
    making it significantly more robust against data that contains extreme outliers or non-normal distributions.

    ## 📋 Functional Overview

    The function identifies anomalies by calculating how far a data point deviates from the median.
    It utilizes an expanding window approach to ensure that as the dataset grows,
    the definition of "normal" behavior adapts dynamically to the historical context.

    ## 🧠 Core Logic Stages

    1. Preprocessing & Validation
    Sample Size Check: Requires a minimum of 10 data points. If the group is too small, it returns an empty DataFrame to avoid biased statistical results.
    Deep Copy: Operates on a group.copy() to ensure the original input data remains untouched.

    2. Initial Training Block
    Baseline Calculation: For the first part of the series (pre-evaluation period), it establishes a static baseline.
    The MAD Formula: > It calculates the Median Absolute Deviation: MAD = median(|x_i - median(x)|).
    Thresholding: It uses a mad_scale_factor (default 0.6745) to make the MAD comparable to a standard deviation for a normal distribution.
    Bounds:
        MAD_high: Median + (Threshold x Scale)$
        MAD_low: max(Median - (Threshold x Scale), 0)$

    3. Expanding Window Evaluation
    Incremental Testing: For each point in the evaluation period, the function recalculates the Median and MAD using all data available up to that point.
    Real-time Simulation: This simulates a "production" environment where each new weekly point is tested against the entirety of its known history.
    Zero-Variance Handling: If MAD is 0 (all historical values are identical), the bounds collapse to the median value to avoid division errors.

    ## 📤 Key Output Columns

    ## 💡 Usage Context

    The MAD model is the "gold standard" for univariate outlier detection in robust statistics. It is highly recommended for:
    - Data with large, extreme spikes that would skew a Mean-based (SD) model.
    - Datasets that are not normally distributed.
    - Scenarios where you need a conservative, reliable boundary that isn't easily shifted by a single bad data point."""

    n = len(group)
    if n < 10:
        return pd.DataFrame(columns=group.columns)

    group = group.copy()
    # Explicitly ensure date_column is datetime right at the start
    group[date_column] = pd.to_datetime(group[date_column])
    train_size = n - eval_period

    # Initialize columns to store the expanding window metrics
    group['Median'] = np.nan
    group['MAD'] = np.nan
    group['MAD_low'] = np.nan
    group['MAD_high'] = np.nan
    group['set'] = ""
    group['is_MAD_anomaly'] = False

    # --- 1. HANDLE TRAINING DATA (Initial Block) ---
    initial_train = group[variable].iloc[:train_size]
    median = initial_train.median()
    mad = np.median(np.abs(initial_train - median))

    if mad == 0:
        lower_mad = median
        upper_mad = median
    else:
        margin = mad_threshold * mad / mad_scale_factor
        lower_mad = max(median - margin, 0)
        upper_mad = median + margin

    # Assign baseline values to the training block
    train_idx = group.index[:train_size]
    group.loc[train_idx, 'Median'] = median
    group.loc[train_idx, 'MAD'] = mad
    group.loc[train_idx, 'MAD_low'] = lower_mad
    group.loc[train_idx, 'MAD_high'] = upper_mad
    group.loc[train_idx, 'set'] = "TRAIN"
    group.loc[train_idx, 'MAD_anomaly'] = group[variable].iloc[:train_size].apply(
        lambda x: classify(x, lower_mad, upper_mad)
    )
    group.loc[train_idx, 'is_MAD_anomaly'] = (group[variable].iloc[:train_size] < lower_mad) | \
                                             (group[variable].iloc[:train_size] > upper_mad)
   

    # --- 2. HANDLE EVALUATION DATA (Expanding Window) ---
    for i in range(train_size, n):
        # Recursive growth: use all data up to the current point i
        current_train = group[variable].iloc[:i]
        
        curr_median = current_train.median()
        curr_mad = np.median(np.abs(current_train - curr_median))
        
        if curr_mad == 0:
            lower_mad = curr_median
            upper_mad = curr_median
        else:
            margin = mad_threshold * curr_mad / mad_scale_factor
            lower_mad = max(curr_median - margin, 0)
            upper_mad = curr_median + margin
            
        # Test current point i
        current_val = group[variable].iloc[i]
        
        group.iloc[i, group.columns.get_loc('Median')] = curr_median
        group.iloc[i, group.columns.get_loc('MAD')] = curr_mad
        group.iloc[i, group.columns.get_loc('MAD_low')] = lower_mad
        group.iloc[i, group.columns.get_loc('MAD_high')] = upper_mad
        group.iloc[i, group.columns.get_loc('set')] = "TEST"
        group.iloc[i, group.columns.get_loc('MAD_anomaly')] = classify(current_val, lower_mad, upper_mad)
        group.iloc[i, group.columns.get_loc('is_MAD_anomaly')] = (current_val < lower_mad) or (current_val > upper_mad)

    # If you have your classify function available:
    # group['MAD_anomaly'] = group.apply(lambda row: classify(row[variable], row['MAD_low'], row['MAD_high']), axis=1)

    group['is_MAD_anomaly'] = group['is_MAD_anomaly'].astype(bool)
    # FINAL SAFETY CHECK
    group[date_column] = pd.to_datetime(group[date_column])
    
    return group
    
   