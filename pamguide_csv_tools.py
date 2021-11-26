import pandas as pd
import os
import datetime
import numpy as np
import config


def process_csvs(csv_folder_path, processed_file_name, processed_folder_path='./processed'):
    processed_path = f'{processed_folder_path}/{processed_file_name}'

    if not os.path.exists(processed_folder_path):
        os.makedirs(processed_folder_path)

    files = os.listdir(csv_folder_path)
    csv_names = []
    for file_name in files:
        if file_name[-4:] == '.csv':
            csv_names.append(file_name)

    to_process = len(csv_names)
    for i, csv_name in enumerate(csv_names):
        df = pd.read_csv(f'{csv_folder_path}/{file_name}')
        df.drop(columns=['1213'], inplace=True)

        df = timestamp(df, csv_name)
        #print('CSVs combined and timestamped.')
        #print('PAMGuide false time column dropped')
        df = inf_to_nans(df)
        df = remove_nans(df)
        #print('Corrupt nan sections removed.')

        to_process = to_process-1

        if i == 0:
            concat_df = df
            concat_df.to_feather(path=processed_path)
        else:
            concat_df = pd.concat([concat_df, df])

            if to_process % 100 == 0:
                print(f'{(i+1)/len(csv_names)*100:.0f}%')
                saved_df = pd.read_feather(path=processed_path)
                concat_df = pd.concat([saved_df, concat_df])
                concat_df.reset_index(drop=True, inplace=True)
                concat_df.to_feather(path=processed_path)
            

def timestamp(df, csv_name):
    time_str = csv_name[15:34]
    try:
        datetime_object = datetime.datetime(
                year=int(time_str[:4]),
                month=int(time_str[4:6]),
                day=int(time_str[6:8]),
                hour=int(time_str[9:11]),
                minute=int(time_str[11:13]),
                second=int(time_str[13:15]),
                microsecond=int(time_str[16:19])*1000,
        )

        timestamps = (np.arange(len(df)) * datetime.timedelta(seconds=0.5))
        timestamps = timestamps + datetime_object
    except:
        timestamps = np.empty(len(df))

    df['timestamp'] = timestamps

    return df


def remove_nans(df):
    '''
    Removes any rows containing nan values and two rows either side of each of 
    these rows.
    '''
    m = df.isna().any(axis=1)
    return df[~(m | m.shift(fill_value=False) | m.shift(-1, fill_value=False) | m.shift(-2, fill_value=False))]

    # Equivalent but slower.


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
    
