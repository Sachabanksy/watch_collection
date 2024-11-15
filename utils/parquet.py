import time
import pandas as pd
import polars as pl

import os

#file = '/Users/sachabanks/DataDudes/3rd Party Data/Watches.csv'
outputpath = '/Users/sachabanks/Desktop/data-dudes-dash/data/watches.parquet'

def make_parquet_file(file_path, file):
    # Read the CSV file
    path = file_path + file
    df = pd.read_csv(path)

    # Write the DataFrame to a Parquet file

    outputpath = os.path.splitext(f'/Users/sachabanks/Desktop/data-dudes-dash/data/{file}')[0]
    df.to_parquet(f"{outputpath}.parquet", index=False)

    print('successfully written')

file_path = '/Users/sachabanks/DataDudes/3rd Party Data/'

files = os.listdir(file_path)
outputpath = '/Users/sachabanks/Desktop/data-dudes-dash/data'
for file in files:
    make_parquet_file(file_path, file)
    
#make_parquet_file(file, outputpath)
import pandas as pd
import os 

file_path = '/Users/sachabanks/Desktop/data-dudes-dash/data'

combined_data = pd.DataFrame()

files = ['test-dataset.parquet', 'test-dataset1.parquet']

for file in file_path:
    if file not in files:
        continue
    print(file)
    df = pd.read_parquet(file_path + '/' +file)
    pd.concat([df, combined_data])

combined_data.to_parquet(f"{file_path}/combined_data.parquet", index=False)
csv_file_path = '/Users/sachabanks/DataDudes/3rd Party Data/Watches.csv'
parquet_file_path = '/Users/sachabanks/Desktop/data-dudes-dash/data/watches.parquet'
# Function to measure execution time
def measure_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time
'''
# Reading CSV with Pandas
df_pandas_csv, time_pandas_csv = measure_time(pd.read_csv, csv_file_path)
print(f"Time taken to read CSV with Pandas: {time_pandas_csv:.4f} seconds")

# Reading Parquet with Pandas
df_pandas_parquet, time_pandas_parquet = measure_time(pd.read_parquet, parquet_file_path)
print(f"Time taken to read Parquet with Pandas: {time_pandas_parquet:.4f} seconds")

# Reading CSV with Polars
df_polars_csv, time_polars_csv = measure_time(pl.read_csv, csv_file_path)
print(f"Time taken to read CSV with Polars: {time_polars_csv:.4f} seconds")

# Reading Parquet with Polars
df_polars_parquet, time_polars_parquet = measure_time(pl.read_parquet, parquet_file_path)
print(f"Time taken to read Parquet with Polars: {time_polars_parquet:.4f} seconds")
'''