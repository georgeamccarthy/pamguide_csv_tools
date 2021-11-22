import pandas as pd
import os
import datetime
import numpy as np
import config

processed_folder_path = './processed'

def process_csvs(csv_folder_path, processed_file_name):
    df = combine_csvs(csv_folder_path)
    print('CSVs combined and timestamped.')
    df = df.drop('1213', axis=1)
    print('PAMGuide false time column dropped')
    df = inf_to_nans(df)
    df = remove_nans(df)
    print('Corrupt nan sections removed.')

    if not os.path.exists(processed_folder_path):
        os.makedirs(processed_folder_path)

    df.reset_index().to_feather(f'{processed_folder_path}/{processed_file_name}.feather')
    print(df)

    print(f'Processed data saved {processed_folder_path}/{processed_file_name}.feather')


def get_csvs():
    csv_names = []
    csv_paths = []

def combine_csvs(csv_folder_path):
    '''
    Combines CSVs and timestamps them.
    '''
    csv_paths = []
    def traverse_dir(path):
        for root, _, file_objects in os.walk(path):
            for file_object in file_objects:
                file_object_path = os.path.join(root, file_object)
                
                if file_object[-4:] == '.csv':
                    csv_paths.append(file_object_path)
                
                elif os.path.isdir(file_object_path):
                    traverse_dir(file_object_path)

    traverse_dir(csv_folder_path)
    csv_paths.sort()

    print(f'{len(csv_paths)} CSVs loaded.')

    # Timestamp each row on the column by the starting timestamp in the file name
    # + 0.5 seconds each row.

    print('Timestamping.')
    df_from_each_csv = (pd.read_csv(f) for f in csv_paths)
    timestamps = np.empty(0)
    for i, df in enumerate(df_from_each_csv):
        csv_name = csv_paths[i].rsplit('/', 1)[-1]
        time_str = csv_name[15:34]

        datetime_object = datetime.datetime(
                year=int(time_str[:4]),
                month=int(time_str[4:6]),
                day=int(time_str[6:8]),
                hour=int(time_str[9:11]),
                minute=int(time_str[11:13]),
                second=int(time_str[13:15]),
                microsecond=int(time_str[16:19])*1000,
        )

        timestamps = np.concatenate((timestamps, datetime_object + np.arange(len(df)) * datetime.timedelta(seconds=0.5)))

    print('Concatenating.')
    df_from_each_csv = (pd.read_csv(f) for f in csv_paths)
    concatenated_df = pd.concat(df_from_each_csv)

    concatenated_df['timestamp'] = timestamps

    return concatenated_df


def remove_nans(df):
    '''
    Removes any rows containing nan values and two rows either side of each of 
    these rows.
    '''
    m = df.isna().any(axis=1)
    return df[~(m | m.shift(fill_value=False) | m.shift(-1, fill_value=False) | m.shift(-2, fill_value=False))]

    # Equivalent but slower.

def remove_nans_old(df):
    '''
    Depreciated nan remover (slower).
    '''
    #identify all the rows in dataframe where there are nan (infinite values)
    rows = df.index[np.isnan(df).any(1)]     

    #create an empty list to store dodgy rows which are either 1 second before or after a period when the hydrophone stopped (missing data)
    dodge_rows = []

    #loop through the rows where there are missing data and find times when hydrophone stopped/started recording 
    for i in range (0, len(rows)-1): 
        #print(rows[i])

        #point where the hydrophone stopped  recording 
        if (rows[i+1]-rows[i] != 1): 
            if (rows[i]+2) not in dodge_rows: 
                dodge_rows.append(rows[i]+2)
            if (rows[i]+1) not in dodge_rows:  
                dodge_rows.append(rows[i]+1)

        #point where hydrophone restarted recording 
        if (rows[i]-rows[i-1]) != 1:
            if (rows[i]-2) not in dodge_rows: 
                dodge_rows.append(rows[i]-2)
            if (rows[i]-1) not in dodge_rows: 
                dodge_rows.append(rows[i]-1)

    #include the dodgy values 1 second after the last period of missing data, not included in above range
    dodge_rows.append(rows[len(rows)-1]+1)
    dodge_rows.append(rows[len(rows)-1]+2)

    #new dataframe does not include data points before or after a period of missing hydrophone data or any missing data (nan) values
    for i in range(0, len(dodge_rows)): 
        df = df.drop(dodge_rows[i])

    #remove nan values 
    df.dropna(inplace=True)
    return df

def inf_to_nans(df):
    return df.replace([np.inf, -np.inf], np.nan)

if __name__ == '__main__':
    if config.csv_folder_path == '':
        print('Enter folder containing .csv files to process')
        csv_folder_path = input('>>> ')
    else:
        csv_folder_path = config.csv_folder_path
        print(f'.csv folder path loaded from config.py ({csv_folder_path})')

    print('Enter output file name (without file ending)')
    processed_file_name = input('>>> ')
    if processed_file_name == '':
        processed_file_name = 'processed'

    process_csvs(csv_folder_path, processed_file_name)
