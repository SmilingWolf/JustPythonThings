import os, sys, math
from PIL import Image

def histEQ(frameGray):
	histeqFrame = []
	histDict = {}
	transformsDict = {}
	for elem in frameGray:
		if elem not in histDict:
			histDict[elem] = 0
		histDict[elem] += 1
	total = 0
	for intensity in sorted(histDict):
		total += histDict[intensity]
		transformsDict[intensity] = int(round((255 / float(len(frameGray))) * total))
	for pixel in frameGray:
		histeqFrame.append(transformsDict[pixel])
	return histeqFrame

if len(sys.argv) < 2:
	print('Usage:')
	print('%s file1' % sys.argv[0])
	sys.exit(-1)

fileName, fileExt = os.path.splitext(sys.argv[1])
imInput = Image.open(sys.argv[1])
frameGray = list(imInput.convert('L').getdata())
imSizes = imInput.size
imInput.close()

imOutput = Image.new('L', imSizes)
imOutput.putdata(frameGray)
imOutput.save('%s.grayscale.png' % fileName, 'PNG')
imInput.close()

frameHist = histEQ(frameGray)
imOutput = Image.new('L', imSizes)
imOutput.putdata(frameHist)
imOutput.save('%s.histeq.png' % fileName, 'PNG')
imInput.close()

