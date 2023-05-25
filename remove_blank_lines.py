#!/usr/bin/env python3

# File: remove_blank_lines.py

"""
Requires a command line argument: the name of a file
to strip of blank (or white space only) lines.
"""

def remove_blank_lines(text_file_name):
    ret = []
    with open(text_file_name, 'r') as instream:
        for line in instream:
            line = line.strip()
            if line:
                ret.append(line)
    with open(text_file_name, 'w') as outstream:
        outstream.write('\n'.join(ret))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Need the name of a file as a second argument.")
    else:
        remove_blank_lines(sys.argv[1])

