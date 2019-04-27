# Image Quality Multi-Layer Perceptron

import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib

from keras.models import Model
from keras.layers import Input, Dense, Activation
from keras.optimizers import SGD

from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau

data = pd.read_csv('scores.csv')
valData = pd.read_csv('val_scores.csv')

scaler = StandardScaler()
data = pd.DataFrame(data=scaler.fit_transform(data), columns=data.columns, index=data.index)
joblib.dump(scaler, 'scaler.wgt')

valData['MOS'] = valData['MOS'] * (9/100.0)
valData = pd.DataFrame(data=scaler.transform(valData), columns=valData.columns, index=valData.index)

Y = data.filter(items=['MOS'], axis=1).values
X = data.filter(items=['PSNRY', 'PSNRCb', 'PSNRCr', 'SSIMY', 'SSIMCb', 'SSIMCr'], axis=1).values

valY = valData.filter(items=['MOS'], axis=1).values
valX = valData.filter(items=['PSNRY', 'PSNRCb', 'PSNRCr', 'SSIMY', 'SSIMCb', 'SSIMCr'], axis=1).values

i = Input(shape=(6, ))
x = Dense(7, kernel_initializer='lecun_normal')(i)
x = Activation('selu')(x)
x = Dense(5, kernel_initializer='lecun_normal')(x)
x = Activation('selu')(x)
x = Dense(3, kernel_initializer='lecun_normal')(x)
x = Activation('selu')(x)
o = Dense(1, kernel_initializer='lecun_normal')(x)

model = Model(inputs=i, outputs=o)

opt = SGD(lr=0.01, momentum=0.9, nesterov=True)
model.compile(optimizer=opt, loss='logcosh')

mc = ModelCheckpoint('models/IQMLP-{epoch:02d}-{val_loss:.4f}.h5', save_best_only=True, monitor='val_loss', mode='min')
reduce_lr = ReduceLROnPlateau(monitor='val_loss', verbose=1, factor=0.5, patience=10, min_lr=0.00001)

model.fit(x=X, y=Y, verbose=1, epochs=200, validation_data=(valX, valY), callbacks=[reduce_lr, mc])
