#!/usr/bin/python3
import os
import sys
from Bauer.Block import Block

if len(sys.argv) < 2:
	print("Usage: %s [Infilename]" % (sys.argv[0]))
	sys.exit(1)
	

f = open(sys.argv[1], "rb")
data = f.read(64)
data = Block(data)
blocks = data.partition(1)

#print hexadecimal
for i in range(len(blocks)):
	if  (i%16)==0:
		print("\n", end="")
	else:
		if((i%8)==0):
			print(" ", end="")
	
	print("".join("%02x " % (x) for x in blocks[i]._data), end="")
print("")

#print binary
for i in range(len(blocks)):
	if  (i%16)==0:
		print("\n", end="")
	else:
		if((i%8)==0):
			print(" ", end="")
	
	print( "".join("{:08b} ".format(x) for x in blocks[i]._data), end="")
print("")

print("end")