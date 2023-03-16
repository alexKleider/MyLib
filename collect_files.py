#!/usr/bin/env python3

# File: ~/Git/collect_files.py

"""
Usage:
    ./collect_files.py [directory[ exclude_file]]
    
"""

import os
import sys

# set defaults:
path = os.path.expanduser('~/Git/Sql/Sql')
exclude = os.path.expanduser('~/Git/Sql/Sql/exclude.txt')
outfile =  os.path.expanduser('~/Git/Sql/collector.txt')

if len(sys.argv) > 1: path = os.path.expanduser(sys.argv[1])
if len(sys.argv) > 2: exclude = os.path.expanduser(sys.argv[2])

forbidden_files = []
with open(exclude, 'r') as infile:
    for line in infile:
        line = line.strip()
        if line and line[0] != '#':
            forbidden_files.append(line)

collector = []
for f in os.listdir(path):
    if f in forbidden_files: continue
    with open(os.path.join(path,f), 'r') as infile:
        for line in infile:
            collector.append(line.rstrip())
    collector.append('')

with open(outfile, 'w') as outf:
    for line in collector: outf.write(line+'\n')


