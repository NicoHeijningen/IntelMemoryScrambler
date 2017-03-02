#!/usr/bin/python3
import os

#verify hypothesis that that the four overlappingstreams
#can generate all the toggle vectors

	

def generateToggleseedKeyblocks(infile, listOfToggleseedKeyblockToBeGenerated):
	outdir = "output/1toggleseeds/"

	infile.seek(0x20)
	outfile = open(("%s%08x.bin" % (outdir, listOfToggleseedKeyblockToBeGenerated.pop(0))), "wb")
	outfile.write(infile.read(64))


	if len(listOfToggleseedKeyblockToBeGenerated) == 4:
		infile.seek(0x0)
		outfile = open(("%s%08x.bin" % (outdir, listOfToggleseedKeyblockToBeGenerated.pop(0))), "wb")
		outfile.write(infile.read(64))


	infile.seek(0x8)
	outfile = open(("%s%08x.bin" % (outdir, listOfToggleseedKeyblockToBeGenerated.pop(0))), "wb")
	outfile.write(infile.read(64))   

	infile.seek(0x10)
	outfile = open(("%s%08x.bin" % (outdir, listOfToggleseedKeyblockToBeGenerated.pop(0))), "wb")
	outfile.write(infile.read(64))   

	infile.seek(0x18)
	outfile = open(("%s%08x.bin" % (outdir, listOfToggleseedKeyblockToBeGenerated.pop(0))), "wb")
	outfile.write(infile.read(64))   




overlappingstream1404004000 = open("output/0generatorvectorsandoverlappingstreams/overlappingstreams/1404004000.bin", "rb")
overlappingstream2808008000 = open("output/0generatorvectorsandoverlappingstreams/overlappingstreams/2808008000.bin", "rb")
overlappingstream410100100010000 = open("output/0generatorvectorsandoverlappingstreams/overlappingstreams/410100100010000.bin", "rb")
overlappingstream820200200020000 = open("output/0generatorvectorsandoverlappingstreams/overlappingstreams/820200200020000.bin", "rb")


generateToggleseedKeyblocks(overlappingstream1404004000, [0x1,0x40,0x400,0x4000]);
generateToggleseedKeyblocks(overlappingstream2808008000, [0x2,0x80,0x800,0x8000]);
generateToggleseedKeyblocks(overlappingstream410100100010000, [0x4,0x10,0x100,0x1000,0x10000]);
generateToggleseedKeyblocks(overlappingstream820200200020000, [0x8,0x20,0x200,0x2000,0x20000]);
print("generated all toggleseed keyblocks")


print("end")