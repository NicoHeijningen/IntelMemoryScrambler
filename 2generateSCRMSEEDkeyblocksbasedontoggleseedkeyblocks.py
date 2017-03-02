#!/usr/bin/python3
import os
from Bauer.Block import Block


#verify the hypothesis that SCRMSEED keyblocks are linear combinations of the toggle vectors


SCRMSEEDToStart = 0	
numberOfSCMRSEEDKeyblocksToGenerate = 100
outdir = "output/2SCRMSEEDkeyblocks/"
debugLevel = 10

def generateSCMRSEEDKeyblock(SCRMSEED):
	if(debugLevel > 500):
		print("generateSCMRSEEDKeyblock(SCRMSEED=0x%08x)" % (SCRMSEED))
		
	generatedSCMRSEEDKeyblock = Block().setfromhex("00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
	toggleCounter = 1
	toggleKeyblockFolder = "output/1toggleseeds/"
	while SCRMSEED > 0:
		if(debugLevel > 1000):
				print("SCRMSEED %d, or 0x%08X" % (SCRMSEED, SCRMSEED))
		
		if(SCRMSEED & 1)==1: #if lowest bit of SCRMSEED is set, xor in the constant vector of toggleCounter
			fileName = "%s%08x.bin" % (toggleKeyblockFolder, toggleCounter)
			
			if(debugLevel > 100):
				print("filename being XORed in: %s" % (fileName))
			f = open(fileName, "rb")
			generatedSCMRSEEDKeyblock = generatedSCMRSEEDKeyblock ^ Block(f.read(64))
			
		SCRMSEED = SCRMSEED >> 1
		toggleCounter = toggleCounter << 1
		
	return generatedSCMRSEEDKeyblock



SCRMSEED = SCRMSEEDToStart
while SCRMSEED < numberOfSCMRSEEDKeyblocksToGenerate:


	generatedSCMRSEEDKeyblock = generateSCMRSEEDKeyblock(SCRMSEED)

	SCMSEEDKeyblock = open(("%s%08x.bin" % (outdir, SCRMSEED)), "wb")
	SCMSEEDKeyblock.write(generatedSCMRSEEDKeyblock.bytesdata)
	
	if(debugLevel > 10):
		print("generated SCRMSEED keyblock for SCRMSEED=0x%08x" % (SCRMSEED))
				
	SCRMSEED = SCRMSEED + 1 



print("end")


