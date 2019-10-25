import sys
from random import randint

manual_text = '''Usage:
  python genRealAddrs.py [n_sample] - outputs n_sample lines with 32bits hexadecimal memory addresses

  n_sample = size of output sample'''

if len(sys.argv) != 2:
    print manual_text
    exit(0)

n_bits = 32
n_sample = int(sys.argv[1])

upperbound = (1 << n_bits) - 1

file_lines = []

with open("time,addr.txt", 'r') as f:
    file_lines = f.readlines()

n_lines = len(file_lines)
start_line = randint(0, n_lines - n_sample)

file_lines = file_lines[start_line : start_line + n_sample]

def addr(a):
    return int(a, 16) % upperbound

def timestamp(t):
    return int(t.replace('.', ''))

file_lines = map(lambda x: x.split(': '), file_lines)
file_lines = map(lambda x: (timestamp(x[0]), hex(addr(x[1]))), file_lines)

for _ in file_lines:
    print _[1]
