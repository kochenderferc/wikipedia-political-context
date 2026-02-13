import glob
import os
import pandas as pd


tsv_files = glob.glob("data/*.tsv")

for file in tsv_files:
    print(file)
    df = pd.read_csv(file, sep="\t")



print(df.columns)
