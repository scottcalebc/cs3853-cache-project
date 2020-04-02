#!/usr/bin/env python3
#python cache simulator 

import sys 
import math 
from Cache import Cache

sys.argv.pop(0)

usage = "python sim.py -f trace_file -s size_in_KB -b block_size -a associativity -r replacment_policy"


def get_param_switch(switch):
    f = sys.argv.index(switch)
    sys.argv.pop(f)
    return sys.argv.pop(f)

if len(sys.argv) < 10:
    print(f'Invalid Parameters:  {usage}')
    exit(1)


try:
    filename = get_param_switch("-f")
    cacheSize = int(get_param_switch("-s"))
    blockSize = int(get_param_switch("-b"))
    associativity = int(get_param_switch("-a"))
    policy = get_param_switch("-r")

    if sys.argv:
        print(f'leftover Parameters:  {usage}')
        exit(1)
except Exception:
    print(f'Unable to convert Parameters:  {usage}')
    exit(1)


f = open(filename, 'r')
print("Cache Simulator CS 3853 Spring 2020\n")
print(f'Trace File:                     {filename}\n')
print("****** Cache Input Parameters ******\n")
print(f'Cache Size:                     {cacheSize}')
print(f'Block Size:                     {blockSize}')
print(f'Associativity:                  {associativity}')
print(f'Replacement Policy:             {policy}\n')
print("***** Calculated Values *****\n")

cache = Cache(size=cacheSize, associativity=associativity, block_size=blockSize, alg=policy)

print(cache)

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
