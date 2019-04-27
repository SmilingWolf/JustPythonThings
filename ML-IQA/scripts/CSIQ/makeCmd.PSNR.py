import pandas as pd

df = pd.read_csv('CSIQ.csv')

for index, row in df.iterrows():
	print('./dump_psnr.exe -s %s.y4m %s.y4m | grep Total >> PSNR3.txt' % (row['reference'], row['distorted']))
