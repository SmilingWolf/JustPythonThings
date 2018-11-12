import os, sys, math
from PIL import Image
import numpy
from scipy import signal

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

def init2DKernel(xRatio, yRatio, taps):
	j = 0
	weigthsTable = []
	while j <= yRatio*taps:
		i = 0
		weigthsLine = []
		while i <= xRatio*taps:
			x = i / float(xRatio)
			y = j / float(yRatio)
			xWeigth = LanczosWindow(x, taps)
			yWeigth = LanczosWindow(y, taps)
			Sx = xWeigth*yWeigth
			weigthsLine.append(float(Sx))
			i += 1
		weigthsLine = weigthsLine[:0:-1] + weigthsLine
		j += 1
		weigthsTable.append(weigthsLine)
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

def norm(pixels):
    return 255.*numpy.absolute(pixels)/numpy.max(pixels)

if len(sys.argv) < 2:
	print('Usage:')
	print('%s <image> <new x> <new y>' % sys.argv[0])
	sys.exit(-1)

x2 = int(sys.argv[2])
y2 = int(sys.argv[3])

fileName, fileExt = os.path.splitext(sys.argv[1])
imInput = Image.open(sys.argv[1])
frameGray = numpy.array(imInput.convert('L'), numpy.float64)
imSizes = imInput.size
imInput.close()

taps = 4
xBigRatio = float(sys.argv[2]) / imSizes[0]
yBigRatio = float(sys.argv[3]) / imSizes[1]
Lanczos2DKernel = init2DKernel(xBigRatio, yBigRatio, taps)

# Sharpen
Sharpen2DKernel = [[-1, -1, -1],
                   [-1,  9, -1],
				   [-1, -1, -1]]

# Edge detect
Edge2DKernel    = [[-1, -1, -1],
                   [-1,  8, -1],
				   [-1, -1, -1]]

# Raise
Raise2DKernel   = [[ 0,  0, -2],
                   [ 0,  2,  0],
				   [ 1,  0,  0]]

effectsKernels = [Sharpen2DKernel, Edge2DKernel, Raise2DKernel]
resizeKernels = [Lanczos2DKernel]

expandedPixels = numpy.array(numpy.zeros((y2, x2), numpy.float64))

xRatio = float(imSizes[0]) / (x2)
yRatio = float(imSizes[1]) / (y2)

for i in xrange(imSizes[1]):
	newY = int(i / yRatio)
	for j in xrange(imSizes[0]):
		newX = int(j / xRatio)
		expandedPixels[newY][newX] = frameGray[i][j]

interpolated = signal.convolve(expandedPixels, resizeKernels[0], 'same')

newSizes = (int(sys.argv[2]), int(sys.argv[3]))
imOutput = Image.fromarray(numpy.clip(interpolated, 0, 255).astype(numpy.uint8), 'L')
imOutput.save('%s.lanczos.png' % fileName, 'PNG')
imInput.close()
