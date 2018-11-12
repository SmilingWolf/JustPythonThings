import os, sys
from PIL import Image

def combinePlanes(RPlane, GPlane, BPlane):
	i = 0
	newImage = []
	while i < len(RPlane):
		newPixel = (RPlane[i], GPlane[i], BPlane[i])
		newImage.append(newPixel)
		i += 1
	return newImage

def nearestNeighbor(frame, x, y, x2, y2):
	newList = [0] * (x2 * y2)

	xRatio = float(x) / x2
	yRatio = float(y) / y2

	i = 0
	offset = 0
	while i < y2:
		j = 0
		while j < x2:
			pixelX = int(j * xRatio)
			pixelY = int(i * yRatio)
			listIndex = (pixelY * x) + pixelX

			pixelX1 = frame[listIndex]

			newList[offset] = pixelX1
			offset += 1
			j += 1
		i += 1
	return newList

if len(sys.argv) < 2:
	print('Usage:')
	print('%s <image> <new x> <new y>' % sys.argv[0])
	sys.exit(-1)

fileName, fileExt = os.path.splitext(sys.argv[1])
imInput = Image.open(sys.argv[1])
RPlane = list(imInput.getdata(0))
GPlane = list(imInput.getdata(1))
BPlane = list(imInput.getdata(2))
imSizes = imInput.size
imInput.close()

print('Original sizes: %dx%d' % (imSizes[0], imSizes[1]))
print('Resizing to %sx%s' % (sys.argv[2], sys.argv[3]))
largerRPlane = nearestNeighbor(RPlane, imSizes[0], imSizes[1], int(sys.argv[2]), int(sys.argv[3]))
largerGPlane = nearestNeighbor(GPlane, imSizes[0], imSizes[1], int(sys.argv[2]), int(sys.argv[3]))
largerBPlane = nearestNeighbor(BPlane, imSizes[0], imSizes[1], int(sys.argv[2]), int(sys.argv[3]))
largerFrame = combinePlanes(largerRPlane, largerGPlane, largerBPlane)

newSizes = (int(sys.argv[2]), int(sys.argv[3]))
imOutput = Image.new('RGB', newSizes)
imOutput.putdata(largerFrame)
imOutput.save('%s.neighbor.png' % fileName, 'PNG')
imInput.close()
