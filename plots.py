import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.ticker as mticker



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
