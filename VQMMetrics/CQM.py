import sys
import numpy as np
from PIL import Image

def MSE(array1, array2):
	error = ((array1 - array2) ** 2).mean(axis=None)
	return error

def PSNR(array1, array2):
	error = MSE(array1, array2)
	return 10 * np.log10(65025 / error)

def getImageArray(imagePath):
	imageFile = Image.open(imagePath)
	imageArray = np.array(imageFile.getdata())
	imageFile.close()
	return imageArray

def RGBToYUVRCT(imageArray):
	imageArray = imageArray.astype(np.float64)
	Y = (imageArray[:,0] + 2*imageArray[:,1] + imageArray[:,2]) / 4
	U = imageArray[:,0] - imageArray[:,1]
	V = imageArray[:,2] - imageArray[:,1]
	imageArray[:,0] = Y
	imageArray[:,1] = U
	imageArray[:,2] = V
	return imageArray

original = getImageArray(sys.argv[1])
distorted = getImageArray(sys.argv[2])

original = RGBToYUVRCT(original)
distorted = RGBToYUVRCT(distorted)

PSNRy = PSNR(original[:,0], distorted[:,0])
PSNRu = PSNR(original[:,1], distorted[:,1])
PSNRv = PSNR(original[:,2], distorted[:,2])

Cw = 7000000/(120000000 + 7000000)
Rw = 120000000/(120000000 + 7000000)
CQM = PSNRy * Rw + ((PSNRu + PSNRv)/2) * Cw
print('%.06f\t%s' % (CQM, sys.argv[2]))
