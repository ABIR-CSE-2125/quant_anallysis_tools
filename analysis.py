import pandas as pd 
import glob
import numpy as np

################################################ TRADE ANALYSIS FUCNTIONS #########################################################

def merged_blotter_df(blotter_dir : str,timestamp_col: str = 'timestamp') -> pd.DataFrame:
    '''
    blotter_dir : blotter dir path
    '''
    blotter_file_paths = glob.glob(f'{blotter_dir}/*.csv')

    # Read and merge blotter files
    blotter_df_list = [pd.read_csv(i) for i in blotter_file_paths]
    for df in blotter_df_list:
        df.columns = df.columns.str.strip()

    # Merge the data frame of each day
    blotter_merged_df = pd.concat(blotter_df_list, ignore_index=True)

    # sort on the basis of timestamp
    blotter_merged_df = blotter_merged_df.sort_values(
    by=[timestamp_col, "trade_sub_type"],
    key=lambda x: x if x.name != "trade_sub_type" else x.map({"unwind": 0, "trade": 1})
    ).reset_index(drop=True)

    # converting time_col to datetime 
    blotter_merged_df[timestamp_col] = pd.to_datetime(blotter_merged_df[timestamp_col])

    return blotter_merged_df

def generate_resample_data(path: str, timestamp_col : str = 'timestamp', freq : str = 'D')-> pd.DataFrame:
    '''
    path : folder path where the csv files are stored
    freq : At which sampling needs to be done
    returns:
    sampled data for the required frequency
    '''
    df_files = glob.glob(f"{path}/*.csv")
    df_list = [pd.read_csv(file) for file in df_files]
    df = pd.concat(df_list, ignore_index=True)
    df = df[df['trade_done'] == True]
    df['Timestamp'] = pd.to_datetime(df[timestamp_col])
    df = df.set_index("Timestamp").sort_index()
    resampled_df = df.resample(freq).last().dropna()
    return resampled_df