import os, sys
from PIL import Image

def bilinearInterpolation(frame, x, y, x2, y2):
	newList = [0] * (x2 * y2)

	xRatio = float(x - 1) / x2
	yRatio = float(y - 1) / y2

	i = 0
	offset = 0
	while i < y2:
		j = 0
		while j < x2:
			pixelX = int(j * xRatio)
			pixelY = int(i * yRatio)
			xDelta = (j * xRatio) - pixelX
			yDelta = (i * yRatio) - pixelY
			listIndex = (pixelY * x) + pixelX

			pixelX1 = frame[listIndex]
			pixelX2 = frame[listIndex + 1]
			pixelY1 = frame[listIndex + x]
			pixelY2 = frame[listIndex + x + 1]

			newPixel = pixelX1 * (1 - xDelta) * (1 - yDelta) + \
					   pixelX2 * xDelta * (1 - yDelta) + \
					   pixelY1 * (1 - xDelta) * yDelta + \
					   pixelY2 * xDelta * yDelta
			newPixel = int(round(newPixel))

			newList[offset] = newPixel
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
frameGray = list(imInput.convert('L').getdata())
imSizes = imInput.size
imInput.close()

print('Original sizes: %dx%d' % (imSizes[0], imSizes[1]))
print('Resizing to %sx%s' % (sys.argv[2], sys.argv[3]))
largerFrame = bilinearInterpolation(frameGray, imSizes[0], imSizes[1], int(sys.argv[2]), int(sys.argv[3]))

newSizes = (int(sys.argv[2]), int(sys.argv[3]))
imOutput = Image.new('L', newSizes)
imOutput.putdata(largerFrame)
imOutput.save('%s.bilinear.png' % fileName, 'PNG')
imInput.close()
