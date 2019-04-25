import sys
from scipy.stats import spearmanr

if len(sys.argv) != 3:
	sys.exit(0)

file1 = open(sys.argv[1], 'r').readlines()
file2 = open(sys.argv[2], 'r').readlines()

file1 = [float(x.split('\t')[0].split(' ')[0]) for x in file1]
file2 = [float(x.split('\t')[0].split(' ')[0]) for x in file2]

scores = list(zip(file1, file2))

inOrder = sorted(scores, reverse=True)
print(('%.04f %s') % (spearmanr(inOrder)[0], sys.argv[2]))
