#!/usr/bin/env python3
#python cache simulator 

import sys 
import math 
from Cache import Cache

sys.argv.pop(0)

usage = "python sim.py -f trace_file -s size_in_KB -b block_size -a associativity -r replacment_policy"


def get_policy_full(policy):
    if policy == 'RR':
        return 'Round Robin'
    elif policy == 'RND':
        return 'Random'
    elif policy == 'LRU':
        return 'Least Recently Used'
    else:
        return policy

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
print(f'Trace File: {filename}')
print(f'Cache Size: {cacheSize}')
print(f'Block Size: {blockSize}')
print(f'Associativity: {associativity}')
print(f'R-Policy: {policy}\n')
print("Cache Simulator - CS 3853 Spring 2020 - Team 15\n")
print(f'Trace File:                     {filename}\n')
print("****** Cache Input Parameters ******\n")
print(f'Cache Size:                     {cacheSize} KB')
print(f'Block Size:                     {blockSize} bytes')
print(f'Associativity:                  {associativity}')
print(f'Replacement Policy:             {get_policy_full(policy)}\n')
cache = Cache(size=cacheSize, associativity=associativity, block_size=blockSize, alg=policy)

print(cache)

#lines = f.readlines()
stopPoint = 0
# print("\nFirst 20 addresses and lengths\n--------------------------------------")
#for i in stopPoint:
cache_access = 0
instr_count = 0
non_instr = 0
for lines in f:
    # if stopPoint > 209:
    #     break
    cLine = lines.split()
    
    if not lines.strip():
        ...
    elif cLine[0] == 'EIP':
        addr = int(cLine[2], 16)
        num_bytes = cLine[1].strip(":()")
        # print(f"{hex(addr)}: ({num_bytes})")

        cache.data_access(addr, num_bytes, 2)
        cache_access += 1
        instr_count += 1
        
    else :
        # one or both or neither can be zero
        dest = int(cLine[cLine.index("dstM:") + 1], 16)
        src = int(cLine[cLine.index("srcM:") + 1], 16)
        num_bytes = 4

        if dest:
            # print(f"Destination: {hex(dest)} bytes: 4")
            cache.data_access(dest, num_bytes, 1)
            non_instr += 1
        if src:
            # print(f"Source: {hex(src)} bytes: 4")
            cache.data_access(src, num_bytes, 1)
            non_instr += 1

    # print(cache.lru_col)

        #if dest and src:
            #print(f'dest: {hex(dest)}\tsrc: {hex(src)}')
        # if int(dest) != 0 and int(src) != 0:
        #     print(f'dest: {dest} \t src: {src}')

    stopPoint += 1


print("\n***** CACHE SIMULATION RESULTS *****\n")
print(cache.results())

print("\n***** CACHE HIT & MISS RATE: *****\n")
print(cache.cpi_rate())


print(cache.total_cycles)
print(non_instr)
# print(f"Sanity check: {cache_access}")
