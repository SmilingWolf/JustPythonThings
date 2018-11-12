import math

# DCT-II and DCT-III matrix init
def InitDCT1DMatrix(matrixLength):
	N = matrixLength
	DCTMatrix = []
	for u in xrange(N):
		DCTRow = []
		for x in xrange(N):
			DCTRow.append(math.cos((math.pi * (2*x + 1) * u) / (2*N)))
		DCTMatrix.append(DCTRow)
	return DCTMatrix

# Do the forward 1D transform
def DCTII1D(imageBlock, DCTMatrix):
	N = len(DCTMatrix[0])
	TXValues = []
	for u in xrange(N):
		somma = 0
		alpha = math.sqrt(float(1)/N) if u == 0 else math.sqrt(float(2)/N)
		for x in xrange(N):
			somma += imageBlock[x] * DCTMatrix[u][x]
		finalCu = alpha * somma
		roundedCu = round(finalCu)
		TXValues.append(0.0 if roundedCu == -0.0 else roundedCu)
	return TXValues

# Do the inverse 1D transform
def DCTIII1D(imageBlock, DCTMatrix):
	N = len(DCTMatrix[0])
	TXValues = []
	for x in xrange(N):
		somma = 0
		for u in xrange(N):
			alpha = math.sqrt(float(1)/N) if u == 0 else math.sqrt(float(2)/N)
			somma += alpha * imageBlock[u] * DCTMatrix[u][x]
		TXValues.append(round(somma))
	return TXValues

N = 8
LumaValues = [181, 180, 180, 178, 177, 176, 175, 174]

DCTMatrix = InitDCT1DMatrix(N)

TXValues = DCTII1D(LumaValues, DCTMatrix)
print TXValues

RecoveredVals = DCTIII1D(TXValues, DCTMatrix)
print RecoveredVals
