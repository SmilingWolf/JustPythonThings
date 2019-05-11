import pandas as pd

valNames = ['refimgs/sailing1.bmp', 'refimgs/womanhat.bmp', 'refimgs/sailing3.bmp', 'refimgs/parrots.bmp', 'refimgs/cemetry.bmp']

baseDF = pd.read_csv('LIVE2.csv')
scoresDF = pd.read_csv('scores.csv')

baseDF = baseDF[baseDF.original == 0].reset_index()

valDF = scoresDF[baseDF.reference.isin(valNames)]
trainDF = scoresDF[~baseDF.reference.isin(valNames)]

valDF.to_csv('scores.valid.LIVE2.csv', index=False)
trainDF.to_csv('scores.train.LIVE2.csv', index=False)
