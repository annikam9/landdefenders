import pandas as pd
mergefinal = pd.read_csv('utils/Finalmerge.csv', sep =",")
mergeyears = pd.read_csv('utils/merge_years.csv', sep =",")
print(mergefinal.head())
print(mergeyears.head())