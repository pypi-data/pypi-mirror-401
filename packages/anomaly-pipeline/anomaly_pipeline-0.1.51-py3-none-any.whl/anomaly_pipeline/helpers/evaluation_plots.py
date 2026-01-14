import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


def initialize_fig(group, group_columns, variable, date_column, anomaly_detection_model):
    
    plot_title = "  --  ".join(list(group[group_columns].values[0])).upper() + "  --  " + anomaly_detection_model
    
    fig = go.Figure()
    
    # Actuals
    fig.add_trace(go.Scatter(
        x=group[date_column],
        y=group[variable],
        mode='lines',
        line=dict(color='seagreen', width=1.5),
        name=variable if variable == variable.upper() else variable.title(),
    ))

    fig.update_layout(
        title=dict(
                text=plot_title,
                y=0.96,
                x=0.5,
                xanchor='center',
                yanchor='top',
                font=dict(size=18, color='black', weight='bold'),
            ),
        height=350,
        width=1200,
        margin=dict(l=50, r=50, t=40, b=30),
        plot_bgcolor='snow',
        paper_bgcolor='whitesmoke',
        xaxis=dict(
            range=[group[date_column].min(), group[date_column].max()],
            showline=True,
            linewidth=0.5,
            linecolor='orange',
            zeroline=False,
            gridcolor='rgba(255, 165, 0, 0.1)',
            mirror=True
            ),
        yaxis=dict(
            range=[group[variable].min()*0.9, group[variable].max()*1.06],
            showline=True,
            linewidth=0.5,
            linecolor='orange',
            zeroline=False,
            gridcolor='rgba(255, 165, 0, 0.1)',
            mirror=True
            ),
        yaxis_title=dict(
            text=variable.replace('_', ' ') if variable == variable.upper() else variable.title().replace('_', ' '),
            font=dict(size=16, weight='bold', color='black')
            ),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            )
        )
    
    return fig


def add_anomalies(fig, group, date_column, variable):
    # Add anomalies markers
    fig.add_trace(go.Scatter(
        x=group[group['is_Anomaly'] == True][date_column],
        y=group[group['is_Anomaly'] == True][variable],
        mode='markers',
        marker=dict(color='pink', symbol='cross', line=dict(width=1), size=9),
        name='Anomalies',
        hoverinfo='skip',
        ))
    return fig


def add_model_anomalies(fig, group, date_column, variable, model):
    fig.add_trace(go.Scatter(
        x=group[group[f'is_{model}_anomaly'] == True][date_column],
        y=group[group[f'is_{model}_anomaly'] == True][variable],
        mode='markers',
        marker=dict(color='palevioletred', symbol='circle', line=dict(width=1), size=9),
        name=f'{model} Anomalies',
        customdata=group[group[f'is_{model}_anomaly'] == True][[f'{model}_anomaly']],
        hovertemplate=(
            f'Date: %{{x|%Y-%m-%d}}<br>' +
            f'{variable if variable == variable.upper() else variable.title()}: %{{y:~.2s}}<br>' +
            f'{model}' + ' Category: %{customdata[0]}<extra></extra>'
            )
        ))
    return fig


def add_anomaly_region(fig, region, group, variable, date_column, threshold_column, threshold_label):
    
    if region == 'upper':
        y0 = group[threshold_column].values[0]
        y1 = group[variable].max()*1.06
    elif region == 'lower':
        y0 = 0
        y1 = group[threshold_column].values[0]
    
    # Shading
    fig.add_shape(
        type="rect",
        x0=0, x1=1, xref="paper",
        y0=y0, y1=y1,
        yref="y",
        fillcolor="rgba(255, 0, 0, 0.055)",
        line=dict(width=0),
        layer="below"
    )

    # Upper Percentile line
    fig.add_trace(go.Scatter(
        x=group[date_column],
        y=group[threshold_column],
        mode='lines',
        line=dict(color='orangered', width=1, dash='dashdot'),
        name=threshold_label,
        showlegend=False
        ))
    
    return fig


def add_eval_period_highlight(fig, group, date_column, variable, eval_period):
    fig.add_trace(go.Scatter(
        x=group[date_column][-eval_period:],
        y=group[variable][-eval_period:],
        mode='lines',
        line=dict(
            color='rgba(0, 255, 0, 0.25)', # 'lime' with 0.25 alpha
            width=10
        ),
        name='Evaluation Period',
        hoverinfo='skip',
    ))
    return fig


