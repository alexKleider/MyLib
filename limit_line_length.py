#!/usr/bin/env python3

# file: limit_line_length.py

"""
Accepts a text file and tries to shorten lines to MAX characters.
First parameter must be a file name.
Optional second parameter can be the output file's name.
If 2nd param is not specified, output will go to "new_<1stParam>".
"""

import sys

MAX = 70



def split_on_space_closest_to_max_len(line, max_len=MAX):
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
#   original_line = line[:]
    original_line = line
    unindented_line = line.lstrip()
    n_leading_spaces = line_length - len(unindented_line)
    if n_leading_spaces > max_len:  # big indentation!!!
        return ('', line[max_len:])
#   indentation = ' ' * n_leading_spaces
    indentation = unindented_line[:n_leading_spaces]
    max_len -= n_leading_spaces
    i_last_space = unindented_line.rfind(' ')
    if i_last_space == -1:  # no spaces on which to split
        return (line, '')
    i_space = unindented_line.find(' ')
#   if i_space == -1:
#       print('returning -1!')
    if i_space > max_len:
        return (indentation + unindented_line[:i_space],
                unindented_line[i_space+1:])
    while True:
        next_space = unindented_line.find(' ', i_space+1)
#       if next_space == -1:
#           print('Found no space within "{}"'
#                   .format(unindented_line))
#           for c in unindented_line:
#               print(ord(c), ' ', end='')
#           sys.exit()
#       else:
#           print("Found a space within '{}'"
#                   .format(unindented_line))
        if (next_space == -1) or (next_space > max_len):
            break
        i_space =next_space
    return (indentation + unindented_line[:i_space],
            unindented_line[i_space +1:])


args = sys.argv
arglen = len(args)
infile = args[1]
if arglen > 2: dest_file = args[2]
else: dest_file = "new_{}".format(infile)
with open(infile, 'r') as source:
    with open(dest_file, 'w') as dest:
        for line in source:
#           line = repr(line.rstrip())
#           print("line: '{}'".format(line))  # for debugging
            while line:
                line2write, line = split_on_space_closest_to_max_len(
                        line)
#               print("writing: '{}'".format(line2write))  # for debugging
#               print("remaining: '{}'".format(line))  # for debugging
                dest.write(line2write + '\n')



