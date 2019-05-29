import sys, os

n = int(sys.argv[1])

for i in range(n):
    addr = os.urandom(4).hex()
    sys.stdout.write(addr+"\n")

sys.stdout.write("-1")