def anomaly_eval_plot(group, group_columns, variable, date_column, eval_period, show_anomaly_scores_on_main_plot=False):
    
    # IS ANOMALY Plot
    # This is the main plot
    """
    Generates an ensemble anomaly evaluation plot using Plotly.

    This function aggregates multiple anomaly detection models (columns starting with 'is_' 
    and ending with '_anomaly') to create a consensus 'Anomaly Score'. It visualizes 
    actual values, mean, median, and highlights points where the ensemble of models 
    agrees there is an anomaly.

    Args:
        group (pd.DataFrame): The processed dataframe containing original data and 
            boolean anomaly flags from various models (e.g., 'is_FB_anomaly').
        group_columns (list): List of column names used to identify the group 
            (e.g., ['Region', 'Product']).
        variable (str): The name of the numeric column being analyzed.
        date_column (str): The name of the datetime column.
        eval_period (int, optional): The number of recent periods evaluated. Defaults to 12.
        show_anomaly_scores_on_main_plot (bool, optional): If True, adds a secondary 
            Y-axis bar chart showing the normalized ensemble score (-100 to 100). 
            Defaults to False.

    Logic:
        - Voting: Counts all columns matching 'is_*_anomaly'.
        - is_Anomaly: True if >= 50% of the active models flag the point.
        - Anomaly Score: A normalized metric where 100 represents total consensus 
          among all models and negative values represent low-risk points.

    Returns:
        None: Displays an interactive Plotly figure.
    """
    try:
        group = group.copy()

        anomaly_cols = []
        for col in group.columns.to_list():
            if col.startswith('is_') and col.endswith('_anomaly') and col != 'is_anomaly':
                anomaly_cols.append(col)
        group['Anomaly Vote Models'] = group.apply(
            lambda row: sorted([col.removeprefix('is_').removesuffix('_anomaly')
                for col in anomaly_cols
                if pd.notna(row[col]) and row[col] == True]),
            axis=1)
        group['Anomaly Vote Models'] = group['Anomaly Vote Models'].apply(lambda x: ', '.join(x))
        group['Mean'] = group[variable].mean()
        group['Median'] = group[variable].median()

        fig = initialize_fig(group, group_columns, variable, date_column, "Anomalies")

        # Mean
        fig.add_trace(go.Scatter(
            x=group[date_column],
            y=group['Mean'],
            mode='lines',
            line=dict(color='maroon', width=0.7, dash='dash'),
            name='Mean',
            showlegend=True,
            hoverinfo='skip',
        ))

        # Median
        fig.add_trace(go.Scatter(
            x=group[date_column],
            y=group['Median'],
            mode='lines',
            line=dict(color='darkblue', width=0.7, dash='dot'),
            name='Median',
            showlegend=True,
            hoverinfo='skip',
        ))

        # Anomalies
        fig.add_trace(go.Scatter(
            x=group[group['is_Anomaly'] == True][date_column],
            y=group[group['is_Anomaly'] == True][variable],
            mode='markers',
            marker=dict(color='red', symbol='circle', line=dict(width=1), size=5*(group[group['is_Anomaly'] == True]['Anomaly_Score'] + 2)),
            name='Anomalies',
            customdata=group[group['is_Anomaly'] == True][['Anomaly_Votes_Display', 'Anomaly Vote Models', 'Anomaly_Score_Display']],
            hovertemplate=(
                f'Date: %{{x|%Y-%m-%d}}<br>' +
                f'{variable if variable == variable.upper() else variable.title()}: %{{y:,d}}<br>' +
                'Anomaly Votes: %{customdata[0]}<br>' +
                'Anomaly Vote Models: %{customdata[1]}<br>' +
                'Anomaly Score: %{customdata[2]}<extra></extra><br>'
                )
            ))

        # Near Anomalies
        fig.add_trace(go.Scatter(
            x=group[(group['is_Anomaly'] == False) & (group['Anomaly_Votes'] >= 1)][date_column],
            y=group[(group['is_Anomaly'] == False) & (group['Anomaly_Votes'] >= 1)][variable],
            mode='markers',
            marker=dict(color='orange',
                        symbol='circle',
                        line=dict(width=1),
                        size=5*(group[(group['is_Anomaly'] == False) & (group['Anomaly_Votes'] >= 1)]['Anomaly_Score'] + 2)),
            name='Not Quite Anomalies',
            customdata=group[(group['is_Anomaly'] == False) & (group['Anomaly_Votes'] >= 1)][['Anomaly_Votes_Display', 'Anomaly Vote Models', 'Anomaly_Score_Display']],
            hovertemplate=(
                f'Date: %{{x|%Y-%m-%d}}<br>' +
                f'{variable if variable == variable.upper() else variable.title()}: %{{y:,d}}<br>' +
                'Anomaly Votes: %{customdata[0]}<br>' +
                'Anomaly Vote Models: %{customdata[1]}<br>' +
                'Anomaly Score: %{customdata[2]}<extra></extra><br>'
                )
            ))

        # Add Anomaly Scores to Secondary Axis
        if show_anomaly_scores_on_main_plot:
            fig.add_trace(go.Bar(
                x=group[date_column],
                y=group['Anomaly_Score_Display'],
                name='Anomaly Score',
                marker=dict(
                    color=np.where(group['Anomaly_Score_Display'] > 0, 'rgba(255, 0, 0, 0.35)', 'rgba(128, 128, 128, 0.15)'),
                    # line=dict(width=0.5, color='gray')
                ),
                yaxis='y2',
                # Ensure it doesn't clutter the main hover box
                hoverinfo='y+name',
                showlegend=True
                ))

            fig.update_layout(
                yaxis2=dict(
                        title='Anomaly Score',
                        overlaying='y',
                        side='right',
                        range=[-105, 105],
                        showgrid=False,
                    ),
                margin=dict(l=50, r=200, t=50, b=50),
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.07,
                ))

        fig.show()
        print("\n")
        
    except Exception as e:
        print(f"Anomaly Plot Failed: {e}")


