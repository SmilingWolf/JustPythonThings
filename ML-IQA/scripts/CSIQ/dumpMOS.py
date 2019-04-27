import pandas as pd

df = pd.read_csv('CSIQ.csv')

for index, row in df.iterrows():
	print(1 - row['dmos'])
