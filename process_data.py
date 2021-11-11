import pandas as pd
from pamguide_csv_tools import combine_csvs, inf_to_nans, remove_nans
from config import processed_path

df = combine_csvs()
df = df.drop('1213', axis=1)
df = inf_to_nans(df)
df = remove_nans(df)

df.reset_index().to_feather(processed_path)
print(df)
