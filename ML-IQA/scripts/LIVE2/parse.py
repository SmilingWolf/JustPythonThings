import numpy as np
import pandas as pd

import scipy.io

dmos = scipy.io.loadmat('dmos_realigned.mat')
orgs = dmos['orgs'][0]
dmos = dmos['dmos_new'][0]

refnames = scipy.io.loadmat('refnames_all.mat')['refnames_all'][0]

refnamesList = [('refimgs/%s' % x[0]) for x in refnames]

# Compression
jp2k = [('jp2k/img%d.bmp' % x) for x in range(1, 228)]
jpeg = [('jpeg/img%d.bmp' % x) for x in range(1, 234)]

# Distortion
wn = [('wn/img%d.bmp' % x) for x in range(1, 175)]
gblur = [('gblur/img%d.bmp' % x) for x in range(1, 175)]
fastfading = [('fastfading/img%d.bmp' % x) for x in range(1, 175)]

dist = np.concatenate((jp2k, jpeg, wn, gblur, fastfading))

df = pd.DataFrame(np.column_stack([refnamesList, dist, orgs, dmos]), columns=['reference', 'distorted', 'original', 'dmos'])
df.to_csv('LIVE2.csv', index=False)
