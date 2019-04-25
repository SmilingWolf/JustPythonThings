import pandas as pd

df = pd.read_csv('LIVE2.csv')

for index, row in df.iterrows():
	if row['original'] == 0:
		print(100 - row['dmos'])
