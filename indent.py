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

"""

import os
import sys

INDENT = 6

# Set up defaults:
indent = INDENT
args = sys.argv
arglen = len(args)
infile = args[1]
root, fname = os.path.split(infile)
dest_file = os.path.join(root, "new_{}".format(fname))

# Collect options:
if arglen > 2:
    if args[2].isdecimal():
        indent = int(args[2])
    else:
        dest_file = args[2]
    if arglen > 3:
        dest_file = args[3]
print(f"Destination set to '{dest_file}'")
print(f"source: {infile}")
print(f"destin: {dest_file}")
print(f"indent: {indent}")

if infile == dest_file:
    with open(infile, 'r') as source:
        text = source.read()
    with open(dest_file, 'w') as dest:
        for line in text.split('\n'):
            dest.write(' '*indent + line + '\n')
else:
    with open(infile, 'r') as source:
        with open(dest_file, 'w') as dest:
            for line in source:
                dest.write(' '*indent + line)

