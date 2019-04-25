import numpy as np
from PIL import Image

# "manual" way, slow
def oldMSE(array1, array2):
	i = 0
	error = 0
	while i < len(array1):
		error += pow(array1[i] - array2[i], 2)
		i += 1
	return float(error) / len(array1)

# have numpy cycle for us; twice as fast as oldMSE
def MSE(array1, array2):
	error = ((array1 - array2) ** 2).mean(axis=None)
	return error

def PSNR(array1, array2):
	error = MSE(array1, array2)
	return 10 * np.log10(65025 / error)

Image1 = Image.open('46657164_p1.png')
Image1Y = np.array(Image1.convert('L').getdata())
Image1.close()

Image2 = Image.open('46657164_p1.jpg')
Image2Y = np.array(Image2.convert('L').getdata())
Image2.close()

print(PSNR(Image1Y, Image2Y))
