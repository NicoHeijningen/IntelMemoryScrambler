#!/usr/bin/python3
import os


for root, dirs, files in os.walk("output"):
	for file in files:
		#print(os.path.join(root,file))
		os.remove(os.path.join(root,file))
		
print("end")