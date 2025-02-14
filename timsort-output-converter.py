
import sys

filename = sys.argv[1]
f = open(filename, 'r')
for l in f:
	l = l.split()
	l[0] = float(l[0])
	l[1] = float(l[1])
	print(str(round(l[0], 16)), str(round(l[1], 16)))
