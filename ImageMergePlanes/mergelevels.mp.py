#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os, sys, glob, numpy
from PIL import Image
from multiprocessing import Pool

def rgb2ycbcr(im):
	xform = numpy.array([[.299, .587, .114], [-.168736, -.331264, .5], [.5, -.418688, -.081312]])
	ycbcr = im.dot(xform.T)
	ycbcr[:,:,[1,2]] += 128
	return numpy.float64(ycbcr)

def ycbcr2rgb(im):
	xform = numpy.array([[1, 0, 1.402], [1, -0.344136, -.714136], [1, 1.772, 0]])
	rgb = im.astype(numpy.float64)
	rgb[:,:,[1,2]] -= 128
	rgb = rgb.dot(xform.T)
	numpy.clip(rgb, 0, 255, rgb)
	return numpy.uint8(rgb)

def mergeImages(file):
	file = file.decode('utf-8')

	fileName = os.path.basename(file)
	fileName, fileExt = os.path.splitext(fileName)
	YSource = Image.open(file)
	imSizes = YSource.size

	YPlane = numpy.array(YSource.getdata(), numpy.float64).reshape((imSizes[1], imSizes[0], 4))
	YPlane = YPlane[:,:,[0, 1, 2]]
	YPlane = rgb2ycbcr(YPlane)[:,:,0]

	CbCrSource = Image.open(u'waifu2x/%s.png' % fileName)
	CbCrSource = CbCrSource.resize((imSizes[0], imSizes[1]), Image.LANCZOS)

	if CbCrSource.mode == 'L':
		return '%s: grayscale image' % file
	elif CbCrSource.mode == 'RGBA':
		CbCrPlane = numpy.array(CbCrSource.getdata(), numpy.float64).reshape((imSizes[1], imSizes[0], 4))
		AlphaPlane = numpy.uint8(CbCrPlane[:,:,3])
		CbCrPlane = CbCrPlane[:,:,[0, 1, 2]]
	else:
		CbCrPlane = numpy.array(CbCrSource.getdata(), numpy.float64).reshape((imSizes[1], imSizes[0], 3))
		AlphaPlane = None

	CbCrPlane = rgb2ycbcr(CbCrPlane)
	CbPlane = CbCrPlane[:,:,1]
	CrPlane = CbCrPlane[:,:,2]

	YCArray = numpy.zeros((imSizes[1], imSizes[0], 3), numpy.float64)
	YCArray[..., 0] = YPlane
	YCArray[..., 1] = CbPlane
	YCArray[..., 2] = CrPlane

	RGBArray = ycbcr2rgb(YCArray)
	if AlphaPlane is None:
		saveMode = 'RGB'
	else:
		RGBArray = numpy.dstack((RGBArray, AlphaPlane))
		saveMode = 'RGBA'

	imOutput = Image.fromarray(RGBArray, saveMode)
	imOutput.save(u'merged/%s.webp' % fileName, 'WebP', lossless=True, quality=100, method=6)
	return file

if __name__ == '__main__':
	imagesList = glob.glob(u'android/*.webp')

	newList = []
	for filename in imagesList:
		newList.append(filename.encode('utf-8'))

	pool = Pool(processes=7)
	successList = pool.imap(mergeImages, newList)
	pool.close()
	pool.join()

	print 'Successfully merged:'
	for elem in successList:
		print elem.encode('utf-8')
