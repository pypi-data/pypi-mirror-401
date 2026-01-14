import pandas as pd
import numpy as np
from datetime import date
from joblib import Parallel, delayed
from .helpers.percentile import detect_outliers_percentile
from .helpers.STD import detect_outliers_sd
from .helpers.MAD import detect_outliers_mad
from .helpers.IQR import detect_outliers_iqr
from .helpers.iso_forest_general import detect_outliers_isf_general
from .helpers.ewma import ewma_with_anomalies_rolling_group
from .helpers.fb_prophet import detect_time_series_anomalies_fb_walkforward
from .helpers.iso_forest_timeseries import detect_time_series_anomalies_isoforest
from .helpers.DB_scan import detect_time_series_anomalies_dbscan
from .helpers.Preprocessing import (create_full_calendar_and_interpolate, 
                                    print_anomaly_stats, 
                                    calculate_ensemble_scores,
                                    min_records_extraction)
from .helpers.evaluation_plots import summary_pie_plot, anomaly_stacked_bar_plot, avg_anomaly_score_plot, anomaly_eval_plot
from IPython.display import display, Markdown


def process_group(model, name, group, group_columns, variable,
                  date_column, alpha, sigma, eval_period, prophet_CI, contamination, random_state):

    if model == "ISF_general":
        return detect_outliers_isf_general(group, variable, contamination, random_state, eval_period)

    if model == "EWMA":
        return ewma_with_anomalies_rolling_group(
            group, group_columns, variable, date_column, alpha, sigma, eval_period
        )

    if model == "FB":
        return detect_time_series_anomalies_fb_walkforward(
            group, variable, date_column, eval_period, prophet_CI
        )
    
    if model == 'ISF_timeseries':
        return detect_time_series_anomalies_isoforest(
            group, variable, date_column, eval_period
        )
    
    if model == 'DBSCAN':
        return detect_time_series_anomalies_dbscan(
            group, variable, date_column, eval_period
        )
    

