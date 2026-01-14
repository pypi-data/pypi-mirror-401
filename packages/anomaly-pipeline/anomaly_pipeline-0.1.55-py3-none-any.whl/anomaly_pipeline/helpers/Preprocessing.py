import pandas as pd
import numpy as np
from datetime import datetime

def classify(val,lower,upper):
    if val < lower:
        return 'low'
    elif val > upper:
        return 'high'
    else:
        return 'none'

def create_full_calendar_and_interpolate(
        master_data,
        group_columns,
        variable,
        date_column,
        freq,
        min_records,
        max_records
    ):
    master_data[date_column] = pd.to_datetime(master_data[date_column])
    
    full_group_data = []
    success_metrics = []
    dropped_metrics = []

    for group_key, group in master_data.groupby(group_columns):
        # Create a dictionary of the group keys for structured reporting
        # This maps {col1: val1, col2: val2}
        current_group_info = {
            col: group_key[i] if isinstance(group_key, (tuple, list)) else group_key 
            for i, col in enumerate(group_columns)
        }
        
        # 1. Calendar Generation
        min_date, max_date = group[date_column].min(), group[date_column].max()
        full_dates = pd.date_range(start=min_date, end=max_date, freq=freq)
        
        if max_records is not None and len(full_dates) > max_records:
            full_dates = full_dates[-max_records:]

        # 2. Expansion
        calendar_dict = current_group_info.copy()
        calendar_dict[date_column] = full_dates
        full_calendar = pd.DataFrame(calendar_dict)

        # 3. Merge
        merged = full_calendar.merge(group, on=group_columns + [date_column], how="left")
        
        total_len = len(merged)
        interpolated_count = merged[variable].isna().sum()
        interpolation_rate = interpolated_count / total_len if total_len > 0 else 0

        # --- Check 1: Min Records ---
        if total_len < min_records:
            drop_entry = current_group_info.copy()
            drop_entry.update({
                "reason": "Below Min Records",
                "details": f"Total records {total_len} < {min_records}",
                "dropped_records": total_len
            })
            dropped_metrics.append(drop_entry)
            continue

        # --- Check 2: Max Interpolation Rate ---
        if interpolation_rate > 0.25:
            drop_entry = current_group_info.copy()
            drop_entry.update({
                "reason": "High Interpolation",
                "details": f"{interpolation_rate:.1%} > 25%",
                "dropped_records": total_len
            })
            dropped_metrics.append(drop_entry)
            continue

        # --- Success: Interpolate ---
        merged["is_missing_record"] = merged[variable].isna()
        merged[variable] = merged[variable].interpolate(method="linear", limit_direction="both")

        success_entry = current_group_info.copy()
        success_entry.update({
            "initial_records": len(group),
            "final_records": total_len,
            "interpolation_pct": round(interpolation_rate * 100, 2)
        })
        success_metrics.append(success_entry)
        full_group_data.append(merged)

    # Convert lists of dicts to DataFrames
    final_df = pd.concat(full_group_data, ignore_index=True) if full_group_data else pd.DataFrame()
    success_report = pd.DataFrame(success_metrics)
    exclusion_report = pd.DataFrame(dropped_metrics)
    
    return final_df, success_report, exclusion_report


