import sys
from scipy.stats import spearmanr

# 25 images
# 24 distortions
#  5 intensities
def getDist(scores, distNum):
	newScores = []
	for x in range(0, 25):
		for z in range(0, 5):
			index = x*(24*5) + distNum*5 + z
			newScores.append(scores[index])
	return newScores

if len(sys.argv) != 3:
	sys.exit(0)

file1 = open(sys.argv[1], 'r').readlines()
file2 = open(sys.argv[2], 'r').readlines()

file1 = [float(x.split('\t')[0].split(' ')[0]) for x in file1]
file2 = [float(x.split('\t')[0].split(' ')[0]) for x in file2]

scores = list(zip(file1, file2))

dist1  = getDist(scores, 0)  # Additive Gaussian noise
dist2  = getDist(scores, 1)  # Additive noise in color components is more intensive than additive noise in the luminance component
dist3  = getDist(scores, 2)  # Spatially correlated noise
dist4  = getDist(scores, 3)  # Masked noise
dist5  = getDist(scores, 4)  # High frequency noise
dist6  = getDist(scores, 5)  # Impulse noise
dist7  = getDist(scores, 6)  # Quantization noise
dist8  = getDist(scores, 7)  # Gaussian blur
dist9  = getDist(scores, 8)  # Image denoising
dist10 = getDist(scores, 9)  # JPEG compression
dist11 = getDist(scores, 10) # JPEG2000 compression
dist12 = getDist(scores, 11) # JPEG transmission errors
dist13 = getDist(scores, 12) # JPEG2000 transmission errors
dist14 = getDist(scores, 13) # Non eccentricity pattern noise
dist15 = getDist(scores, 14) # Local block-wise distortions of different intensity
dist16 = getDist(scores, 15) # Mean shift (intensity shift)
dist17 = getDist(scores, 16) # Contrast change
dist18 = getDist(scores, 17) # Change of color saturation
dist19 = getDist(scores, 18) # Multiplicative Gaussian noise
dist20 = getDist(scores, 19) # Comfort noise
dist21 = getDist(scores, 20) # Lossy compression of noisy images
dist22 = getDist(scores, 21) # Image color quantization with dither
dist23 = getDist(scores, 22) # Chromatic aberrations
dist24 = getDist(scores, 23) # Sparse sampling and reconstruction

inOrder = sorted(dist10+dist11, reverse=True)
print(('%.04f %s') % (spearmanr(inOrder)[0], sys.argv[2]))
