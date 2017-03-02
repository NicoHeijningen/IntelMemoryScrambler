#!/usr/bin/python3
import os
from Bauer.Block import Block


#verify the hypothesis that PRBSes combinations of the SCRMSEED keyblock and the generator vectors


SCRMSEEDToStart = 0	
numberOfPRBSsToGenerate = 100
outdir = "output/2SCRMSEEDkeyblocks/"
debugLevel = 10





# generates PRBS based on the SCMSEED keyblock and generator vectors
def generatePRBS(SCMRSEEDKeyblock, generatorVectors, debugLevel):
	generatedPRBS = Block()
	addresscounter = 0
	while addresscounter < 0x400:
		if(debugLevel > 1000):
				print("addresscounter %d, or 0x%08X" % (addresscounter, addresscounter))

		temp = SCMRSEEDKeyblock #always add the SCMSEED keyblock
		
		
		if((addresscounter & 0x200) >> 9): 
			temp = temp ^ generatorVectors[3] # 0x200 bit is set, so add its generator vector
			if(debugLevel > 1000):
				print("(addresscounter & 0x200) >> 9")

		if((addresscounter & 0x100) >> 8):
			temp = temp ^ generatorVectors[2] # 0x100 bit is set, so add its generator vector
			if(debugLevel > 1000):
				print("(addresscounter & 0x100) >> 8")

		if((addresscounter & 0x80) >> 7):
			temp = temp ^ generatorVectors[1] # 0x80 bit is set, so add its generator vector
			if(debugLevel > 1000):
				print("(addresscounter & 0x80) >> 7")

		if((addresscounter & 0x40) >> 6):
			temp = temp ^ generatorVectors[0] # 0x40 bit is set, so add its generator vector
			if(debugLevel > 1000):
				print("(addresscounter & 0x40) >> 6")


		generatedPRBS = generatedPRBS + temp
		
		#print debug after temp has been added
		if(debugLevel > 800):
			temp = temp.partition(1)


			for i in range(len(temp)):
				if  (i%16)==0:
					print("\n", end="")
				else:
					if((i%8)==0):
						print(" ", end="")


				print("%s " % (temp[i].tosmallhexstr()), end="")
			print("\n")


		addresscounter = addresscounter + 0x40
		
	return generatedPRBS

	

SCRMSEED = SCRMSEEDToStart
while SCRMSEED < numberOfPRBSsToGenerate:

	generatorVectors = [Block()]*4
	generatorVectors[0] = Block(open("output/0generatorvectorsandoverlappingstreams/generatorvectors/00000040.bin", "rb").read(64))
	generatorVectors[1] = Block(open("output/0generatorvectorsandoverlappingstreams/generatorvectors/00000080.bin", "rb").read(64)) 
	generatorVectors[2] = Block(open("output/0generatorvectorsandoverlappingstreams/generatorvectors/00000100.bin", "rb").read(64)) 
	generatorVectors[3] = Block(open("output/0generatorvectorsandoverlappingstreams/generatorvectors/00000200.bin", "rb").read(64)) 

	SCMRSEEDKeyblock = open("output/2SCRMSEEDkeyblocks/%08x.bin" % (SCRMSEED), "rb")
	
	generatedPRBS = generatePRBS(Block(SCMRSEEDKeyblock.read(64)), generatorVectors, debugLevel)
	
	if(debugLevel > 10):
		print("generated PRBS for SCRMSEED=0x%08x" % (SCRMSEED))
	
	PRBS = open("output/3PRBSs/%08x.bin" % (SCRMSEED), "wb")
	
	PRBS.write(generatedPRBS.bytesdata)
	
	SCRMSEED = SCRMSEED + 1 


print("end")