def run_pipeline(master_data, group_columns, variable,
                 date_column, freq, min_records,max_records,
                 contamination, random_state,
                 alpha, sigma, eval_period,
                 prophet_CI, mad_threshold, mad_scale_factor):
    
    if min_records is None:
        min_records = min_records_extraction(freq,eval_period)
        print(f"Min records needed to run an anomaly pipeline for a group is {min_records}")
        
    if max_records is not None:
        max_records = max_records + eval_period
        print(f"Max records used to run an anomaly pipeline for a group is {max_records}")

    # preprocess calendar
    final_data, success_report, exclusion_report = create_full_calendar_and_interpolate(
        master_data,
        group_columns,
        variable,
        date_column,
        freq,
        min_records,
        max_records
    )

    groups = list(final_data.groupby(group_columns))

  # Run in parallel (use all cores: n_jobs=-1)

        ## Percentile
    results_percentile  = []
    results_SD = []
    results_IQR = []
    results_MAD = []
    for name, group in groups:
        # percentile
        res_percentile = detect_outliers_percentile(group, variable, date_column, eval_period)
        results_percentile.append(res_percentile)
        
        # SD
        res_SD = detect_outliers_sd(group, variable, date_column, eval_period)
        results_SD.append(res_SD)
        
        # MAD
        res_MAD =  detect_outliers_mad(group, variable, date_column, mad_threshold, mad_scale_factor, eval_period)
        results_MAD.append(res_MAD)
        
        # IQR
        res_IQR = detect_outliers_iqr(group, variable, date_column, eval_period)
        results_IQR.append(res_IQR)

    anomaly_key_channel_percentile = pd.concat(results_percentile, ignore_index=True)
    
    #print("anomaly_key_channel_percentile data frame created")
    #print(anomaly_key_channel_percentile.head())
    
    anomaly_key_channel_SD = pd.concat(results_SD, ignore_index=True)
    SD_cols = group_columns+[date_column]+['Mean', 'SD', 'SD2_low', 'SD2_high','SD_anomaly',
       'is_SD_anomaly']
    anomaly_key_channel_SD_final =  anomaly_key_channel_SD[SD_cols]
    
    #print("anomaly_key_channel_SD data frame created")
    #print(anomaly_key_channel_SD.head())
    
    anomaly_key_channel_MAD = pd.concat(results_MAD, ignore_index=True)
    MAD_cols = group_columns+[date_column]+['Median', 'MAD', 'MAD_low', 'MAD_high','is_MAD_anomaly',
       'MAD_anomaly']
    anomaly_key_channel_MAD_final =  anomaly_key_channel_MAD[MAD_cols]
    
    #print("anomaly_key_channel_MAD data frame created")
    #print(anomaly_key_channel_MAD.head())
    
    anomaly_key_channel_IQR = pd.concat(results_IQR, ignore_index=True)
    IQR_cols = group_columns+[date_column]+['Q1', 'Q3', 'IQR', 'IQR_low', 'IQR_high','IQR_anomaly',
       'is_IQR_anomaly']
    anomaly_key_channel_IQR_final =  anomaly_key_channel_IQR[IQR_cols]
    
    #print("anomaly_key_channel_IQR data frame created")
    #print(anomaly_key_channel_IQR.head())
                                    
    
        ## ISF_general
    results_ISF_general = Parallel(n_jobs=-1, verbose=0)(delayed(process_group)('ISF_general', name, group, group_columns, variable,date_column, alpha, sigma, eval_period, prophet_CI, contamination, random_state) for name, group in groups)


        # Combine results back
    anomaly_key_channel_ISF_general= (
                pd.concat(results_ISF_general)
                  .sort_values(by=group_columns+[date_column])
            )
    #print("anomaly_key_channel_ISF_general data frame created")
    #print(anomaly_key_channel_ISF_general.head())
    
     ## EWMA
    results_EWMA = Parallel(n_jobs=-1, verbose=0)(
                delayed(process_group)('EWMA', name, group,group_columns, variable, date_column,
                                       alpha, sigma, eval_period, prophet_CI, contamination, random_state) for name, group in groups)


                # Combine results back
    anomaly_key_channel_EWMA= (
                    pd.concat(results_EWMA)
                      .sort_values(by=group_columns+[date_column])
                )
    #print("anomaly_key_channel_EWMA data frame created")
    #print(anomaly_key_channel_EWMA.head())
    EWMA_cols = group_columns+[date_column]+['alpha', 'sigma', 'EWMA_forecast',
       'STD', 'EWMA_high', 'EWMA_low',"EWMA_residual", "EWMA_anomaly",'is_EWMA_anomaly']

    anomaly_key_channel_EWMA_final =  anomaly_key_channel_EWMA[EWMA_cols]
        

    ## FB
    results_fb = Parallel(n_jobs=-1, verbose=0)(delayed(process_group)('FB', name, group,group_columns, variable,date_column,
                                  alpha, sigma, eval_period,prophet_CI, contamination, random_state) for name, group in groups)


        # Combine results back
    anomaly_key_channel_fb= (
                pd.concat(results_fb)
                  .sort_values(by=group_columns+[date_column])
            )

    #print("anomaly_key_channel_fb data frame created")
    #print(anomaly_key_channel_fb.head())
    FB_cols = group_columns+[date_column]+["FB_forecast","FB_low","FB_high",
                                                            "FB_residual","FB_anomaly","is_FB_anomaly"]

    anomaly_key_channel_fb_final =  anomaly_key_channel_fb[FB_cols]
        
       
        ## Isolation Forest timeseries
    results_ISF_timeseries = Parallel(n_jobs=-1, verbose=0)(
    delayed(process_group)('ISF_timeseries', name, group,group_columns, variable, date_column,
                                       alpha, sigma, eval_period, prophet_CI, contamination, random_state) for name, group in groups)


        # Combine results back
    anomaly_key_channel_ISF_timeseries= (
            pd.concat(results_ISF_timeseries)
              .sort_values(by=group_columns+[date_column])
        )
    #print(anomaly_key_channel_ISF_timeseries.head())
    ISF_cols = group_columns+[date_column]+["IsolationForest_score_timeseries", "IsolationForest_score_low_timeseries", "is_IsolationForest_anomaly_timeseries"]
    anomaly_key_channel_ISF_timeseries_final =  anomaly_key_channel_ISF_timeseries[ISF_cols]
    
    #print("anomaly_key_channel_ISF_timeseries data frame created")
    #print(anomaly_key_channel_ISF_timeseries.head())
    
       ## DB Scan 
    results_DB = Parallel(n_jobs=-1, verbose=0)(
    delayed(process_group)('DBSCAN', name, group,group_columns, variable, date_column,
                                       alpha, sigma, eval_period,prophet_CI, contamination, random_state) for name, group in groups)
    
     # Combine results back
    anomaly_key_channel_DB= (
                pd.concat(results_DB)
                  .sort_values(by=group_columns+[date_column])
            )
        
    
    #print("anomaly_key_channel_DB data frame created")
    #print(anomaly_key_channel_DB.head())
    
    DB_cols = group_columns+[date_column]+["dbscan_score", "dbscan_score_high", "is_DBSCAN_anomaly"]
    anomaly_key_channel_DB_final =  anomaly_key_channel_DB[DB_cols]

        # combine ISF general and timeseries data frames
    anomaly_key_channel_ISF = anomaly_key_channel_ISF_general.merge(anomaly_key_channel_ISF_timeseries_final, 
                                                                     on= group_columns+[date_column], how= 'inner') 
    
   
    # Column 1 Logic: If 'type' is train, take from 'col_A', else take from 'col_B'
    anomaly_key_channel_ISF['IsolationForest_score'] = np.where(anomaly_key_channel_ISF['set'] == 'TRAIN', 
                               anomaly_key_channel_ISF['IsolationForest_score_general'], 
                               anomaly_key_channel_ISF['IsolationForest_score_timeseries'])

    anomaly_key_channel_ISF['IsolationForest_score_low'] = np.where(anomaly_key_channel_ISF['set'] == 'TRAIN',
                               anomaly_key_channel_ISF['IsolationForest_score_low_general'], 
                               anomaly_key_channel_ISF['IsolationForest_score_low_timeseries'])

    # Column 2 Logic: If 'type' is train, take from 'IsolationForest_general', else take from 'IsolationForest_timeseries'
    anomaly_key_channel_ISF['is_IsolationForest_anomaly'] = np.where(anomaly_key_channel_ISF['set'] == 'TRAIN', 
                               anomaly_key_channel_ISF['is_IsolationForest_anomaly_general'], 
                               anomaly_key_channel_ISF['is_IsolationForest_anomaly_timeseries'])
    
    ISF_cols = group_columns+[date_column]+['IsolationForest_score', 'IsolationForest_score_low', 'is_IsolationForest_anomaly']
    anomaly_key_channel_ISF_final =  anomaly_key_channel_ISF[ISF_cols]
    
    
    #print("anomaly_key_channel_ISF data frame created")
    #print(anomaly_key_channel_ISF.head())
    
    
    # combine all the data frames       
        
    anomaly = anomaly_key_channel_percentile.merge(anomaly_key_channel_SD_final,  on= group_columns+[date_column], how='inner')
    anomaly = anomaly.merge(anomaly_key_channel_MAD_final,  on= group_columns+[date_column], how='inner')
    anomaly = anomaly.merge(anomaly_key_channel_IQR_final,  on= group_columns+[date_column], how='inner')
    anomaly = anomaly.merge(anomaly_key_channel_EWMA_final,  on= group_columns+[date_column], how='inner')
    anomaly = anomaly.merge(anomaly_key_channel_fb_final, on= group_columns+[date_column], how= 'inner')  
    anomaly = anomaly.merge(anomaly_key_channel_ISF_final, on= group_columns+[date_column], how= 'inner')  
    anomaly = anomaly.merge(anomaly_key_channel_DB_final, on= group_columns+[date_column], how= 'inner')  
    anomaly_final = calculate_ensemble_scores(anomaly, variable)
    globals()['anomaly_df'] = anomaly_final
    #print(anomaly_final.head())
    print(f"Successfully processed {len(success_report)} groups.")
    print(f"Excluded {len(exclusion_report)} groups due to low quality.")
    
    print_anomaly_stats(anomaly_final, group_columns)

    # Plot summary charts
    # ------------------------------
    
    # Get data for pie chart
    pie_chart_df = anomaly_final['is_Anomaly'].value_counts().reset_index()
    pie_chart_df['is_Anomaly'] = np.where(pie_chart_df['is_Anomaly'] == True, 'Anomalous Records', 'Evaluated Records')
    pie_chart_df = pie_chart_df.rename(columns={'is_Anomaly': 'Records'})
    if len(exclusion_report) > 0:
        pie_chart_df = pd.concat([pie_chart_df,
                                  pd.DataFrame({'Records': ['Dropped Records'], 'count': [exclusion_report['dropped_records'].sum()]})])
        exclusion_report = exclusion_report.drop(columns='dropped_records')
    print("")
    summary_pie_plot(pie_chart_df, title=f"Anomaly Detection Summary for {len(master_data[group_columns].drop_duplicates())} Groups")
    anomaly_stacked_bar_plot(anomaly_final, group_columns, variable, date_column)
    avg_anomaly_score_plot(anomaly_final, group_columns, date_column)
    
    top_5_anomaly_groups = anomaly_final.groupby(group_columns)['is_Anomaly'].agg(['mean', 'sum', 'count']).reset_index()\
        .sort_values('mean', ascending=False).reset_index(drop=True).head(5)

    eval_plots_msg = f"""
---
### Overall Evaluation Plots of the {len(top_5_anomaly_groups)} Groups with the Highest Anomaly Rates

Here is how to view detailed plots of individual anomaly detection models per group.\n
Start with the main (first) DataFrame returned from the timeseries_anomaly_detection function.\n
Suppose you called that DataFrame anomaly_df, that the group_columns are 'taxonomy' and 'channel', and that you want to see all the plots for the group where 'taxonomy' = 'tools' and 'channel' = 'mobile'.
Then you could run this code block:\n

```python
from anomaly_pipeline.helpers.evaluation_info import evaluation_info
from anomaly_pipeline.helpers.help_anomaly import help_anomaly

group_values = ['tools', 'mobile'] 
mask = anomaly_df[group_columns].eq(group_values).all(axis=1)
group_df = anomaly_df[mask]

evaluation_info(
    group_df,
    group_columns,
    variable,
    date_column,
    eval_period)
```
---
"""

    display(Markdown(eval_plots_msg))
    
    group_nbr = 1
    for group_key, group in top_5_anomaly_groups.groupby(group_columns, sort=False):
        anomaly_rate = group['mean'].values[0]
        group_df = anomaly_final.merge(group[group_columns], on=group_columns, how='inner')
        group_id = group_df[group_columns].drop_duplicates().astype(str).apply(lambda x: ' -- '.join(x), axis=1).values[0]
        group_msg = f"""#### #{group_nbr}, Anomaly Rate: {anomaly_rate:.1%}, Group: {group_id}"""
        display(Markdown(group_msg))
        anomaly_eval_plot(group_df, group_columns, variable, date_column, eval_period, show_anomaly_scores_on_main_plot=False)
        group_nbr += 1
    
    return anomaly_final, success_report, exclusion_report

