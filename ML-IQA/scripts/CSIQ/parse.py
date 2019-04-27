import pandas as pd

others = pd.read_csv('rawData.csv')

distFolders = ['awgn', 'jpeg', 'jpeg2000', 'fnoise', 'blur', 'contrast']
distNames = ['AWGN', 'JPEG', 'jpeg2000', 'fnoise', 'BLUR', 'contrast']

header = 'reference,distorted,dmos\n'

with open('CSIQ.csv', 'w') as hFile:
	hFile.write(header)
	for index, line in others.iterrows():
		formatted = 'reference/%s.png,%s/%s.%s.%d.png,%.03f\n' % (line['image'], distFolders[line['dst_idx']-1], line['image'], distNames[line['dst_idx']-1], line['dst_lev'], line['dmos'])
		hFile.write(formatted)
