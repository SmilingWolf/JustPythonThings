import sys

import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib

from keras.models import load_model

for database in ['CSIQ', 'LIVE2', 'TID2013']:
	data = pd.read_csv('scores.full.%s.csv' % database)

	for modelName in sys.argv[1:]:
		scaler = joblib.load('%s.wgt' % modelName)
		dataMod = pd.DataFrame(data=scaler.transform(data), columns=data.columns, index=data.index)

		X = dataMod.filter(items=['PSNRY', 'PSNRCb', 'PSNRCr', 'SSIMY', 'SSIMCb', 'SSIMCr'], axis=1).values

		model = load_model('%s.h5' % modelName)
		model.summary()

		predicted = model.predict(X)

		invScaler = StandardScaler()
		invScaler.scale_, invScaler.mean_, invScaler.var_ = scaler.scale_[0], scaler.mean_[0], scaler.var_[0]

		results = invScaler.inverse_transform(predicted)

		with open('%s-%s.txt' % (modelName, database), 'w') as hFile:
			for mos in results:
				hFile.write('%.05f\n' % mos[0])
