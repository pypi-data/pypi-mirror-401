import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.stattools import acf

def get_dynamic_lags(series: pd.Series) -> list:
    
    n = len(series)
    
    # Determine Max Lags (Max is min(50% of data, a hard cap of 60))
    nlags = min(int(n * 0.5), 60)
    
    if nlags < 5:
        return [1, 2, 3]

    # Calculate ACF and Confidence Intervals, get the 10 most-significant lags
    autocorrelations, confint = acf(series.dropna(), nlags=nlags, alpha=0.25, fft=True)
    autocorr_values = autocorrelations[1:]
    conf_limit = confint[1:, 1] - autocorr_values
    is_significant = np.abs(autocorr_values) > conf_limit
    significant_autocorr = autocorr_values[is_significant]
    significant_lags_indices = np.where(is_significant)[0] + 1
    ranked_indices = np.argsort(np.abs(significant_autocorr))[::-1]
    top_lags_indices = ranked_indices[:10]
    top_lags = significant_lags_indices[top_lags_indices].tolist()
    base_lags = [1, 2, 3]
    dynamic_lags = sorted(list(set(base_lags + top_lags)))[:10]
    
    return dynamic_lags

def detect_time_series_anomalies_isoforest(
    group,
    variable,
    date_column,
    eval_period,
    ):
    
    """
    # 🌲 Isolation Forest Time-Series Anomaly Detection
    ---

    The `detect_time_series_anomalies_isoforest` function implements an **unsupervised machine learning** approach to outlier detection.
    Unlike traditional statistical models that define "normal" regions, this model explicitly identifies anomalies by **isolating** them in a high-dimensional feature space.

    ## 📋 Functional Overview
    This function utilizes a **walk-forward validation** strategy. For every evaluation point, it dynamically engineers a unique feature set,
    fits a forest of decision trees, and determines if the current observation is an outlier based on how easily it can be isolated from historical data.



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
    Isolation Forest is exceptionally powerful for **multi-dimensional anomalies**.
    Because it considers lags, rolling stats, and trend simultaneously, it can detect "subtle" anomalies where the value might look normal,
    but the **relationship** between the value and its recent history is broken.

    ---
    ### ⚙️ Implementation Strategy
    The function handles the "test" points one-by-one in a loop. After each prediction, the training set expands to include the latest observed value,
    ensuring the forest is always aware of the most recent data trends before predicting the next point."""

    
    group[date_column] = pd.to_datetime(group[date_column])
    group = group.copy().sort_values(date_column).reset_index(drop=True)
    group['set'] = np.where(np.arange(len(group)) >= len(group) - eval_period, 'TEST', 'TRAIN')
    
    '''
    Iterate over each of the evaluation periods, fitting the model to all the data before the evaluation period
    and then getting the predicted anomaly score for the given evaluation period
    '''
    try:
        test_anom = []

        for t in list(range(eval_period - 1, -1, -1)):

            try:

                # Boundary between rolling train and rolling forecast region
                cutoff_date = group[date_column].max() - pd.Timedelta(weeks=t)

                # Get train set to determine lags
                model_group = group.copy()
                train = model_group[model_group[date_column] <= cutoff_date].copy()
                lags = get_dynamic_lags(train[variable])

                # Create lag features on the entire model_group DF
                for lag in lags:
                    model_group[f'lag{lag}'] = model_group[variable].shift(lag)

                # Get rolling stats features for the entire model_group DF
                rolling_stats_features = []    
                for w in [int(np.ceil(max(lags)/4)), int(np.ceil(max(lags)/2)), int(max(lags))]:
                    if w >= 3:
                        rolling_stats_features.append('roll_mean' + str(w))
                        rolling_stats_features.append('roll_std' + str(w))
                        model_group['roll_mean' + str(w)] = model_group[variable].shift(1).rolling(w).mean()
                        model_group['roll_std' + str(w)] = model_group[variable].shift(1).rolling(w).std()

                # Get trend feature
                model_group['trend'] = group.index

                # Drop records with NAs
                model_group = model_group.copy().dropna()

                # Split into train and test (train and test now both have all the features
                train = model_group[model_group[date_column] <= cutoff_date].copy()
                test = model_group[model_group[date_column] == cutoff_date].copy()

                # Identify all model features (lags, rolling stats, trend, and the variable itself)
                features = [f'lag{i}' for i in lags] + rolling_stats_features +  ['trend'] + [variable]

                # Create and fit the model
                iso_forest_model = IsolationForest(
                    n_estimators=200,
                    contamination=0.01,
                    random_state=42
                    )
                iso_forest_model.fit(train[features])

                train['IsolationForest_score_timeseries'] = iso_forest_model.decision_function(train[features])
                anomaly_threshold = min(0,
                    train[train['IsolationForest_score_timeseries'] > 0]['IsolationForest_score_timeseries'].mean() - 3 * train[train['IsolationForest_score_timeseries'] > 0]['IsolationForest_score_timeseries'].std())
                test['IsolationForest_score_timeseries'] = iso_forest_model.decision_function(test[features])
                test['contamination_anomaly'] = iso_forest_model.predict(test[features])  # -1 = anomaly, 1 = normal
                test['IsolationForest_score_low_timeseries'] = anomaly_threshold
                test['threshold_anomaly'] = np.where(test['IsolationForest_score_timeseries'] < anomaly_threshold, -1, 1)
                
                test['is_IsolationForest_anomaly_timeseries'] = np.where((test['contamination_anomaly'] == -1) & (test['threshold_anomaly'] == -1), True, False)
                test = test[[variable, date_column, 'IsolationForest_score_timeseries', 'IsolationForest_score_low_timeseries', 'is_IsolationForest_anomaly_timeseries']]
                test_anom.append(test)
            except:
                pass
        try:
            test_anom = pd.concat(test_anom)
            group = group.merge(test_anom[[variable,
                                           date_column,
                                           'IsolationForest_score_timeseries',
                                           'IsolationForest_score_low_timeseries',
                                           'is_IsolationForest_anomaly_timeseries']],
                                on=[variable, date_column],
                                how='left')
        except:
            print("Error in Isolation Forest process")
            group["IsolationForest_score_timeseries"] = np.nan
            group["IsolationForest_score_low_timeseries"] = np.nan
            group["is_IsolationForest_anomaly_timeseries"] = np.nan
    
    except:
        group["IsolationForest_score_timeseries"] = np.nan
        group["IsolationForest_score_low_timeseries"] = np.nan
        group["is_IsolationForest_anomaly_timeseries"] = np.nan
        # Get string or object dtype columns from group that would identify the group
        group_id = key_series.select_dtypes(include=['object', 'string']).columns.tolist()
        group_id = " ".join(key_series[group_id].reset_index(drop=True).iloc[0].to_list())
        print(f'Isolation Forest Anomaly Detection failed for {group_id}')
    
    return group