def print_anomaly_stats(df, group_columns):
    # Calculate global stats
    total_records = len(df)
    # Ensure is_anomaly is treated as boolean for counting
    total_anomalies = df['is_Anomaly'].fillna(False).astype(bool).sum()
    anomaly_rate = (total_anomalies / total_records) * 100

    print("\n" + "="*45)
    print(f"{'ANOMALY DETECTION SUMMARY':^45}")
    print("="*45)
    print(f"{'Total Records:':<25} {total_records:,}")
    print(f"{'Total Anomalies:':<25} {total_anomalies:,}")
    print(f"{'Anomaly Rate:':<25} {anomaly_rate:.2f}%")
    print("-" * 45)

    # --- CHANGE START: Group by Rate ---
    print(f"Top 5 Groups by Anomaly Rate ({' > '.join(group_columns)}):")
    
    # 1. Group by keys
    # 2. Calculate mean (rate) and count (to show absolute numbers too)
    group_stats = df.groupby(group_columns)['is_Anomaly'].agg(['mean', 'sum']).sort_values(by='mean', ascending=False).head(5)
    
    for label, row in group_stats.iterrows():
        # Handle single vs multiple group columns for clean printing
        group_label = label if isinstance(label, str) else " | ".join(map(str, label))
        rate_pct = row['mean'] * 100
        count = int(row['sum'])
        
        # Print the Rate % and the absolute count in brackets for context
        print(f" - {group_label} : {rate_pct:.2f}% ({count} anomalies)")
    # --- CHANGE END ---
    
    print("="*45 + "\n")