def anomaly_percentile_plot(group, group_columns, variable, date_column, eval_period, final_anomalies=True):
    # Percentile Model Plot
    """
    Visualizes anomaly detection based on Percentile-derived thresholds.

    This function plots the time-series data alongside shaded regions representing 
    the upper and lower percentile boundaries. It highlights specific 'Percentile' 
    model anomalies and can optionally overlay the final consensus anomalies.

    Args:
        group (pd.DataFrame): Dataframe containing the time-series data and 
            calculated percentile columns ('Percentile_low', 'Percentile_high', 
            and 'is_Percentile_anomaly').
        group_columns (list): Column names used for grouping/title identification.
        variable (str): The numeric column name being plotted on the Y-axis.
        date_column (str): The datetime column name for the X-axis.
        final_anomalies (bool, optional): If True, overlays the final ensemble 
            consensus markers (red circles) on top of the model-specific markers. 
            Defaults to True.
        eval_period (int, optional): The look-back period used for the evaluation 
            context. Defaults to 12.

    Logic:
        - Shading: Uses `add_anomaly_region` to fill the area beyond 'Percentile_low' 
          and 'Percentile_high'.
        - Model Markers: Highlights points where 'is_Percentile_anomaly' is True.
        - Integration: Uses helper functions `initialize_fig`, `add_anomaly_region`, 
          and `add_model_anomalies` to maintain a consistent UI/UX.

    Returns:
        None: Displays an interactive Plotly figure.
    """
    try:
        group = group.copy()
        fig = initialize_fig(group, group_columns, variable, date_column, "Percentile Anomaly Detection")
        # Lower anomaly region shading and threshold line
        fig = add_anomaly_region(fig, 'lower', group, variable, date_column, 'Percentile_low', 'Percentile Low')
        # Upper anomaly region shading and threshold line
        fig = add_anomaly_region(fig, 'upper', group, variable, date_column, 'Percentile_high', 'Percentile High')
        # Percentile Anomalies
        fig = add_model_anomalies(fig, group, date_column, variable, 'Percentile')
        # Add anomalies markers
        if final_anomalies:
            fig = add_anomalies(fig, group, date_column, variable)
        fig.show()
        print("\n")
    except Exception as e:
        print(f"Percentile Anomaly Plot Failed: {e}") 


def anomaly_sd_plot(group, group_columns, variable, date_column, eval_period, final_anomalies=True):
    # SD Model Plot
    """
    Visualizes anomaly detection based on Standard Deviation (SD) thresholds.

    This function plots the time-series data and overlays shaded regions representing 
    statistical boundaries (typically 2 or 3 standard deviations from the mean). 
    It identifies 'SD' model-specific anomalies and can optionally display the 
    final ensemble consensus markers.

    Args:
        group (pd.DataFrame): Dataframe containing the time-series data and 
            calculated SD boundary columns ('SD2_low', 'SD2_high', and 
            'is_SD_anomaly').
        group_columns (list): Column names used for grouping/title identification.
        variable (str): The numeric column name being plotted on the Y-axis.
        date_column (str): The datetime column name for the X-axis.
        final_anomalies (bool, optional): If True, overlays the final ensemble 
            consensus markers (red circles) on top of the SD model markers. 
            Defaults to True.
        eval_period (int, optional): The look-back period used for the evaluation 
            context. Defaults to 12.

    Logic:
        - Shading: Utilizes `add_anomaly_region` to fill the areas outside the 
          'SD2_low' and 'SD2_high' thresholds, visually representing the 
          statistical "outlier zones."
        - Model Markers: Highlights points where the SD model specifically 
          triggered an anomaly flag.
        - Visualization Helpers: Relies on `initialize_fig`, `add_anomaly_region`, 
          and `add_model_anomalies` for UI consistency across the pipeline.

    Returns:
        None: Displays an interactive Plotly figure and prints a newline.
    """
    try:
        group = group.copy()
        fig = initialize_fig(group, group_columns, variable, date_column, "SD Anomaly Detection")
        # Lower anomaly region shading and threshold line
        fig = add_anomaly_region(fig, 'lower', group, variable, date_column, 'SD2_low', 'SD Low')
        # Upper anomaly region shading and threshold line
        fig = add_anomaly_region(fig, 'upper', group, variable, date_column, 'SD2_high', 'SD High')
        # SD Anomalies
        fig = add_model_anomalies(fig, group, date_column, variable, 'SD')
        # Add anomalies markers
        if final_anomalies:
            fig = add_anomalies(fig, group, date_column, variable)
        fig.show()
        print("\n")
    except Exception as e:
        print(f"SD Anomaly Plot Failed: {e}")
        
        
