# Image Quality Support Vector Regressor

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
from sklearn.svm import NuSVR

data = pd.read_csv('scores.csv')

modelName = 'IQSVR'

scaler = joblib.load('%s.scaler.wgt' % modelName)
data = pd.DataFrame(data=scaler.fit_transform(data), columns=data.columns, index=data.index)

X = data.filter(items=['PSNRY', 'PSNRCb', 'PSNRCr', 'SSIMY', 'SSIMCb', 'SSIMCr'], axis=1).values

model = joblib.load('%s.model.wgt' % modelName)

predicted = model.predict(X)

mos = pd.DataFrame(data=predicted, index=data.index, columns=['MOS'])
others = pd.DataFrame(data=X, index=data.index, columns=['PSNRY', 'PSNRCb', 'PSNRCr', 'SSIMY', 'SSIMCb', 'SSIMCr'])

submission = pd.concat([mos, others], axis=1)
submission = pd.DataFrame(data=scaler.inverse_transform(submission), columns=submission.columns, index=submission.index)
submission.to_csv('predicted-%s.csv' % modelName, index=False)
