import pandas as pd

valNames = ['reference/snow_leaves.png', 'reference/elk.png', 'reference/boston.png', 'reference/butter_flower.png', 'reference/bridge.png']

baseDF = pd.read_csv('CSIQ.csv')
scoresDF = pd.read_csv('scores.csv')

trainDF = pd.DataFrame(columns=scoresDF.columns)
valDF = pd.DataFrame(columns=scoresDF.columns)

valDF = scoresDF[baseDF.reference.isin(valNames)]
trainDF = scoresDF[~baseDF.reference.isin(valNames)]

valDF.to_csv('scores.valid.CSIQ.csv', index=False)
trainDF.to_csv('scores.train.CSIQ.csv', index=False)