def anomaly_mad_plot(group, group_columns, variable, date_column, eval_period, final_anomalies=True):
    # MAD Model Plot
    """
    Visualizes anomaly detection based on Median Absolute Deviation (MAD).

    MAD is a robust measure of statistical dispersion. This plot displays the 
    time-series data with shaded thresholds derived from the median and 
    the MAD scale factor. It is particularly effective for datasets where 
    mean and standard deviation are heavily skewed by extreme outliers.

    Args:
        group (pd.DataFrame): Dataframe containing the time-series data and 
            calculated MAD boundary columns ('MAD_low', 'MAD_high', and 
            'is_MAD_anomaly').
        group_columns (list): Column names used for grouping/title identification.
        variable (str): The numeric column name being plotted on the Y-axis.
        date_column (str): The datetime column name for the X-axis.
        final_anomalies (bool, optional): If True, overlays the final ensemble 
            consensus markers (red circles) on top of the MAD model markers. 
            Defaults to True.
        eval_period (int, optional): The look-back period used for the evaluation 
            context. Defaults to 12.

    Logic:
        - Shading: Highlights the areas outside the 'MAD_low' and 'MAD_high' 
          thresholds. Because MAD uses the median as a baseline, these bands 
          are often tighter and more resistant to outlier-driven "threshold bloat."
        - Model Markers: Specifically plots points flagged by the 'is_MAD_anomaly' 
          logic.
        - Helper Integration: Uses `initialize_fig` for layout and `add_anomalies` 
          for consensus overlay.

    Returns:
        None: Displays an interactive Plotly figure.
    """
    try:
        group = group.copy()
        fig = initialize_fig(group, group_columns, variable, date_column, "MAD Anomaly Detection")
        # Lower anomaly region shading and threshold line
        fig = add_anomaly_region(fig, 'lower', group, variable, date_column, 'MAD_low', 'MAD Low')
        # Upper anomaly region shading and threshold line
        fig = add_anomaly_region(fig, 'upper', group, variable, date_column, 'MAD_high', 'MAD High')
        # MAD Anomalies
        fig = add_model_anomalies(fig, group, date_column, variable, 'MAD')
        # Add anomalies markers
        if final_anomalies:
            fig = add_anomalies(fig, group, date_column, variable)
        fig.show()
        print("\n")
    except Exception as e:
        print(f"MAD Anomaly Plot Failed: {e}")


def anomaly_iqr_plot(group, group_columns, variable, date_column, eval_period, final_anomalies=True):
    """
    Visualizes anomaly detection based on the Interquartile Range (IQR).

    This function utilizes the Tukey's Fences method to identify outliers. It 
    calculates the spread between the 25th (Q1) and 75th (Q3) percentiles to 
    establish 'Normal' bounds. It is highly effective for skewed data as it 
    does not assume a normal distribution.

    Args:
        group (pd.DataFrame): Dataframe containing the time-series data and 
            calculated IQR boundary columns ('IQR_low', 'IQR_high', and 
            'is_IQR_anomaly').
        group_columns (list): Column names used for grouping/title identification.
        variable (str): The numeric column name being plotted on the Y-axis.
        date_column (str): The datetime column name for the X-axis.
        final_anomalies (bool, optional): If True, overlays the final ensemble 
            consensus markers (red circles) on top of the IQR-specific markers. 
            Defaults to True.
        eval_period (int, optional): The look-back period used for the evaluation 
            context. Defaults to 12.

    Logic:
        - Shading: Fills the region below Q1 - 1.5*IQR and above Q3 + 1.5*IQR.
        - Robustness: Because it uses quartiles rather than mean/SD, it is 
          resistant to being "fooled" by the outliers it is trying to detect.
        - Consistency: Uses the standard suite of helpers (`initialize_fig`, 
          `add_anomaly_region`) to match the rest of the pipeline's visual style.

    Returns:
        None: Displays an interactive Plotly figure.
    """
    # IQR Model Plot
    try:
        group = group.copy()
        fig = initialize_fig(group, group_columns, variable, date_column, "IQR Anomaly Detection")
        # Lower anomaly region shading and threshold line
        fig = add_anomaly_region(fig, 'lower', group, variable, date_column, 'IQR_low', 'IQR Low')
        # Upper anomaly region shading and threshold line
        fig = add_anomaly_region(fig, 'upper', group, variable, date_column, 'IQR_high', 'IQR High')
        # IQR Anomalies
        fig = add_model_anomalies(fig, group, date_column, variable, 'IQR')
        # Add anomalies markers
        if final_anomalies:
            fig = add_anomalies(fig, group, date_column, variable)
        fig.show()
        print("\n")
    except Exception as e:
        print(f"IQR Anomaly Plot Failed: {e}")


