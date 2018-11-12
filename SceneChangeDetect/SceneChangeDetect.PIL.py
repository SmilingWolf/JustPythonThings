# Scene change detector
# Works on images in various formats thanks to the Python Imaging Library
# More specifically, the Pillow fork

# Algos and (some) thresholds from:
# "Fast Pixel-Based Video Scene Change Detection" by Xiaoquan Yi and Nam Ling

import os, sys, glob, random
from PIL import Image

def calcMAFD(frame1, frame2):
	i = 0
	total = 0
	while (i < min(len(frame1), len(frame2))):
		intensity1 = frame1[i]
		intensity2 = frame2[i]
		total += abs(intensity2 - intensity1)
		i += 1
	MAFD = total / float(len(frame1))
	return MAFD

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

def frameVariance(frameGray, MAFD):
	total = 0
	for pixel in frameGray:
		total += abs(pixel - MAFD)
	return total / float(len(frameGray))

def isSceneChange(frameBuf, frameGray1, frameGray2):
	if len(frameGray1) != len(frameGray2):
		return True

	normMAFD = calcMAFD(frameGray1, frameGray2)
	print normMAFD
	if (normMAFD < 14):
		return False

	frameHist1 = histEQ(frameGray1)
	frameHist2 = histEQ(frameGray2)
	histMAFD1 = calcMAFD(frameHist1, frameHist2)
	print histMAFD1
	if (histMAFD1 < 40):
		return False

	frameHist0 = histEQ(framesBuf[0])
	histMAFD0 = calcMAFD(frameHist0, frameHist1)
	SDMAFD = histMAFD1 - histMAFD0
	print SDMAFD

	ADFV = abs(frameVariance(frameGray2, histMAFD1) - frameVariance(frameGray1, histMAFD0))
	print ADFV
	if (normMAFD > 42 and histMAFD1 < 100 and ADFV > 23):
		return True
	elif (ADFV < 2 or SDMAFD < 5):
		return False
	return True

def shiftLeft(frameBuf, frame):
	frameBuf.append(frame)
	if (len(frameBuf) > 2):
		del frameBuf[0]
	return frameBuf

if len(sys.argv) < 2:
	print('Usage:')
	print('%s <directory>' % sys.argv[0])
	sys.exit(-1)

imagesPaths = glob.glob(sys.argv[1] + '/*.bmp')
imagesPaths += glob.glob(sys.argv[1] + '/*.png')
imagesPaths += glob.glob(sys.argv[1] + '/*.jpg')

if len(imagesPaths) < 2:
	print('Not enough images to parse. Wrong/nonexistent directory?')
	sys.exit(-1)

i = 1
truck = []
bucket = []
framesBuf = []
while i < (len(imagesPaths)):
	frameGray1 = list(Image.open(imagesPaths[i-1]).convert('L').getdata())
	frameGray2 = list(Image.open(imagesPaths[i]).convert('L').getdata())
	framesBuf = shiftLeft(framesBuf, frameGray1)
	if i == 1:
		bucket.append(imagesPaths[i-1])

	doesItChange = isSceneChange(framesBuf, frameGray1, frameGray2)
	if doesItChange == False:
		print '%s -> %s: same sequence' % (imagesPaths[i-1], imagesPaths[i])
	else:
		print '%s -> %s: different sequence' % (imagesPaths[i-1], imagesPaths[i])
		truck.append(bucket)
		bucket = []
	bucket.append(imagesPaths[i])

	sys.stdout.flush()
	i += 1
truck.append(bucket)

script = open('script.sh', 'a+b')
for bucket in truck:
	#sample = random.choice(bucket)
	sample = bucket[0]
	script.write('cp --parents %s samples/\r\n' % sample)
