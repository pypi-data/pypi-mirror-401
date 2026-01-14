import pandas as pd
import numpy as np
from .Preprocessing import classify

def detect_outliers_iqr(group, variable, date_column, eval_period):
    n = len(group)
    if n < 10:
        return pd.DataFrame(columns=group.columns)

    group = group.copy()
    # Explicitly ensure date_column is datetime right at the start
    group[date_column] = pd.to_datetime(group[date_column])
    train_size = n - eval_period

    # --- 1. HANDLE TRAINING DATA (Initial Block) ---
    # Calculate baseline IQR using all data available before eval_period
    initial_train = group[variable].iloc[:train_size]
    
    q1 = initial_train.quantile(0.25)
    q3 = initial_train.quantile(0.75)
    iqr = q3 - q1
    
    low = max(q1 - 1.5 * iqr, 0)
    high = q3 + 1.5 * iqr

    # Assign initial bounds to the training rows
    group.loc[group.index[:train_size], 'Q1'] = q1
    group.loc[group.index[:train_size], 'Q3'] = q3
    group.loc[group.index[:train_size], 'IQR'] = iqr
    group.loc[group.index[:train_size], 'IQR_low'] = low
    group.loc[group.index[:train_size], 'IQR_high'] = high
    group.loc[group.index[:train_size], 'set'] = "TRAIN"
    group.loc[group.index[:train_size], 'IQR_anomaly'] = group[variable].iloc[:train_size].apply(
        lambda x: classify(x, low, high)
    )
    group.loc[group.index[:train_size], 'is_IQR_anomaly'] = (
        (group[variable].iloc[:train_size] < low) | 
        (group[variable].iloc[:train_size] > high)
    )

    
    # --- 2. HANDLE EVALUATION DATA (Expanding Window) ---
    # Iterate through the eval period, increasing the training set one point at a time
    for i in range(train_size, n):
        # Data available up to this point (expanding)
        current_train = group[variable].iloc[:i]
        
        Q1 = current_train.quantile(0.25)
        Q3 = current_train.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_q = max(Q1 - 1.5 * IQR, 0)
        upper_q = Q3 + 1.5 * IQR
        
        # Test the current point i
        current_val = group[variable].iloc[i]
        group.iloc[i, group.columns.get_loc('Q1')] = Q1
        group.iloc[i, group.columns.get_loc('Q3')] = Q3
        group.iloc[i, group.columns.get_loc('IQR')] = IQR
        group.iloc[i, group.columns.get_loc('IQR_low')] = lower_q
        group.iloc[i, group.columns.get_loc('IQR_high')] = upper_q
        group.iloc[i, group.columns.get_loc('set')] = "TEST"
        group.iloc[i, group.columns.get_loc('IQR_anomaly')] = classify(current_val, lower_q, upper_q)
        group.iloc[i, group.columns.get_loc('is_IQR_anomaly')] = (current_val < lower_q) or (current_val > upper_q)

    # Cast boolean column properly
    group['is_IQR_anomaly'] = group['is_IQR_anomaly'].astype(bool)
    # FINAL SAFETY CHECK
    group[date_column] = pd.to_datetime(group[date_column])
    
    return group