def anomaly_ewma_plot(group, group_columns, variable, date_column, eval_period, final_anomalies=True):
    """
    Visualizes anomaly detection based on Exponentially Weighted Moving Average (EWMA).

    This plot highlights anomalies using a moving baseline that gives more weight to 
    recent observations. It visualizes the EWMA forecast line, the calculated upper 
    and lower control limits (bands), and model-specific outliers. It is ideal for 
    detecting shifts in mean or variance in non-stationary time series.

    Args:
        group (pd.DataFrame): Dataframe containing the time-series data and 
            EWMA-specific columns ('EWMA_forecast', 'EWMA_low', 'EWMA_high', 
            and 'is_EWMA_anomaly').
        group_columns (list): Column names used for grouping and plot titles.
        variable (str): The name of the target numeric column.
        date_column (str): The name of the datetime column.
        final_anomalies (bool, optional): If True, overlays the final ensemble 
            consensus markers (red circles) on top of the EWMA markers. 
            Defaults to True.
        eval_period (int, optional): The number of recent periods evaluated. 
            Used for context in title or scaling. Defaults to 12.

    Logic:
        - Forecast Line: Displays the weighted moving average ('slateblue').
        - Dynamic Thresholds: Visualizes 'EWMA_low' and 'EWMA_high' as 'orangered' 
          dashdot lines with light red shading in the outlier zones.
        - Model Markers: Highlights points where the EWMA logic specifically 
          triggered an anomaly flag.

    Returns:
        None: Displays an interactive Plotly figure.
    """
    # EWMA Model Plot
    try:
        group = group.copy()
        fig = initialize_fig(group, group_columns, variable, date_column, "EWMA Anomaly Detection")
        # EWMA Forecast
        fig.add_trace(go.Scatter(
            x=group[date_column],
            y=group['EWMA_forecast'],
            mode='lines',
            line=dict(color='slateblue', width=0.5, dash='dashdot'),
            name='EWMA Forecast',
            showlegend=True
            ))
        # EWMA low line
        fig.add_trace(go.Scatter(
            x=group[date_column],
            y=group['EWMA_low'],
            mode='lines',
            line=dict(color='orangered', width=1, dash='dashdot'),
            name='EWMA Low',
            showlegend=False
            ))
        # Lower Shading
        fig.add_trace(go.Scatter(
            x=group[group['EWMA_low'].isna()==False][date_column],
            y=[0] * len(group[group['EWMA_low'].isna()==False]),
            mode="lines",
            line=dict(width=0),
            hoverinfo="skip",
            showlegend=False,
            fill="tonexty",
            fillcolor="rgba(255, 0, 0, 0.07)"
        ))
        # EWMA high line
        fig.add_trace(go.Scatter(
            x=group[date_column],
            y=group['EWMA_high'],
            mode='lines',
            line=dict(color='orangered', width=1, dash='dashdot'),
            name='EWMA High',
            showlegend=False,
            ))
        # Upper Shading
        fig.add_trace(go.Scatter(
            x=group[group['EWMA_high'].isna()==False][date_column],
            y=[group[variable].max() * 1.06] * len(group[group['EWMA_high'].isna()==False]),
            mode="lines",
            line=dict(width=0),
            hoverinfo="skip",
            showlegend=False,
            fill="tonexty",
            fillcolor="rgba(255, 0, 0, 0.07)"
            ))
        # EWMA Anomalies
        fig.add_trace(go.Scatter(
            x=group[group['is_EWMA_anomaly'] == True][date_column],
            y=group[group['is_EWMA_anomaly'] == True][variable],
            mode='markers',
            marker=dict(color='palevioletred', symbol='circle', line=dict(width=1), size=9),
            name='EWMA Anomalies',
            ))
        # Add anomalies markers
        if final_anomalies:
            fig = add_anomalies(fig, group, date_column, variable)
        fig.show()
        print("\n")
    except Exception as e:
        print(f"EWMA Anomaly Plot Failed: {e}")


