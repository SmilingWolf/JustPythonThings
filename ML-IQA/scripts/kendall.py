import sys
from scipy.stats import kendalltau

if len(sys.argv) != 3:
	sys.exit(0)

file1 = open(sys.argv[1], 'r').readlines()
file2 = open(sys.argv[2], 'r').readlines()

file1 = [float(x.split('\t')[0].split(' ')[0]) for x in file1]
file2 = [float(x.split('\t')[0].split(' ')[0]) for x in file2]

print(('%.04f %s') % (kendalltau(file1, file2)[0], sys.argv[2]))
