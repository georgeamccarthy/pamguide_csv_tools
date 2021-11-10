import pandas as pd
import os
from config import csv_folder_path, save_folder_path

csv_names = []
for root, dirs, files in os.walk(csv_folder_path):
    for file in files:
        if file.endswith(".csv"):
            csv_names.append(os.path.join(root, file))

csv_names.sort()

df_from_each_csv = (pd.read_csv(f) for f in csv_names)
concatenated_df = pd.concat(df_from_each_csv)

if not os.path.exists(save_folder_path):
    os.makedirs(save_folder_path)

save_path = f'{save_folder_path}/processed.feather'

print(f'Saving csv: {save_path}')
concatenated_df.to_feather(save_path)