def anomaly_fb_plot(group, group_columns, variable, date_column, eval_period, final_anomalies=True):
    """
    Visualizes anomaly detection using the Facebook Prophet (FB) model.

    This function displays the Prophet model's additive trend and seasonality 
    forecasts along with its uncertainty intervals (yhat_upper and yhat_lower). 
    It is particularly useful for identifying anomalies in data with strong 
    seasonality (weekly/yearly) that simpler statistical models might miss.

    Args:
        group (pd.DataFrame): Dataframe containing Prophet output columns 
            ('FB_forecast', 'FB_low', 'FB_high', and 'is_FB_anomaly').
        group_columns (list): Column names used to identify and title the group.
        variable (str): The name of the target numeric column analyzed.
        date_column (str): The name of the datetime column.
        final_anomalies (bool, optional): If True, overlays the final ensemble 
            consensus markers (red circles) over the Prophet markers. 
            Defaults to True.
        eval_period (int, optional): The number of recent periods analyzed. 
            Defaults to 12.

    Logic:
        - Recursive Visibility: Since FB Prophet is run in a walk-forward manner, 
          the shaded regions represent the prediction interval at the time 
          of forecast.
        - Outlier Zones: Shaded red areas represent values that fall outside 
          the model's expected confidence interval (based on `prophet_CI`).
        - Model Markers: Highlights points where Prophet specifically flagged 
          an anomaly based on its trend and seasonal expectations.

    Returns:
        None: Displays an interactive Plotly figure.
    """
    # FB Prophet Model Plot
    try:
        group = group.copy()
        fig = initialize_fig(group, group_columns, variable, date_column, "FB Prophet Anomaly Detection")    
        # FB Forecast
        fig.add_trace(go.Scatter(
            x=group[date_column],
            y=group['FB_forecast'],
            mode='lines',
            line=dict(color='slateblue', width=0.5, dash='dashdot'),
            name='FB Forecast',
            showlegend=True
            ))
        # Lower FB line
        fig.add_trace(go.Scatter(
            x=group[date_column],
            y=group['FB_low'],
            mode='lines',
            line=dict(color='orangered', width=1, dash='dashdot'),
            name='FB Low',
            showlegend=False
            ))
        # Lower Shading
        fig.add_trace(go.Scatter(
            x=group[group['FB_low'].isna()==False][date_column],
            y=[0] * len(group[group['FB_low'].isna()==False]),
            mode="lines",
            line=dict(width=0),
            hoverinfo="skip",
            showlegend=False,
            fill="tonexty",
            fillcolor="rgba(255, 0, 0, 0.07)"
        ))
        # Upper FB line
        fig.add_trace(go.Scatter(
            x=group[date_column],
            y=group['FB_high'],
            mode='lines',
            line=dict(color='orangered', width=1, dash='dashdot'),
            name='FB High',
            showlegend=False,
            ))
        # Upper Shading
        fig.add_trace(go.Scatter(
            x=group[group['FB_high'].isna()==False][date_column],
            y=[group[variable].max() * 1.06] * len(group[group['FB_high'].isna()==False]),
            mode="lines",
            line=dict(width=0),
            hoverinfo="skip",
            showlegend=False,
            fill="tonexty",
            fillcolor="rgba(255, 0, 0, 0.07)"
            ))
        # FB Anomalies
        fig.add_trace(go.Scatter(
            x=group[group['is_FB_anomaly'] == True][date_column],
            y=group[group['is_FB_anomaly'] == True][variable],
            mode='markers',
            marker=dict(color='palevioletred', symbol='circle', line=dict(width=1), size=9),
            name='FB Anomalies',
            ))
        # Add anomalies markers
        if final_anomalies:
            fig = add_anomalies(fig, group, date_column, variable)
        fig.show()
        print("\n")
    except Exception as e:
        print(f"FB Anomaly Plot Failed: {e}")


def anomaly_dbscan_plot(group, group_columns, variable, date_column, eval_period, final_anomalies=True):
    """
    Visualizes anomaly detection using the DBSCAN clustering algorithm.

    DBSCAN identifies anomalies as 'noise' points that reside in low-density 
    regions of the feature space. Unlike threshold-based methods, DBSCAN 
    looks for multi-dimensional patterns. This plot highlights points 
    flagged as noise by the algorithm, contextually placed within the 
    time-series trend.

    Args:
        group (pd.DataFrame): Dataframe containing the time-series data and 
            DBSCAN results (specifically the 'is_DBSCAN_anomaly' column).
        group_columns (list): Column names used to identify and title the group.
        variable (str): The name of the target numeric column analyzed.
        date_column (str): The name of the datetime column.
        final_anomalies (bool, optional): If True, overlays the final ensemble 
            consensus markers (red circles) over the DBSCAN markers. 
            Defaults to True.
        eval_period (int, optional): The number of recent periods to highlight 
            as the evaluation window. Defaults to 12.

    Logic:
        - Density Clustering: Points are flagged as anomalies if they are 
          isolated from the main "clusters" of data points in the feature space.
        - Eval Period Highlight: Uses `add_eval_period_highlight` to visually 
          distinguish the recent testing window from the historical training data.
        - Model Markers: Highlights specific DBSCAN outliers using 'mediumorchid' 
          circles.

    Returns:
        None: Displays an interactive Plotly figure.
    """
    # DBSCAN Model Plot
    try:
        group = group.copy()
        fig = initialize_fig(group, group_columns, variable, date_column, "DBSCAN Anomaly Detection")
        # Evaluation Period
        if eval_period >= 1:
            fig = add_eval_period_highlight(fig, group, date_column, variable, eval_period)
        # DBSCAN Anomalies
        fig.add_trace(go.Scatter(
            x=group[group['is_DBSCAN_anomaly'] == True][date_column],
            y=group[group['is_DBSCAN_anomaly'] == True][variable],
            mode='markers',
            marker=dict(color='mediumorchid', symbol='circle', line=dict(width=1), size=7),
            name='DBSCAN Anomalies',
            ))
        # Add anomalies markers
        if final_anomalies:
            fig = add_anomalies(fig, group, date_column, variable)
        fig.show()
        print("\n")
    except Exception as e:
        print(f"DBSCAN Anomaly Plot Failed: {e}")


