import pandas as pd 

df=pd.read_csv("/Users/mohan_007/Documents/play_by_play_2024.csv")

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    # print(df)
    print(df.dtypes)