#!/usr/bin/env python3

# File: pager.py

"""
Usage:
    ./pager.py textfile [nlines]

Requires one mandatory parameter: the name of a text file
and has one optional parameter: nlines (which defaults to NLINES.)
Inserts a form feed character into blank lines
such that no page will be > nlines long (where ever possible.)
Output is directed to "new-" + textfile.
"""

import sys

NLINES = 62

args = sys.argv
if len(args) < 2:
    print("Must provide the name of a text file.")
    sys.exit()
else: 
    fname = args[1]
if len(args) == 3:
    nlines = int(args[2])
else:
    nlines = NLINES

outfname = 'new-'+fname

with open(fname, 'r') as infile:
    lines = [line.rstrip() for line in infile]
blocks = []  # list of lists of lines
current_block = []  # current list of lines
for line in lines:
    line = line.rstrip()
    if line:  # continue adding to current block
        current_block.append(line)
    else:  # encountered a blank line (end of block)
        appendee = [line for line in current_block]
        if appendee:
            blocks.append(appendee)
            current_block = []

ret = []   # to be returned
page = []
extranewlines = 0
for block in [b for b in blocks if b]:
    npage = len(page)
    nblock = len(block)
    if (npage + nblock + extranewlines) < nlines:
        page.extend(block)
    else:
        extranewlines = 0
        if ret:
            ret[-1] = ret[-1].rstrip() + '\f'
        ret.extend(page)
        page = [item for item in block]
    page[-1] = page[-1].rstrip() + '\n'
    extranewlines += 1
if page:
    ret[-1] = ret[-1].rstrip() + '\f'
    ret.extend(page)

if ret and ret[0] == '\f':
    ret.pop(0)

with open(outfname, 'w') as outfile:
    outfile.write('\n'.join(ret))



