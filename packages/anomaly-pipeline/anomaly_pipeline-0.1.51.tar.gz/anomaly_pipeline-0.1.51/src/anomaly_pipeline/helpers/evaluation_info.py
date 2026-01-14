import pandas as pd
import numpy as np
from IPython.display import display, Markdown
from anomaly_pipeline.helpers.evaluation_plots import anomaly_eval_plot, anomaly_percentile_plot,\
    anomaly_sd_plot, anomaly_mad_plot, anomaly_iqr_plot, anomaly_ewma_plot, anomaly_fb_plot, anomaly_dbscan_plot, anomaly_isolation_forest_plot


def evaluation_info(
    eval_df,
    group_columns,
    variable,
    date_column,
    eval_period,
    models_to_plot=[]
    ):
    
    group_ids = eval_df[group_columns].drop_duplicates().reset_index(drop=True)
    group_cnt = len(group_ids)
    
    if group_cnt == 1 and len(models_to_plot) == 0:
        models_to_plot = ['overall', 'percentile', 'iqr', 'mad', 'std', 'ewma', 'prophet', 'dbscan', 'isolation_forest']
    elif group_cnt >= 2 and len(models_to_plot) == 0:
        models_to_plot = ['overall']
    
    record_cnt = len(eval_df)
    date_cnt = len(eval_df[date_column].drop_duplicates())
    anomaly_cnt = len(eval_df[eval_df['is_Anomaly'] == True])
    interpolated_cnt = len(eval_df[eval_df['is_missing_record'] == True])
    interpolation_method = 'linear'
    if interpolated_cnt >= 6:
        interpolated_records_msg = " Here is a view of 5 of the interpolated records:"""
    elif interpolated_cnt <= 5 and interpolated_cnt >= 2:
        interpolated_records_msg = f" Here is a view of the {interpolated_cnt} interpolated records:"
    elif interpolated_cnt == 1:
        interpolated_records_msg = " Here is a view of the 1 interpolated record:"
    else:
        interpolated_records_msg = ""
    
    if interpolated_cnt >= 1:
        interpolation_msg = f""" and values were interpolated using the {interpolation_method} method and {interpolated_cnt} additional records were added to the data.{interpolated_records_msg}"""
    else:
        interpolation_msg = ""
    
    no_eval_groups = (
        eval_df.groupby(group_columns)['is_Anomaly']\
        .agg(is_all_na=lambda x: x.isna().all(), historical_data_points='size')\
        .reset_index()
    )
    no_eval_groups = no_eval_groups[no_eval_groups['is_all_na'] == True].drop(columns='is_all_na').reset_index(drop=True)
    
    if len(no_eval_groups) >= 6:
        no_evals_sub_msg = f"Here are 5 of the {len(no_eval_groups)} groups that do not have enough historical data points:"
    elif len(no_eval_groups) >= 2 and len(no_eval_groups) <= 5:
        no_evals_sub_msg = f"Here are the {len(no_eval_groups)} groups that do not have enough historical data points:"
    elif len(no_eval_groups) == 1:
        no_evals_sub_msg = f"Here is the 1 group that does not have enough historical data points:"
    else:
        no_evals_sub_msg = ""

    no_evals_msg = f"""{len(no_eval_groups)} distinct group_column values did not have minimum number of historical data points to satisfy the period for evaluation that you specified.

To increase the chance of evaluating these records, lower the `eval_period` parameter, which controls which number of periods to evaluate.

{no_evals_sub_msg}
"""

    eval_msg1 = f"""## Anomaly Detection successfully ran on the `{variable}` column.

{group_cnt} distinct unique ID from group_columns values {'were' if group_cnt >= 2 else 'was'} evaluated on {'their' if group_cnt >= 2 else 'its'} last {eval_period} dates, which is {(eval_period/date_cnt):.0%} of the records in the data."""
    
    eval_msg2 = f"""
{interpolated_cnt} records were missing{interpolation_msg}.

{anomaly_cnt} records were identified as anomalous. This is {(anomaly_cnt/record_cnt):.0%} of the data.

### Preview of final table:"""
    
    plot_msg = """---
## Evaluation Plots"""

    display(Markdown(eval_msg1))
    
    if interpolated_cnt >= 1:
        display(eval_df[eval_df['is_missing_record'] == True].sample(min(interpolated_cnt, 5)))
    
    display(Markdown(eval_msg2))
    
    display(eval_df.head(10))
    
    if len(no_eval_groups) >= 1:
        display(Markdown(no_evals_msg))
        display(no_eval_groups.head(5))
    
    display(Markdown(plot_msg))
    
    # plot all specified model plots for all groups
    for row in group_ids.itertuples():
        group_df = pd.DataFrame([row._asdict()])[group_columns]
        group_df = eval_df.copy().merge(group_df, on=group_columns, how='inner')
        
        if len(group_df) > eval_period:
        
            for model in models_to_plot:
                if model == 'overall':
                    anomaly_eval_plot(group_df, group_columns, variable, date_column, eval_period=12, show_anomaly_scores_on_main_plot=False)
                elif model == 'percentile':
                    anomaly_percentile_plot(group=group_df, group_columns=group_columns, variable=variable, date_column=date_column, eval_period=eval_period, final_anomalies=False)
                elif model == 'iqr':            
                    anomaly_iqr_plot(group=group_df, group_columns=group_columns, variable=variable, date_column=date_column, eval_period=eval_period, final_anomalies=False)
                elif model == 'mad':
                    anomaly_mad_plot(group=group_df, group_columns=group_columns, variable=variable, date_column=date_column, eval_period=eval_period, final_anomalies=False)
                elif model == 'std':
                    anomaly_sd_plot(group=group_df, group_columns=group_columns, variable=variable, date_column=date_column, eval_period=eval_period, final_anomalies=False)
                elif model == 'ewma':
                    anomaly_ewma_plot(group=group_df, group_columns=group_columns, variable=variable, date_column=date_column, eval_period=eval_period, final_anomalies=False)
                elif model == 'prophet':
                    anomaly_fb_plot(group=group_df, group_columns=group_columns, variable=variable, date_column=date_column, eval_period=eval_period, final_anomalies=False)
                elif model == 'dbscan':
                    anomaly_dbscan_plot(group=group_df, group_columns=group_columns, variable=variable, date_column=date_column, eval_period=eval_period, final_anomalies=False)
                elif model == 'isolation_forest':
                    anomaly_isolation_forest_plot(group=group_df, group_columns=group_columns, variable=variable, date_column=date_column, eval_period=eval_period, final_anomalies=False)
