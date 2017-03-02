#!/usr/bin/python3
import os
from Bauer.Block import Block, BitString

# verify hypothesis that 1026 bits can generate all data required to emulate the scrambler
# 19 bits of every LFSR stretch are enough to generate a whole keyblock
# produce the generator vectors and two overlapping streams
# other two overlapping streams are produced from the data present in the first two


# generate keyblocks based on LFSR keys
def produceKeyblocks(lfsrKeys):
	keyblock = Block()
	for j in range(0,len(lfsrKeys)): #iterate through all lfsrkeys
		for k in range(0,4): #iterate though PRBS words
			#print(str(lfsrKeys[i][j]._strm[3-k:19-k])) 
			keyblock += Block().setfrombits(lfsrKeys[j]._strm[3-k:19-k]) # shift the LFSR keys
			
	return keyblock


#based on a binary input file generate the other overlapping stream in the output file..
def generateOtherOverlappingstreams(infile, outfile):
	#The mapping is as follows
	#{1}-0x20 XOR {1}-0x28 = {4}-0x0
	#{1}-0x28 XOR {1}-0x30 = {4}-0x8
	#{1}-0x30 XOR {1}-0x38 = {4}-0x10
	#{1}-0x38 XOR {1}-0x40 = {4}-0x18
	#{1}-0x40 XOR {1}-0x48 = {4}-0x20
	#{1}-0x48 XOR {1}-0x50 = {4}-0x28
	#{1}-0x50 XOR {1}-0x58 = {4}-0x30
	#{1}-0x50 XOR {1}-0x58 XOR {1}-0x18 = {4}-0x38
	#{1}-0x50 XOR {1}-0x58 XOR {1}-0x18 XOR {1}-0x20 = {4}-0x40
	#{1}-0x50 XOR {1}-0x58 XOR {1}-0x18 XOR {1}-0x20 XOR {1}-0x28 = {4}-0x48
	#{1}-0x50 XOR {1}-0x58 XOR {1}-0x18 XOR {1}-0x20 XOR {1}-0x28 XOR {1}-0x30 = {4}-0x50
	#{1}-0x50 XOR {1}-0x58 XOR {1}-0x18 XOR {1}-0x20 XOR {1}-0x28 XOR {1}-0x30 XOR {1}-0x38 = {4}-0x58

	outOffset= 0x0
	inOffset = 0x20
	while outOffset <= 0x58:
		outfile.seek(outOffset)
		infile.seek(inOffset)
		dxor = bytes()

		if(outOffset <= 0x30):
			d1 = infile.read(8) #read LFSR stretch
			d2 = infile.read(8) #read LFSR stretch

			dxor = bytes(c1 ^ c2 for (c1, c2) in zip(d1, d2))
			inOffset = inOffset + 8

		else:
			inOffset = 0x50 #no longer update inOffset as 0x50 and 0x58 keep being xored in..
			infile.seek(inOffset)
			d1 = infile.read(8) #read LFSR stretch
			d2 = infile.read(8) #read LFSR stretch
			dxor = bytes(c1 ^ c2 for (c1, c2) in zip(d1, d2))
			vectorsToBeXoredIn = outOffset - 0x30
			while vectorsToBeXoredIn != 0:
				#print("here 0x%02x, data dxor=%s" % (vectorsToBeXoredIn+0x10, str(dxor)))
				infile.seek(vectorsToBeXoredIn+0x10)
				dxor = bytes(c1 ^ c2 for (c1, c2) in zip(dxor, infile.read(8)))
				vectorsToBeXoredIn = vectorsToBeXoredIn - 8


		#print("going to write to address outfile.tell=0x%02x, data dxor=%s" % (outfile.tell(), str(dxor)))
		outfile.write(dxor)

		outOffset = outOffset + 8
	
	
	
	

#lfsr keys for the generator vectors
generatorVectorsLfsrKeys = [[BitString("")]*8 for i in range(4)]

