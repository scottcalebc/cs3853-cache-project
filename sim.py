#!/usr/bin/env python3
#python cache simulator 

import sys 
import math 
addrSize = 32
filename = sys.argv[2]
cacheSize = sys.argv[4]
blockSize = sys.argv[6]
associativity = int(sys.argv[8])
policy = sys.argv[10]
f = open(filename, 'r')
print("Cache Simulator CS 3853 Spring 2020")
print("Cmd Line:" , sys.argv[:])
print("Trace File:", filename)
print("Cache Size: ", cacheSize, "KB")
print("Block Size: ", blockSize, "bytes")
print("Associativity: ", associativity)
print("Policy: ", policy)
print("----- Calculated Values -----")
if(associativity == 1):
    #calculate the values for a fully associated cache 
    index = 0
    totalIndices = 1
    offset = math.log(float(blockSize), 2)
    tagSize = (int)(addrSize - offset)
    totalBlocks = (int(cacheSize) * 1024 )/int(blockSize)
    totalBlocksPower = math.log(float(totalBlocks), 2)
   #overhead = valid bits + tag bits + dirty bits 
    overhead = (totalBlocks*( 1 + tagSize)) / 8
    implementationMemory = int(cacheSize)*1024 + int(overhead)
    hitRate = 0 
else:
    # 32  = tag bits + index + offset 
    # tag bits =  32 - index - offset
    # offset == block size = n where 2^n
    offset = math.log(float(blockSize), 2) 
    associativityPower = math.log(float(associativity), 2)
    # index == cache size = n where 2^n (the plus 10 is for kb)
    index = (int)(math.log(float(cacheSize), 2) + 10 - associativityPower - offset)
    tagSize = (int)(addrSize - index - offset)
    totalBlocksPower = index + associativityPower
    totalBlocks = (int)(2 ** totalBlocksPower)
    totalIndices = (int)(totalBlocks / associativity)
    #overhead = valid bits + tag bits + dirty bits 
    overhead = (totalBlocks*( 1 + tagSize)) / 8
    implementationMemory = int(cacheSize)*1024 + int(overhead)
    hitRate = 0

print("offset:", offset)
print("Total # Blocks:", totalBlocks, "( 2 ^",totalBlocksPower,")")
print("Tag Size:", tagSize, "bits")
print("Index Size:", index,"bits, Total Indices:", totalIndices)
print("Overhead Memory Size:", overhead, "bytes")
print("Implementation Memory Size:", implementationMemory, "bytes")
print("----- Results -----")
print("Cache Hit Rate:", hitRate, "%")

lines = f.readlines()
stopPoint = range(0,60)
print("\nFirst 20 addresses and lengths\n--------------------------------------")
for i in stopPoint:
    cLine = lines[i].split()
    if not lines[i].strip():
        ...
    elif cLine[0] == 'EIP':
        print("0x" + cLine[2] + ":", cLine[1].strip(":"))
    else :
        ...
