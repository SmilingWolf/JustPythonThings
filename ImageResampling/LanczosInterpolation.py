import os, sys, math
from PIL import Image

M_PI = math.pi

def frange(start, stop, step):
	x = start
	while x < stop:
		yield x
		x += step

def sinc(x):
	if x == 0:
		return 1
	else:
		return math.sin(M_PI * x) / (M_PI * x)

def LanczosWindow(x, a):
	# Lanczos kernel: at x = 0, it has value 1
	if x == 0:
		return 1

	# Lanczos kernel: zero at every integer argument x
	# Check if x has got a fractional part, return 0 if it is an integer
	# Gotta do it manually because the loss of precision and error propagation
	# cause the function to output near-zero-but-not-zero values
	if x % 1 == 0:
		return 0

	if abs(x) < a:
		return sinc(x) * sinc(x / a)
	else:
		return 0

def initKernel(ratio, taps):
	i = 0
	weigthsTable = []
	while i <= ratio*taps:
		x = i / float(ratio)
		weigthsTable.append(LanczosWindow(x, taps))
		i += 1
	weigthsTable = weigthsTable[:0:-1] + weigthsTable
	return weigthsTable

def expandBuffer(pixels, ratio):
	i = 0
	lastX = -1
	expandedPixels = []
	while i < len(pixels) * ratio:
		index = int(i / float(ratio))
		if lastX == index:
			newUnit = 0
		else:
			lastX = index
			newUnit = pixels[index]
		expandedPixels.append(newUnit)
		i += 1
	return expandedPixels

def convolution(pixels, kernel, x):
	i = 0
	Sx = 0
	pixelIndex = x - ((len(kernel) - 1) / 2)
	while i < len(kernel):
		if (0 <= pixelIndex + i < len(pixels)):
			Sx += pixels[pixelIndex + i] * kernel[i]
		i += 1
	return int(Sx)

if len(sys.argv) < 2:
	print('Usage:')
	print('%s <image> <new x> <new y>' % sys.argv[0])
	sys.exit(-1)

fileName, fileExt = os.path.splitext(sys.argv[1])
imInput = Image.open(sys.argv[1])
frameGray = list(imInput.convert('L').getdata())
imSizes = imInput.size
imInput.close()

taps = 4
xRatio = float(sys.argv[2]) / imSizes[0]
yRatio = float(sys.argv[3]) / imSizes[1]
LanczosKernel = initKernel(xRatio, taps)

# nearest neighbor doubling
#LanczosKernel = [1, 1, 0]

# linear resample doubling
#LanczosKernel = [0.5, 1, 0.5]

largerXFrame = []
for y in xrange(imSizes[1]):
	interpPixels = []
	xPixels = frameGray[y*imSizes[0]:y*imSizes[0]+imSizes[0]]
	expandedPixels = expandBuffer(xPixels, xRatio)
	for x in xrange(len(expandedPixels)):
		interpPixels.append(convolution(expandedPixels, LanczosKernel, x))
	largerXFrame += interpPixels

largerXYFrame = [None] * int((imSizes[0]*xRatio) * (imSizes[1]*yRatio))
for y in xrange(int(imSizes[0]*xRatio)):
	interpPixels = []
	yPixels = [largerXFrame[x] for x in xrange(y, y+int(imSizes[1]*imSizes[0]*xRatio), int(imSizes[0]*xRatio))]
	expandedPixels = expandBuffer(yPixels, yRatio)
	for x in xrange(len(expandedPixels)):
		interpPixels.append(convolution(expandedPixels, LanczosKernel, x))
	for index, pixel in enumerate(interpPixels):
		largerXYFrame[y+int(index*imSizes[0]*xRatio)] = pixel

newSizes = (int(sys.argv[2]), int(sys.argv[3]))
imOutput = Image.new('L', newSizes)
imOutput.putdata(largerXYFrame)
imOutput.save('%s.lanczos.png' % fileName, 'PNG')
imInput.close()