#00000040.bin
#generatorVectorsLfsrKeys for generatorvector[0]
generatorVectorsLfsrKeys[0][0] = BitString("0110000011000111000")
generatorVectorsLfsrKeys[0][1] = BitString("0111110001000100000")
generatorVectorsLfsrKeys[0][2] = BitString("0011000011001011010")
generatorVectorsLfsrKeys[0][3] = BitString("0101110000101101000")
generatorVectorsLfsrKeys[0][4] = BitString("0011101011011011000")
generatorVectorsLfsrKeys[0][5] = BitString("0100101000011110010")
generatorVectorsLfsrKeys[0][6] = BitString("0010011101011100000")
generatorVectorsLfsrKeys[0][7] = BitString("0000011011110000000")

#00000080.bin
#generatorVectorsLfsrKeys for generatorvector[1]
generatorVectorsLfsrKeys[1][0] = BitString("0100101001010010110")
generatorVectorsLfsrKeys[1][1] = BitString("0101101001010000101")
generatorVectorsLfsrKeys[1][2] = BitString("0100111101010110110")
generatorVectorsLfsrKeys[1][3] = BitString("0111101000110111101")
generatorVectorsLfsrKeys[1][4] = BitString("1100010111000011100")
generatorVectorsLfsrKeys[1][5] = BitString("0111010001101111111")
generatorVectorsLfsrKeys[1][6] = BitString("1000100101000010010")
generatorVectorsLfsrKeys[1][7] = BitString("0111100111100110001")

#00000100.bin
#generatorVectorsLfsrKeys for generatorvector[2]
generatorVectorsLfsrKeys[2][0] = BitString("1101000101101011011")
generatorVectorsLfsrKeys[2][1] = BitString("1000000101101001101")
generatorVectorsLfsrKeys[2][2] = BitString("1100000001101111001")
generatorVectorsLfsrKeys[2][3] = BitString("0110000111001011101")
generatorVectorsLfsrKeys[2][4] = BitString("0100110101101111011")
generatorVectorsLfsrKeys[2][5] = BitString("0110011111111010100")
generatorVectorsLfsrKeys[2][6] = BitString("0100010111101110000")
generatorVectorsLfsrKeys[2][7] = BitString("0001111001110101101")

#00000200.bin
#generatorVectorsLfsrKeys for generatorvector[3]
generatorVectorsLfsrKeys[3][0] = BitString("0100100110001001010")
generatorVectorsLfsrKeys[3][1] = BitString("1111111011110110001")
generatorVectorsLfsrKeys[3][2] = BitString("0101010000000010111")
generatorVectorsLfsrKeys[3][3] = BitString("0010011010110010100")
generatorVectorsLfsrKeys[3][4] = BitString("0010101100110001010")
generatorVectorsLfsrKeys[3][5] = BitString("1100001100010110000")
generatorVectorsLfsrKeys[3][6] = BitString("1101010111001011111")
generatorVectorsLfsrKeys[3][7] = BitString("0100010000001100000")


#lfsr keys for the overlappingstreams
overlappingStreamsLfsrKeys = [[BitString("")]*12 for i in range(2)]
#1404004000.bin
overlappingStreamsLfsrKeys[0][0]  = BitString("0000000000000000000") #padding
overlappingStreamsLfsrKeys[0][1]  = BitString("0001000000000000010")
overlappingStreamsLfsrKeys[0][2]  = BitString("1110000011000011000")
overlappingStreamsLfsrKeys[0][3]  = BitString("0000011100000000000")
overlappingStreamsLfsrKeys[0][4]  = BitString("0000000000000000001")
overlappingStreamsLfsrKeys[0][5]  = BitString("0000010000000000001")
overlappingStreamsLfsrKeys[0][6]  = BitString("0010010000000110001")
overlappingStreamsLfsrKeys[0][7]  = BitString("0010010010010011001")
overlappingStreamsLfsrKeys[0][8]  = BitString("0010110011111010011")
overlappingStreamsLfsrKeys[0][9]  = BitString("0110110011111010111")
overlappingStreamsLfsrKeys[0][10] = BitString("0011110011111010001")
overlappingStreamsLfsrKeys[0][11] = BitString("1000110000111001111")

