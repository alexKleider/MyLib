#!/usr/bin/env python3

# file: limit_line_length.py

"""
Accepts a text file and tries to shorten lines to MAX characters.
First parameter must be a file name.
If a second parameter is provided:
    If it is an integer:
        max line length parameter will be over ridden to this
        value and a third parameter will be allowed to specify the
        file name.
If 2nd param is not specified, output will go to "new_<1stParam>"
    and the default line length (MAX) is used.
Provides and serves as a wrapper around:
    limit_line_length(infile, outfile, maxlen)
"""
usage = """Usage:
    $ limit_line_length.py <in-file> [<out_file]
    $ limit_line_length.py <in-file> <max_line_length> [<out_file]
# Note: in the latter case 2nd param must be an positive integer.
"""

import os
import sys

MAX = 70


def split_on_space_closest_to_max_len(line, max_len):
    """
    Returns a tuple of two (possibly empty) strings.
    If the line is <= <max_len>: it is returned as t[0] & t[1] is ''.
    If indented beyond <max_len> t[0] is '' & t[1] is line[max_len:]
    If there are no spaces then t[0] is <line> and t[1] is ''.
    If the first space is beyond <max_len>: t[0] is up to the space
    and t[1] what was after the space.
    Otherwise the line is broken at a space such that t[0] is the
    longest it can be up to max_len and t[1] is what comes after the space.
    Trailing spaces are stripped.
    """
    line = line.rstrip()
    line_length = len(line)
    if line_length <= max_len:  # simplest scenario
        return (line, '')       # empty lines included
    original_line = line
    unindented_line = line.lstrip()
    n_leading_spaces = line_length - len(unindented_line)
    if n_leading_spaces > max_len:  # big indentation!!!
        return ('', line[max_len:])
    indentation = unindented_line[:n_leading_spaces]
    max_len -= n_leading_spaces
    i_last_space = unindented_line.rfind(' ')
    if i_last_space == -1:  # no spaces on which to split
        return (line, '')
    i_space = unindented_line.find(' ')
    if i_space > max_len:
        return (indentation + unindented_line[:i_space],
                unindented_line[i_space+1:])
    while True:
        next_space = unindented_line.find(' ', i_space+1)
        if (next_space == -1) or (next_space > max_len):
            break
        i_space =next_space
    return (indentation + unindented_line[:i_space],
            unindented_line[i_space +1:])

def limit_line_length(infile, outfile, max_line_len):
    with open(infile, 'r') as source:
        with open(outfile, 'w') as dest:
            for line in source:
                while line:
                    line2write, line = split_on_space_closest_to_max_len(
                            line, max_line_len)
                    dest.write(line2write + '\n')


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print("Must provide at least one parameter!")
        print(usage)
        sys.exit()
    infile = args[0]
    maxlen = MAX
    outfile = ''
    if len(args) > 1:
        if args[1].isdecimal():
            maxlen = int(args[1])
            print(f"Setting maxlen to {maxlen}")
        else:
            outfile = args[1]
            print(f"Setting outfile to {outfile}")
            if len(args) > 2:
                print(f"Unused 3rd parameter: {args[2]}")
        if len(args) > 2 and not outfile:
            outfile = args[2]
            print(f"Set outfile to third param: {outfile}")
    if not outfile:
        root, fname = os.path.split(infile)
        outfile = os.path.join(root, "new_{}".format(fname))
        print(f"outfile set to default: {outfile}")
    print(f"Params are: {infile}, {outfile}, {maxlen}")
    limit_line_length(infile, outfile, maxlen)

