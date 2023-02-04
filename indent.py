#!/usr/bin/env python3

# File: indent.py


"""
Accepts a text file and indents each line (to a default of 6 spaces.)
First parameter must be a file name.
Optional second parameter can be the output file's name.
If 2nd param is not specified, output will go to "new_<1stParam>".
"""

import os
import sys

INDENT = 6


args = sys.argv
arglen = len(args)
infile = args[1]
if arglen > 2:
    dest_file = args[2]
else:
    root, fname = os.path.split(infile)
    dest_file = os.path.join(root, "new_{}".format(fname))
with open(infile, 'r') as source:
    with open(dest_file, 'w') as dest:
        for line in source:
            dest.write(' '*INDENT + line)

