import pandas as pd
import os

df= pd.read_csv('processed.csv')
for r in df:
    print(r)