#2808008000.bin
overlappingStreamsLfsrKeys[1][0]  = BitString("0000000000000000000") #padding
overlappingStreamsLfsrKeys[1][1]  = BitString("0101000100001000010")
overlappingStreamsLfsrKeys[1][2]  = BitString("0010000000001000000")
overlappingStreamsLfsrKeys[1][3]  = BitString("1000000000010000000")
overlappingStreamsLfsrKeys[1][4]  = BitString("0001000000000010010")
overlappingStreamsLfsrKeys[1][5]  = BitString("0001000100000110010")
overlappingStreamsLfsrKeys[1][6]  = BitString("0001000101100111010")
overlappingStreamsLfsrKeys[1][7]  = BitString("1001101101100111000")
overlappingStreamsLfsrKeys[1][8]  = BitString("1001110101010110000")
overlappingStreamsLfsrKeys[1][9]  = BitString("1001000111010111010")
overlappingStreamsLfsrKeys[1][10] = BitString("1100110001011110010")
overlappingStreamsLfsrKeys[1][11] = BitString("1011000111011111010")


#show that we only require 1026 bits
numberOfBitsRequired=0

#bits required for generator vectors
for i in range(0,4):
	for j in range(0,8):
		numberOfBitsRequired += len(generatorVectorsLfsrKeys[i][j])

#bits required for generator vectors
for i in range(0,2):
	for j in range(1,12): # start at index 1 as to exclude the padding bits.
		numberOfBitsRequired += len(overlappingStreamsLfsrKeys[i][j])

print("Total number of bits required: %d" % (numberOfBitsRequired))





#generate generator vectors
generatorVectors = [Block()]*4
generatorVectors[0] = produceKeyblocks(generatorVectorsLfsrKeys[0])
generatorVectors[1] = produceKeyblocks(generatorVectorsLfsrKeys[1])
generatorVectors[2] = produceKeyblocks(generatorVectorsLfsrKeys[2])	
generatorVectors[3] = produceKeyblocks(generatorVectorsLfsrKeys[3])

#write generator vector to filesystem
open("output/0generatorvectorsandoverlappingstreams/generatorvectors/00000040.bin", "wb").write(generatorVectors[0].bytesdata)
open("output/0generatorvectorsandoverlappingstreams/generatorvectors/00000080.bin", "wb").write(generatorVectors[1].bytesdata)
open("output/0generatorvectorsandoverlappingstreams/generatorvectors/00000100.bin", "wb").write(generatorVectors[2].bytesdata)
open("output/0generatorvectorsandoverlappingstreams/generatorvectors/00000200.bin", "wb").write(generatorVectors[3].bytesdata)

print("generated all generator vectors")







#generate overlapping streams
overlappingStreams = [Block()]*2
overlappingStreams[0] = produceKeyblocks(overlappingStreamsLfsrKeys[0])
overlappingStreams[1] = produceKeyblocks(overlappingStreamsLfsrKeys[1])

open("output/0generatorvectorsandoverlappingstreams/overlappingstreams/1404004000.bin", "wb").write(overlappingStreams[0].bytesdata)
open("output/0generatorvectorsandoverlappingstreams/overlappingstreams/2808008000.bin", "wb").write(overlappingStreams[1].bytesdata)


print("generated two overlapping streams")




#load two of the overlapping streams, generate the other two
# load 1404004000.bin and 2808008000.bin, to generate 410100100010000.bin and 820200200020000.bin, respectively.
overlappingstream1404004000 = open("output/0generatorvectorsandoverlappingstreams/overlappingstreams/1404004000.bin", "rb")
overlappingstream2808008000 = open("output/0generatorvectorsandoverlappingstreams/overlappingstreams/2808008000.bin", "rb")

#{1}={0x1, 0x40, 0x400, 0x4000}=overlappingstream1404004000 --> {4}={0x4, 0x10, 0x100, 0x1000, 0x10000}
#{2}={0x2, 0x80, 0x800, 0x8000}=overlappingstream2808008000 --> {8}={0x8, 0x20, 0x200, 0x2000, 0x20000}
overlappingstream410100100010000 = open("output/0generatorvectorsandoverlappingstreams/overlappingstreams/410100100010000.bin", "wb")
overlappingstream820200200020000 = open("output/0generatorvectorsandoverlappingstreams/overlappingstreams/820200200020000.bin", "wb")

generateOtherOverlappingstreams(overlappingstream1404004000, overlappingstream410100100010000)
generateOtherOverlappingstreams(overlappingstream2808008000, overlappingstream820200200020000)
print("generated other two overlapping streams")



print("end")