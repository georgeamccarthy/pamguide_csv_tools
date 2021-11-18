# PAMGuide CSV Tools

PAMGuide CSV Tools converts `.csv` files outputted by PAMGuide into a processed `.feather` binary file. 

## Features

✅ Combines all child CSVs in parent folder.

✅ Removes `nan` entries.

✅ Timestamps data.

✅ Converts csv to DataFrame.

✅ Feather binary file is fast and lightweight.

## How to use PAMGuide CSV Tools

### Command-line

This can be run from the command-line by downloading `pamguide_csv_tools.py` and running

```
python pamguide_csv_tools.py
```

### Python

This can be used within python by importing the file

```python
from pamguide_csv_tools import process_csvs

process_csvs(csv_folder_path='/data/pamgguide_csv_folder')
```

Where `csv_folder_path` should be set to where you are storing your CSVs.

## How to use feather files

### Load feather into Pandas DataFrame
```python
import pandas as pd

df = pd.read_feather(path='mydata.feather')
```

### Save Pandas DataFrame to feather file

This creates `df_as_feather.feather` in the local directory.

```python
df.reset_index().to_feather(path='mydata.feather')
```