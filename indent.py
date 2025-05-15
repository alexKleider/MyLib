#!/usr/bin/env python3

# File: indent.py


"""
Accepts a text file and indents each line (to a
default of 6 spaces.)
First parameter must be a file name.
Optional second parameter can be
    an integer to replace the default INDENT=6
        If an integer: then a third parameter can specify an
        output file.
    OR the output file's name.
If an output file is not specified, output will go
to "new_<1stParam>".

Usage: $ ./indent.py infile [spaces2indent] outfile
"""

import os
import sys

INDENT = 6

# Set up defaults:
outfile = None
indent = 0
args = sys.argv
arglen = len(args)
print(f"{arglen=}")
if not arglen > 1:
    print("Usage:  indent.py infile [spaces2indent] [outfile]")
    print("At the very least, an input file must be specified!")
    sys.exit()
infile = args[1]
if arglen >2:
    print("3 or more args")
    try:
        indent = int(args[2])
    except ValueError:
        outfile = args[2]
if arglen == 4:
    outfile = args[3]

if not outfile:
        root, fname = os.path.split(infile)
        outfile = os.path.join(root, "new_{}".format(fname))
if not indent:
    indent = INDENT

print(f"source: {infile}")
print(f"indent: {indent}")
print(f"Destination set to '{outfile}'")

if infile == outfile:
    with open(infile, 'r') as source:
        text = source.read()
    with open(outfile, 'w') as dest:
        for line in text.split('\n'):
            dest.write(' '*indent + line + '\n')
else:
    with open(infile, 'r') as source:
        with open(outfile, 'w') as dest:
            for line in source:
                dest.write(' '*indent + line)

