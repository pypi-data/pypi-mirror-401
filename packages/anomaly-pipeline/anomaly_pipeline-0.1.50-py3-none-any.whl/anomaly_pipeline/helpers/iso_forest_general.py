import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_outliers_isf_general(group, variable, contamination=0.03, random_state=42, eval_period=12):
    n = len(group)
    if n < 10:
        return pd.DataFrame(columns=group.columns)

    group = group.copy()
    train_size = n - eval_period

    # Initialize columns
    group['set'] = ""
    group['IsolationForest_score_general'] = 0.0
    group['IsolationForest_score_low_general'] = 0.0
    group['is_IsolationForest_anomaly_general'] = False

    # --- 1. HANDLE TRAINING DATA (Initial Block) ---
    # Baseline ISF using all data available before eval_period
    initial_train = group[[variable]].iloc[:train_size]
    
    iso = IsolationForest(contamination=contamination, random_state=random_state)
    iso.fit(initial_train)
    
    # We use decision_function for the raw anomaly score
    group.loc[group.index[:train_size], 'IsolationForest_score_general'] = iso.decision_function(initial_train)
    group.loc[group.index[:train_size], 'IsolationForest_score_low_general'] = iso.offset_
    group.loc[group.index[:train_size], 'is_IsolationForest_anomaly_general'] = iso.predict(initial_train) == -1
    group.loc[group.index[:train_size], 'set'] = "TRAIN"

    # --- 2. HANDLE EVALUATION DATA (Expanding Window) ---
    # Iterate through the eval period, increasing the training set one point at a time
    for i in range(train_size, n):
        # Data available up to this point (expanding window)
        current_train = group[[variable]].iloc[:i]
        
        # Re-fit the model on all data known up to point i
        iso_expanding = IsolationForest(contamination=contamination, random_state=random_state)
        iso_expanding.fit(current_train)
        
        # Test the current point i
        current_point = group[[variable]].iloc[[i]]
        
        group.iloc[i, group.columns.get_loc('IsolationForest_score_general')] = iso_expanding.decision_function(current_point)[0]
        group.iloc[i, group.columns.get_loc('IsolationForest_score_low_general')] = iso_expanding.offset_
        group.iloc[i, group.columns.get_loc('is_IsolationForest_anomaly_general')] = iso_expanding.predict(current_point)[0] == -1
        group.iloc[i, group.columns.get_loc('set')] = "TEST"

    # Cast boolean column properly
    group['is_IsolationForest_anomaly_general'] = group['is_IsolationForest_anomaly_general'].astype(bool)
    
    return group