def anomaly_isolation_forest_plot(group, group_columns, variable, date_column, eval_period, final_anomalies=True):
    """
    Visualizes anomaly detection using the Isolation Forest algorithm.

    Isolation Forest is an unsupervised learning algorithm that isolates anomalies 
    by randomly selecting a feature and a split value. Since anomalies are few 
    and different, they are easier to isolate (shorter path length in the tree). 
    This plot shows points identified as anomalies based on this branching logic.

    Args:
        group (pd.DataFrame): Dataframe containing time-series data and 
            Isolation Forest results (specifically 'is_IsolationForest_anomaly_timeseries').
        group_columns (list): Column names used to identify and title the group.
        variable (str): The name of the target numeric column analyzed.
        date_column (str): The name of the datetime column.
        final_anomalies (bool, optional): If True, overlays the final ensemble 
            consensus markers (red circles) over the Isolation Forest markers. 
            Defaults to True.
        eval_period (int, optional): The number of recent periods to highlight 
            as the evaluation window. Defaults to 12.

    Logic:
        - Tree-Based Isolation: Anomalies are identified by having shorter average 
          path lengths across a forest of random trees.
        - Temporal Context: Uses `add_eval_period_highlight` to shade the recursive 
          testing window, helping users see if anomalies are recent.
        - Model Markers: Highlights specific Isolation Forest outliers using 
          'mediumorchid' markers.

    Returns:
        None: Displays an interactive Plotly figure.
    """
    # Isolation Forest Model Plot
    try:
        group = group.copy()
        fig = initialize_fig(group, group_columns, variable, date_column, "Isolation Forest Anomaly Detection")
        # Evaluation Period
        if eval_period >= 1:
            fig = add_eval_period_highlight(fig, group, date_column, variable, eval_period)
        # Isolation Forest Anomalies
        fig.add_trace(go.Scatter(
            x=group[group['is_IsolationForest_anomaly'] == True][date_column],
            y=group[group['is_IsolationForest_anomaly'] == True][variable],
            mode='markers',
            marker=dict(color='mediumorchid', symbol='circle', line=dict(width=1), size=7),
            name='Isolation Forest Anomalies',
            ))
        # Add anomalies markers
        if final_anomalies:
            fig = add_anomalies(fig, group, date_column, variable)
        fig.show()
        print("\n")
    except Exception as e:
        print(f"Isolation Forest Time Series Anomaly Plot Failed: {e}")


def anomaly_stacked_bar_plot(df, group_columns, variable, date_column, anomaly_col='is_Anomaly'):
    """
    Generates a time-ordered stacked bar chart showing Normal vs. Anomalous record counts.

    Args:
        df (pd.DataFrame): The dataframe containing the data.
        date_column (str): The name of the datetime column.
        anomaly_col (str): The name of the boolean column (True=Anomaly).
        title (str): Title of the chart.

    Returns:
        None: Displays the interactive Plotly figure.
    """
    try:
        # 1. Aggregation
        # Group by date to get counts across all unique_ids for that specific timestamp
        # We count 'True' values for anomalies, and calculate 'Normal' as Total - Anomalies

        df['normal_val'] = np.where(df[anomaly_col] != True, df[variable], 0)
        df['anomaly_val'] = np.where(df[anomaly_col] == True, df[variable], 0)

        agg_df = df.groupby(date_column).agg(
                normal_sum=('normal_val', 'sum'),
                anomaly_sum=('anomaly_val', 'sum')
            ).reset_index()

        agg_df['total_sum'] = agg_df['normal_sum'] + agg_df['anomaly_sum']

        # Calculate percentage (handle division by zero just in case)
        agg_df['anomaly_pct'] = np.where(
            agg_df['total_sum'] > 0, 
            (agg_df['anomaly_sum'] / agg_df['total_sum']) * 100, 
            0
        )
        # 2. Initialize Figure
        fig = go.Figure()

        # 3. Add Traces
        # Bottom Bar: Non-Anomalous (Grey)
        fig.add_trace(go.Bar(
            x=agg_df[date_column],
            y=agg_df['normal_sum'],
            name='Normal',
            marker_color='silver',  # Grey/Silver for normal data
            customdata=agg_df[['total_sum']],
            hovertemplate=(
                f'<b>Date:</b> %{{x|%Y-%m-%d}}<br>' +
                f'<b>Normal Records:</b> %{{y:,}}<br>' +
                f'<b>Total Volume:</b> %{{customdata[0]:,}}<extra></extra>'
            )
        ))

        # Top Bar: Anomalous (Red)
        fig.add_trace(go.Bar(
            x=agg_df[date_column],
            y=agg_df['anomaly_sum'],
            name='Anomaly',
            marker_color='crimson',  # Red for anomalies
            customdata=agg_df[['total_sum', 'anomaly_pct']],
            hovertemplate=(
                f'<b>Date:</b> %{{x|%Y-%m-%d}}<br>' +
                f'<b>Anomalies:</b> %{{y:,}}<br>' +
                f'<b>Anomaly Rate:</b> %{{customdata[1]:.1f}}%<extra></extra>'
            )
        ))

        # 4. Apply Visual Design (Matching your existing style)
        fig.update_layout(
            title=dict(
                text=f'Anomaly Volume Over Time for {len(df[group_columns].drop_duplicates())} Groups',
                y=0.96,
                x=0.5,
                xanchor='center',
                yanchor='top',
                font=dict(size=18, color='black', weight='bold'),
            ),
            barmode='stack', # This stacks the red bars on top of the grey bars
            height=350,
            width=1200,
            margin=dict(l=50, r=50, t=40, b=30),
            plot_bgcolor='snow',
            paper_bgcolor='whitesmoke',
            xaxis=dict(
                range=[agg_df[date_column].min(), agg_df[date_column].max()],
                showline=True,
                linewidth=0.5,
                linecolor='orange',
                zeroline=False,
                gridcolor='rgba(255, 165, 0, 0.1)',
                mirror=True,
            ),
            yaxis=dict(
                # Dynamic range with a little headroom
                range=[0, agg_df['total_sum'].max() * 1.1],
                showline=True,
                linewidth=0.5,
                linecolor='orange',
                zeroline=False,
                gridcolor='rgba(255, 165, 0, 0.1)',
                mirror=True,
                title=dict(
                    text=variable.replace('_', ' ').title(),
                    font=dict(size=16, weight='bold', color='black')
                ),
            ),
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02,
            )
        )

        fig.show()
        print("\n")
    except Exception as e:
        print(f"Stacked Bar Plot Failed: {e}")


