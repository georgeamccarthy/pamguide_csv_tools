import pandas as pd
import os
from config import csv_folder_path, processed_path
import datetime
import numpy as np

csv_paths = []
csv_names = []
for root, dirs, files in os.walk(csv_folder_path):
    for file in files:
        if file.endswith(".csv"):
            csv_names.append(file)
            csv_paths.append(os.path.join(root, file))

csv_paths.sort()

# Timestamp each row on the column by the starting timestamp in the file name
# + 0.5 seconds each row.

df_from_each_csv = (pd.read_csv(f) for f in csv_paths)
timestamps = np.empty(0)
for i, df in enumerate(df_from_each_csv):
    time_str = csv_names[i][15:34]
    year = int(time_str[:4])
    month = int(time_str[4:6])
    day = int(time_str[6:8])
    hour = int(time_str[9:11])
    minute = int(time_str[11:13])
    second = int(time_str[13:15])
    millisecond = int(time_str[16:19])
    datetime_object = datetime.datetime(year, month, day, hour, minute, second, microsecond=millisecond*1000)

    timestamps = np.concatenate((timestamps, datetime_object + np.arange(len(df)) * datetime.timedelta(seconds=0.5)))

df_from_each_csv = (pd.read_csv(f) for f in csv_paths)
concatenated_df = pd.concat(df_from_each_csv)

concatenated_df['timestamp'] = timestamps

if not os.path.exists(processed_path):
    os.makedirs(processed_path)

print(f'Saving csv: {processed_path}')
print(concatenated_df.head())
concatenated_df.reset_index().to_feather(processed_path)

