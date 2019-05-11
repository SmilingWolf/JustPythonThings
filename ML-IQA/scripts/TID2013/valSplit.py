import pandas as pd

valNames = ['I15.BMP', 'I07.BMP', 'I19.BMP', 'I18.BMP']

baseDF = pd.read_csv('TID2013.csv')
scoresDF = pd.read_csv('scores.csv')

valDF = scoresDF[baseDF.reference.isin(valNames)]
trainDF = scoresDF[~baseDF.reference.isin(valNames)]

valDF.to_csv('scores.valid.TID2013.csv', index=False)
trainDF.to_csv('scores.train.TID2013.csv', index=False)
