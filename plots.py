import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.ticker as mticker
import glob


########################################################################################################################################################

def win_count_weekday_wise_plot(daily_pnl,Positive,Negative,title,weekday_count = 5,):
    '''
    daily_pnl : pd.Dataframe with Daily PnL with timestamp as index
    Positive : Column name for Positive Pnl
    Negative : Column name for Negative Pnl
    weekday_count : how many days are we considering
    '''

    df = pd.DataFrame({"PnL": daily_pnl, "Weekday": daily_pnl.index.weekday}) 

    weekday_pnl_counts = df.groupby("Weekday")["PnL"].agg(  
        Positive_Days=lambda x: (x > 0).sum(),  
        Negative_Days=lambda x: (x < 0).sum()  
    ).reset_index()  

    # Map weekday numbers to names  
    weekday_pnl_counts["Weekday"] = weekday_pnl_counts["Weekday"].map(  
        {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday",5 : 'Staurday'}  
    )  

    plt.figure(figsize=(10, 6))

# Define bar width
    bar_width = 0.4  

    # Get weekday labels (Convert index to actual weekday names)
    if weekday_count == 6:
        weekday_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",'Saturday']
    elif weekday_count == 5:
        weekday_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    x = np.arange(len(weekday_labels))  # Numeric positions for bars

    # Define new colors
    pos_color = "royalblue"  # Positive PnL Days
    neg_color = "tomato"     # Negative PnL Days

    # Create bars for positive and negative PnL counts
    plt.bar(x - bar_width / 2, weekday_pnl_counts[Positive], width=bar_width, color=pos_color, label="Positive PnL Days", edgecolor="black")
    plt.bar(x + bar_width / 2, weekday_pnl_counts[Negative], width=bar_width, color=neg_color, label="Negative PnL Days", edgecolor="black")

    # Add labels and title
    plt.xlabel("Weekday", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.title(title, fontsize=14)
    plt.xticks(ticks=x, labels=weekday_labels, rotation=0)  # Set proper weekday names
    plt.legend()

    # Show the plot
    plt.show()

def weekday_wise_aggregation_plot(daily_pnl,metric,title):
    '''
    daily_pnl : pd.Dataframe with Daily PnL with timestamp as index
    metric : mean | min | max | std ...or something else that can be aggregation metric
    '''
    daily_pnl.index = pd.to_datetime(daily_pnl.index)

    # Extract the weekday name from the timestamp index
    metric_list = [metric]
    weekday_stats = daily_pnl.groupby(daily_pnl.index.day_name()).agg(metric_list)

    # Reorder weekdays properly (optional)
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    weekday_stats = weekday_stats.reindex(weekday_order)

    # Function to format y-axis labels in "K" (thousands)
    def format_k(value, pos):
        return f'{int(value / 1000)}K' if value >= 1000 else int(value)

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))  # Adjust figure size
    fig.suptitle(title, fontsize=16)

    # Plot Mean PnL
    sns.barplot(x=weekday_stats.index, y=weekday_stats[metric], color="royalblue", ax=ax)

    # Formatting
    ax.set_title(f"{metric} PnL", fontsize=14)
    ax.set_xlabel("Weekday", fontsize=12)
    ax.set_ylabel(f"{metric} PnL", fontsize=12)
    ax.grid(axis="y", linestyle="-", alpha=0.7)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_k))  # Format y-axis in 'K'

    # Show the plot
    plt.show()



def comparative_pnl_plot(backtest_path_1, backtest_path_2, strategy_name_1, strategy_name_2):
    """
    Plots a dual-axis line graph comparing the 'portfolio_value' column from two backtests.

    Parameters:
        backtest_path_1 (str): Path to the first backtest directory.
        backtest_path_2 (str): Path to the second backtest directory.
        strategy_name_1 (str): Name of First Strategy
        strategy_name_2 (str): Name of Second Startegy
    Raises:
        ValueError: If 'portfolio_value' is not found in either DataFrame.
    """

    # Load and process first dataset
    df1_files = glob.glob(f"{backtest_path_1}/consolidated_store/*.csv")
    df1_list = [pd.read_csv(file) for file in df1_files]
    df1 = pd.concat(df1_list, ignore_index=True)
    df1 = df1[df1['trade_done'] == True]
    df1['Timestamp'] = pd.to_datetime(df1['timestamp'])
    df1 = df1.set_index("Timestamp").sort_index()
    df1_daily = df1.resample('D').last().dropna()

    # Load and process second dataset
    df2_files = glob.glob(f"{backtest_path_2}/consolidated_store/*.csv")
    df2_list = [pd.read_csv(file) for file in df2_files]
    df2 = pd.concat(df2_list, ignore_index=True)
    df2 = df2[df2['trade_done'] == True]
    df2['Timestamp'] = pd.to_datetime(df2['timestamp']) 
    df2 = df2.set_index("Timestamp").sort_index()
    df2_daily = df2.resample('D').last().dropna()

    # Validate column existence
    if "portfolio_value" not in df1_daily.columns:
        raise ValueError("Column 'portfolio_value' not found in first dataset.")
    if "portfolio_value" not in df2_daily.columns:
        raise ValueError("Column 'portfolio_value' not found in second dataset.")

    # Plotting
    fig, ax1 = plt.subplots(figsize=(16, 7))

    # Primary Y-axis (df1)
    ax1.plot(df1_daily.index, df1_daily["portfolio_value"], label=f"Portfolio Value {strategy_name_1}", color='#64B5F6')
    ax1.set_ylabel(f"Portfolio Value {strategy_name_1}", color='black')
    ax1.tick_params(axis='y', labelcolor='black')

    # Secondary Y-axis (df2)
    ax2 = ax1.twinx()
    ax2.plot(df2_daily.index, df2_daily["portfolio_value"], label=f"Portfolio Value {strategy_name_2}", color='#4CAF50')
    ax2.set_ylabel(f"Portfolio Value {strategy_name_2}", color='black')
    ax2.tick_params(axis='y', labelcolor='black')

    # Number formatting function
    def format_number(value, _):
        if 1_000 <= abs(value) < 1_000_000:
            return f"{value / 1_000:.1f}K"
        elif abs(value) >= 1_000_000:
            return f"{value / 1_000_000:.1f}M"
        return str(int(value))  # Convert to int for cleaner display

    # Apply formatting to y-ticks
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(format_number))
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(format_number))

    # Labels and title
    ax1.set_xlabel("Date")
    plt.title(f'Comparison : {strategy_name_1} vs {strategy_name_2}')

    # Show grid and legend
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    fig.tight_layout()
    plt.show()
