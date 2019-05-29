import sys
from random import randint

usage = '''usage:
  python genLinearAddrs.py [n_sample] - outputs n_sample lines with 32bits hexadecimal memory addresses

  n_sample = size of output sample'''

if len(sys.argv) != 2:
    print usage
    exit(0)

n_bits = 32
n_sample = int(sys.argv[1])

upperbound = (1 << n_bits) - 1
start = randint(0, upperbound - n_sample)

for addr in xrange(start, start + n_sample):
    print hex(addr)


