from .pipeline import run_pipeline

def timeseries_anomaly_detection(
    master_data=None, 
    group_columns = None, 
    variable= None,
    date_column = None,
    freq="W-MON",
    min_records=None,  
    max_records =None,
    contamination=0.03, 
    random_state=42,
    alpha=0.3, 
    sigma=1.5, 
    eval_period=1,
    prophet_CI=0.90, 
    mad_threshold=2, 
    mad_scale_factor=0.6745
):
    
    """
    Performs anomaly detection on grouped time-series data.

    This function identifies outliers within specific groups of data by analyzing 
    historical trends, applying statistical thresholds, and calculating 
    prediction intervals.
    
    # Mandatory Columns:
    - master_data: Input DataFrame containing variables, dates, and group identifiers.
    - group_columns: List of columns used to segment the data (e.g., ['Region', 'Product']).
    - variable: The numerical target column to analyze for outliers.
    - date_column: The datetime column representing the time axis.
    
    # Default arguments:
    - freq (str): Frequency of the time series (Pandas offset alias). Defaults to 'W-MON'.
    - min_records: Minimum history required per group. Default is None; If None, extracts based on freq (1 Year + eval_period).
    - max_records: Maximum history to retain per group. Default is None; if provided, filters for the most recent N records.
    - contamination (float): Expected proportion of outliers in the data (0 to 0.5). Defaults to 0.03.
    - random_state (int): Seed for reproducibility in stochastic models. Defaults to 42.
    - alpha (float): Smoothing factor for trend calculations. Defaults to 0.3.
    - sigma (float): Standard deviation multiplier for thresholding. Defaults to 1.5.
    - eval_period: The number of trailing records in each group to evaluate for anomalies.
    - prophet_CI (float): The confidence level for the prediction interval (0 to 1). Defaults to 0.9.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
            - final_results: The main dataframe containing original data, interpolated values, 
              forecasts, residuals, and anomaly flags (e.g., is_FB_anomaly, is_IQR_anomaly).
            - success_report: A summary table for successful groups showing 'initial_record_count', 
              'interpolated_record_count', and 'interpolation_pct'.
            - exclusion_report: A diagnostic table listing groups dropped from the analysis 
              and the specific reason (e.g., "Insufficient records" or "High Interpolation").
              
    """
    # --- 1. MANDATORY PARAMETER VALIDATION ---
    required_params = {
        "master_data": master_data,
        "group_columns": group_columns,
        "variable": variable,
        "date_column": date_column
    }

    missing_params = [name for name, val in required_params.items() if val is None]

    if missing_params:
        print("\n" + "!"*60)
        print("❌ ERROR: MISSING REQUIRED PARAMETERS")
        print("The following parameters are required to run the detection:")
        for param in missing_params:
            print(f"  - {param}")
        
        print("\n💡 HINT: Use help(timeseries_anomaly_detection) to see detailed")
        print("descriptions and expected formats for each parameter.")
        print("!"*60 + "\n")
        return # Exit early
    
    # --- 2. MANDATORY COLUMN VALIDATION ---
    mandatory_cols = group_columns + [variable, date_column]
    missing_cols = [col for col in mandatory_cols if col not in master_data.columns]
    
    if missing_cols:
        raise ValueError(
            f"CRITICAL ERROR: Mandatory columns missing from input DataFrame: {missing_cols}. "
            f"Please ensure group_columns, variable, and date_column are correctly spelled."
        )
        return # Exit early
        
    # --- 3. EXECUTE PIPELINE ---
    # Store results in a local variable first
    final_df, success_report, exclusion_report = run_pipeline(
        master_data=master_data,
        group_columns=group_columns,
        variable=variable,
        date_column=date_column,
        freq=freq,
        min_records=min_records,
        max_records=max_records, 
        contamination=contamination,
        random_state=random_state,
        alpha=alpha,
        sigma=sigma,
        eval_period=eval_period,
        prophet_CI=prophet_CI,
        mad_threshold=mad_threshold, 
        mad_scale_factor=mad_scale_factor
    )

    import inspect
    # Inside your timeseries_anomaly_detection function:
    # 1. Get the line of code that called this function
    frame = inspect.currentframe().f_back
    call_line = ""
    if frame and inspect.getframeinfo(frame).code_context:
        call_line = inspect.getframeinfo(frame).code_context[0].strip()

    # 2. Check if the user assigned the result to variables
    # We split by the function name and check the part before it (index 0)
    is_assigned = False
    if "timeseries_anomaly_detection" in call_line:
        prefix = call_line.split("timeseries_anomaly_detection")[0]
        # If there is exactly one '=', it's an assignment
        if prefix.count("=") == 1:
            is_assigned = True

    # 3. If NOT assigned, trigger the "Auto-Save" to the global namespace
    if not is_assigned:
        from IPython import get_ipython
        shell = get_ipython()
        if shell:
            shell.user_ns['final_results'] = final_df
            shell.user_ns['success_report'] = success_report
            shell.user_ns['exclusion_report'] = exclusion_report

            print("\n" + "*"*60)
            print("🚀 AUTO-SAVE: Variables were not assigned.")
            print("The outputs have been saved globally for you as:")
            print("   - final_results, success_report, exclusion_report")
            print("*"*60 + "\n")

    # 4. Final return logic
    if is_assigned:
        # Determine if the user assigned to a single variable or multiple
        prefix = call_line.split("=")[0].strip()
        
        # If there's no comma in the assignment prefix, they used a single variable
        if "," not in prefix:
            print(f"\n💡 INFO: You assigned the output to a single variable: '{prefix}'")
            print(f"   This variable is a tuple containing 3 DataFrames. Access them via:")
            print(f"   1. Results Data:    {prefix}[0]")
            print(f"   2. Success Report:  {prefix}[1]")
            print(f"   3. Exclusion List:  {prefix}[2]")
            print(f"   Or unpack them: final_df, success, exclusion = {prefix}\n")
        
        return final_df, success_report, exclusion_report
    else:
        # Return None so Jupyter doesn't print the "wall of text"
        return None