def calculate_ensemble_scores(df, variable):
    """
    Calculates the normalized consensus score across all anomaly models.
    """
    
    # Identify all columns that are model flags (is_..._anomaly)
    anomaly_flags = [col for col in df.columns if col.startswith('is_') and col.endswith('_anomaly') and col != 'is_Anomaly']
    
    # 1. Total Votes (Count of True)
    df['Anomaly_Votes'] = df[anomaly_flags].sum(axis=1).astype(int)

    # 2. Total Models active for that row (Count of non-NaN values)
    df['Vote_Cnt'] = df[anomaly_flags].notna().sum(axis=1).astype(int)
    
    # 3. Anomaly Votes Score Display (-100 to 100)
    # Calculation: 200 * (percentage_yes - 0.5)
    df['Anomaly_Votes_Display'] = np.ceil(200 * (df['Anomaly_Votes'] / df['Vote_Cnt'] - 0.5)).astype(int)
    
    # 5. Final Boolean Consensus (e.g., majority rule)
    df['is_Anomaly'] = df['Anomaly_Votes'] / df['Vote_Cnt'] >= 0.5

    # 6. Scale all the model scores to be between -1 and 1
    try:
        df['Percentile_score_scaled'] = np.where(df['is_Percentile_anomaly'].isna()==False,
                                                 abs(df[variable] - (df['Percentile_high'] + df['Percentile_low'])/2)/((df['Percentile_high'] - df['Percentile_low'])/2) - 1,
                                                 np.nan)
        df['Percentile_score_scaled'] = df['Percentile_score_scaled']/abs(df['Percentile_score_scaled']).max()                                                       
    except:
        pass

    try:
        df['SD_score_scaled'] = np.where(df['is_SD_anomaly'].isna()==False,
                                         abs(df[variable] - (df['SD2_high'] + df['SD2_low'])/2)/((df['SD2_high'] - df['SD2_low'])/2) - 1,
                                         np.nan)
        df['SD_score_scaled'] = df['SD_score_scaled']/abs(df['SD_score_scaled']).max()                                                       
    except:
        pass

    try:
        df['MAD_score_scaled'] = np.where(df['is_MAD_anomaly'].isna()==False,
                                          abs(df[variable] - (df['MAD_high'] + df['MAD_low'])/2)/((df['MAD_high'] - df['MAD_low'])/2) - 1,
                                          np.nan)
        df['MAD_score_scaled'] = df['MAD_score_scaled']/abs(df['MAD_score_scaled']).max()                                                       
    except:
        pass

    try:
        df['IQR_score_scaled'] = np.where(df['is_IQR_anomaly'].isna()==False,
                                          abs(df[variable] - (df['IQR_high'] + df['IQR_low'])/2)/((df['IQR_high'] - df['IQR_low'])/2) - 1,
                                          np.nan)
        df['IQR_score_scaled'] = df['IQR_score_scaled']/abs(df['IQR_score_scaled']).max()                                                       
    except:
        pass

    try:
        df['EWMA_score_scaled'] = np.where(df['is_EWMA_anomaly'].isna()==False,
                                           abs(df[variable] - (df['EWMA_high'] + df['EWMA_low'])/2)/((df['EWMA_high'] - df['EWMA_low'])/2) - 1,
                                           np.nan)
        df['EWMA_score_scaled'] = df['EWMA_score_scaled']/abs(df['EWMA_score_scaled']).max()                                                       
    except:
        pass

    try:
        df['FB_score_scaled'] = np.where(df['is_FB_anomaly'].isna()==False,
                                         abs(df[variable] - (df['FB_high'] + df['FB_low'])/2)/((df['FB_high'] - df['FB_low'])/2) - 1,
                                         np.nan)
        df['FB_score_scaled'] = df['FB_score_scaled']/abs(df['FB_score_scaled']).max()                                                       
    except:
        pass

    try:
        df['IsoForest_score_scaled'] = np.where(df['is_IsolationForest_anomaly'].isna()==False,
                                                df['IsolationForest_score'] - df['IsolationForest_score_low'],
                                                np.nan)
        df['IsoForest_score_scaled'] = df['IsoForest_score_scaled']/abs(df['IsoForest_score_scaled']).max()
    except:
        pass

    try:
        df['dbscan_score_scaled'] = np.where(df['is_DBSCAN_anomaly'].isna()==False, df['dbscan_score_high'] - df['dbscan_score'], np.nan)
        df['dbscan_score_scaled'] = df['dbscan_score_scaled']/abs(df['dbscan_score_scaled']).max()                                                       
    except:
        pass
    
    score_scaled_cols = []
    for col in df.columns.to_list():
        if '_score_scaled' in col:
            score_scaled_cols.append(col)

    df['Anomaly_Score'] = df[score_scaled_cols].mean(axis=1)
    
    # Ensure that Anomaly_Scores of flagged anomalies are all higher than Anomaly_Scores of non-anomalies
    
    # Adjust Anomaly_Score so that if is_Anomaly then the Anomaly_Score >= 0.5
    if df['is_Anomaly'].sum() >= 1:
        if df[df['is_Anomaly'] == True]['Anomaly_Score'].min() < 0.5:
            df['Anomaly_Score'] = df['Anomaly_Score'] + (0.5 - df[df['is_Anomaly'] == True]['Anomaly_Score'].min())
    
    # Adjust Anomaly_Scores where is_Anomaly = False so that the max is < 0.5
    if len(df[df['is_Anomaly'] == False]) >= 1:
        if df[df['is_Anomaly'] == False]['Anomaly_Score'].max() > 0.5:
            non_anom_adj = df[df['is_Anomaly'] == False]['Anomaly_Score'].max() - 0.49
            df.loc[df['is_Anomaly'] == False, 'Anomaly_Score'] = df.loc[df['is_Anomaly'] == False, 'Anomaly_Score'] - non_anom_adj
    
    df['Anomaly_Score'] = df['Anomaly_Score']/abs(df['Anomaly_Score']).max()
    
    df['Anomaly_Score_Display'] = np.where(df['Anomaly_Score'] < 0, np.floor(100*df['Anomaly_Score']),
                                                        np.where(df['Anomaly_Score'].between(0, 1), np.ceil(100*df['Anomaly_Score']),
                                                                 np.where(df['Anomaly_Score'] > 1, 100, 0))).astype(int)
    
    # 7. Reposition is_Anomaly column to the end
    df['is_Anomaly'] = df.pop('is_Anomaly')

    return df



def min_records_extraction(freq,eval_period):
    freq_upper = freq.upper()
    
    if freq_upper.startswith('W'):
        annual_count = 52
    elif freq_upper.startswith('D') or freq_upper.startswith('B'):
        annual_count = 365
    elif freq_upper.startswith('M'):
        annual_count = 12
    else:
        # Fallback to weekly if custom/unknown
        annual_count = 52

    # Logic: 1 year for min, 2 years for max
    min_records = annual_count + eval_period
    #max_records = (2 * annual_count) + eval_period
    
    return min_records