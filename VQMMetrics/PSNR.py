from PIL import Image
import math, numpy

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
	error = MSE(Image1Y, Image2Y)
	return 10 * math.log(65025 / error, 10)

Image1 = Image.open('46657164_p1.png')
Image1Y = numpy.array(Image1.convert('L').getdata())
print Image1Y[1200*0+0:1200*0+8]
print Image1Y[1200*1+0:1200*1+8]
print Image1Y[1200*2+0:1200*2+8]
print Image1Y[1200*3+0:1200*3+8]
print Image1Y[1200*4+0:1200*4+8]
print Image1Y[1200*5+0:1200*5+8]
print Image1Y[1200*6+0:1200*6+8]
print Image1Y[1200*7+0:1200*7+8]
Image1.close()

Image2 = Image.open('46657164_p1.jpg')
Image2Y = numpy.array(Image2.convert('L').getdata())
Image2.close()

print PSNR(Image1Y, Image2Y)