def summary_pie_plot(summary_df, title="Anomaly Detection Summary"):
    """
    Generates a Pie Chart visualizing the distribution of Evaluated, Anomalous, 
    and Dropped records using the specific project styling.

    Args:
        summary_df (pd.DataFrame): Dataframe containing columns 'evaluated records', 
                                   'anomalies', and 'dropped'.
    
    Returns:
        None: Displays the interactive Plotly figure.
    """
    try:
        colors = ['silver', 'crimson', 'gold'] 

        # 2. Initialize Figure
        fig = go.Figure()

        # 3. Add Trace
        fig.add_trace(go.Pie(
            labels=summary_df['Records'],
            values=summary_df['count'],
            marker=dict(
                colors=colors, 
                line=dict(color='white', width=2)
            ),
            textposition='auto',
            texttemplate='%{label}<br>%{percent:.0%}',
            # textinfo='percent+label',
            hoverinfo='label+value+percent',
            sort=False
        ))

        # 4. Apply Visual Design (Matching provided style)
        fig.update_layout(
            title=dict(
                text=title,
                y=0.96,
                x=0.5,
                xanchor='center',
                yanchor='top',
                font=dict(size=18, color='black', weight='bold'),
            ),
            height=400,
            width=600,
            margin=dict(l=50, r=50, t=80, b=30),
            plot_bgcolor='snow',
            paper_bgcolor='whitesmoke',
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02,
            )
        )

        fig.show()
        print("\n")

    except Exception as e:
        print(f"Summary Pie Plot Failed: {e}")


def avg_anomaly_score_plot(df, group_columns, date_column):
    
    try:
        plot_title = f"Average Anomaly Scores Over Time for {len(df[group_columns].drop_duplicates())} Groups"

        fig = go.Figure()

        agg_df = df.groupby(date_column)['Anomaly_Score'].mean().reset_index()

        # Average Anomaly Scores
        fig.add_trace(go.Scatter(
            x=agg_df[date_column],
            y=agg_df['Anomaly_Score'],
            mode='lines',
            line=dict(color='seagreen', width=1.5),
            name='Average Anomaly Score',
        ))

        fig.update_layout(
            title=dict(
                    text=plot_title,
                    y=0.96,
                    x=0.5,
                    xanchor='center',
                    yanchor='top',
                    font=dict(size=18, color='black', weight='bold'),
                ),
            height=350,
            width=1200,
            margin=dict(l=50, r=50, t=40, b=30),
            plot_bgcolor='snow',
            paper_bgcolor='whitesmoke',
            xaxis=dict(
                range=[agg_df[date_column].min(), agg_df[date_column].max()],
                showline=True,
                linewidth=0.5,
                linecolor='orange',
                zeroline=False,
                gridcolor='rgba(255, 165, 0, 0.1)',
                mirror=True
                ),
            yaxis=dict(
                range=[agg_df['Anomaly_Score'].min()*0.9, agg_df['Anomaly_Score'].max()*1.06],
                showline=True,
                linewidth=0.5,
                linecolor='orange',
                zeroline=False,
                gridcolor='rgba(255, 165, 0, 0.1)',
                mirror=True
                ),
            yaxis_title=dict(
                text='Average Anomaly Score',
                font=dict(size=16, weight='bold', color='black')
                ),
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02,
                )
            )

        fig.show()
        print("\n")
    except Exception as e:
        print(f"Anomaly Score Plot Failed: {e}")