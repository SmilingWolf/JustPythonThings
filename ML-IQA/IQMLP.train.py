# Image Quality Multi-Layer Perceptron

import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib

from keras.models import Model
from keras.layers import Input, Dense, Activation
from keras.optimizers import SGD

from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau

data = pd.read_csv('scores-CSIQ.csv')
data = data.append(pd.read_csv('scores-LIVE2.csv'))
data = data.append(pd.read_csv('scores-TID2013.csv'))

scaler = StandardScaler()
data = pd.DataFrame(data=scaler.fit_transform(data), columns=data.columns, index=data.index)
joblib.dump(scaler, 'scaler.wgt')

Y = data.filter(items=['MOS'], axis=1).values
X = data.filter(items=['PSNRY', 'PSNRCb', 'PSNRCr', 'SSIMY', 'SSIMCb', 'SSIMCr'], axis=1).values

i = Input(shape=(6, ))
x = Dense(5, kernel_initializer='lecun_normal')(i)
x = Activation('selu')(x)
x = Dense(3, kernel_initializer='lecun_normal')(x)
x = Activation('selu')(x)
o = Dense(1, kernel_initializer='lecun_normal')(x)

model = Model(inputs=i, outputs=o)

opt = SGD(lr=0.01, momentum=0.9, nesterov=True)
model.compile(optimizer=opt, loss='logcosh')

mc = ModelCheckpoint('models/IQMLP-{epoch:02d}-{loss:.4f}.h5', save_best_only=True, monitor='loss', mode='min')
reduce_lr = ReduceLROnPlateau(monitor='loss', verbose=1, factor=0.5, patience=10, min_lr=0.00001)

model.fit(x=X, y=Y, verbose=1, epochs=200, validation_split=0.0, callbacks=[reduce_lr, mc])
