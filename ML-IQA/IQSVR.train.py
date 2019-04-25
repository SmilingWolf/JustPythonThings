# Image Quality Support Vector Regressor

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
from sklearn.svm import NuSVR

data = pd.read_csv('scores.csv')

scaler = StandardScaler()
data = pd.DataFrame(data=scaler.fit_transform(data), columns=data.columns, index=data.index)
joblib.dump(scaler, 'IQSVR.scaler.wgt')

Y = data.filter(items=['MOS'], axis=1).values
X = data.filter(items=['PSNRY', 'PSNRCb', 'PSNRCr', 'SSIMY', 'SSIMCb', 'SSIMCr'], axis=1).values

Y = np.reshape(Y, (-1, ))

model = NuSVR(gamma=0.05, C=4.0, nu=0.9)
model.fit(X, Y)
joblib.dump(model, 'IQSVR.model.wgt')
