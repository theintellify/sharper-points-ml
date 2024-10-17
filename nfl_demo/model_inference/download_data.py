import nfl_data_py as nfl

df=nfl.import_pbp_data([2023,2024], downcast=True, cache=False, alt_path=None)

print(df)

df.to_csv("2023_2024.csv", encoding='utf-8', index=False)