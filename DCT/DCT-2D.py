import math

# DCT-II and DCT-III 1D matrix init
def InitDCT1DMatrix(matrixLength):
	N = matrixLength
	DCTMatrix = []
	for u in xrange(N):
		DCTRow = []
		for x in xrange(N):
			DCTRow.append(math.cos((math.pi * (2*x + 1) * u) / (2*N)))
		DCTMatrix.append(DCTRow)
	return DCTMatrix

# DCT-II and DCT-III 2D matrix init
def InitDCT2DMatrix(Matrix1D):
	N = len(Matrix1D)
	DCT2DMatrix = []
	for u in xrange(N):
		DCT2DRow = []
		for v in xrange(N):
			DCT1DMatrix = []
			for x in xrange(N):
				DCT1DRow = []
				for y in xrange(N):
					ucos = Matrix1D[u][x]
					vcos = Matrix1D[v][y]
					product = ucos * vcos
					DCT1DRow.append(product)
				DCT1DMatrix.append(DCT1DRow)
			# print DCT1DMatrix
			DCT2DRow.append(DCT1DMatrix)
		DCT2DMatrix.append(DCT2DRow)
	return DCT2DMatrix

# Do the forward 2D transform
def DCTII2D(imageBlock, DCTMatrix):
	N = len(DCTMatrix[0])
	TXMatrix = []
	for u in xrange(N):
		TXRow = []
		alphau = math.sqrt(float(1)/N) if u == 0 else math.sqrt(float(2)/N)
		for v in xrange(N):
			sommax = 0
			alphav = math.sqrt(float(1)/N) if v == 0 else math.sqrt(float(2)/N)
			for x in xrange(N):
				sommay = 0
				for y in xrange(N):
					sommay += imageBlock[x][y] * DCTMatrix[u][v][x][y]
				sommax += sommay
			finalCuv = alphau * alphav * sommax
			roundedCuv = finalCuv
			TXRow.append(0.0 if roundedCuv == -0.0 else roundedCuv)
		print TXRow
		TXMatrix.append(TXRow)
	return TXMatrix

# Do the inverse 2D transform
def DCTIII2D(imageBlock, DCTMatrix):
	N = len(DCTMatrix[0])
	TXMatrix = []
	for x in xrange(N):
		TXRow = []
		for y in xrange(N):
			sommau = 0
			for u in xrange(N):
				sommav = 0
				for v in xrange(N):
					alphau = math.sqrt(float(1)/N) if u == 0 else math.sqrt(float(2)/N)
					alphav = math.sqrt(float(1)/N) if v == 0 else math.sqrt(float(2)/N)
					sommav += alphau * alphav * imageBlock[u][v] * DCTMatrix[u][v][x][y]
				sommau += sommav
			TXRow.append(int(round(sommau)))
		print TXRow
		TXMatrix.append(TXRow)
	return TXMatrix

def StupidFwdQuant(imageBlock, quantVal):
	TXMatrix = []
	for row in imageBlock:
		TXRow = []
		for coeff in row:
			finalQuantized = int(round(coeff / quantVal))
			TXRow.append(finalQuantized)
		print TXRow
		TXMatrix.append(TXRow)
	return TXMatrix

def StupidInvQuant(imageBlock, quantVal):
	TXMatrix = []
	for row in imageBlock:
		TXRow = []
		for coeff in row:
			TXRow.append(coeff * quantVal)
		print TXRow
		TXMatrix.append(TXRow)
	return TXMatrix

N = 8
LumaValues = [[181, 180, 180, 178, 177, 176, 175, 174],
			  [180, 180, 179, 178, 176, 176, 175, 173],
			  [180, 179, 178, 178, 177, 175, 173, 172],
			  [180, 180, 179, 178, 175, 174, 173, 172],
			  [181, 180, 178, 176, 176, 175, 173, 172],
			  [180, 179, 177, 177, 175, 174, 172, 170],
			  [179, 179, 177, 175, 174, 173, 172, 170],
			  [180, 178, 176, 175, 173, 172, 171, 169]]

DCTMatrix1D = InitDCT1DMatrix(N)
DCTMatrix2D = InitDCT2DMatrix(DCTMatrix1D)
TXValues = DCTII2D(LumaValues, DCTMatrix2D)
TXValues = StupidFwdQuant(TXValues, 6)
# ----
TXValues = StupidInvQuant(TXValues, 6)
RecoveredVals = DCTIII2D(TXValues, DCTMatrix2D)
