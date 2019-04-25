import pandas as pd

df = pd.read_csv('LIVE2.csv')

for index, row in df.iterrows():
	if row['original'] == 0:
		print('./dump_psnr.exe -s %s.y4m %s.y4m | grep Total >> PSNR3.txt' % (row['reference'], row['distorted']))
