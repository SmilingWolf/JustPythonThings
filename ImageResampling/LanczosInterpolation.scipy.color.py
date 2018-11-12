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

def resizePlane(plane, kernel, x, y, x2, y2):
	xRatio = float(x) / (x2)
	yRatio = float(y) / (y2)
	expandedPixels = numpy.array(numpy.zeros((y2, x2), numpy.float64))

	for i in xrange(y):
		newY = int(i / yRatio)
		for j in xrange(x):
			newX = int(j / xRatio)
			expandedPixels[newY][newX] = plane[i][j]

	interpolated = signal.convolve(expandedPixels, kernel, 'same')
	return interpolated

if len(sys.argv) < 2:
	print('Usage:')
	print('%s <image> <new x> <new y>' % sys.argv[0])
	sys.exit(-1)

x2 = int(sys.argv[2])
y2 = int(sys.argv[3])

fileName, fileExt = os.path.splitext(sys.argv[1])
imInput = Image.open(sys.argv[1])
imSizes = imInput.size
RPlane = numpy.array(imInput.getdata(0), numpy.float64).reshape((imSizes[1], imSizes[0]))
GPlane = numpy.array(imInput.getdata(1), numpy.float64).reshape((imSizes[1], imSizes[0]))
BPlane = numpy.array(imInput.getdata(2), numpy.float64).reshape((imSizes[1], imSizes[0]))
imInput.close()

# Nearest Neigbor double?
NearestN2DKernel = [[1.00, 1.00, 0.00],
                    [1.00, 1.00, 0.00],
                    [0.00, 0.00, 0.00]]

# Bilinear double?
Bilinear2DKernel = [[0.25, 0.50, 0.25],
                    [0.50, 1.00, 0.50],
                    [0.25, 0.50, 0.25]]

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
resizeKernels = [NearestN2DKernel, Bilinear2DKernel, Lanczos2DKernel]

resizedR = resizePlane(RPlane, resizeKernels[2], imSizes[0], imSizes[1], x2, y2)
resizedG = resizePlane(GPlane, resizeKernels[2], imSizes[0], imSizes[1], x2, y2)
resizedB = resizePlane(BPlane, resizeKernels[2], imSizes[0], imSizes[1], x2, y2)

rgbArray = numpy.zeros((y2, x2, 3), 'uint8')
rgbArray[..., 0] = numpy.clip(resizedR, 0, 255)
rgbArray[..., 1] = numpy.clip(resizedG, 0, 255)
rgbArray[..., 2] = numpy.clip(resizedB, 0, 255)

newSizes = (int(sys.argv[2]), int(sys.argv[3]))
imOutput = Image.fromarray(rgbArray, 'RGB')
imOutput.save('%s.lanczos.png' % fileName, 'PNG')
imInput.close()
