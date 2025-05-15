#!/usr/bin/env python3

# File: builtins.py

from code import helpers

built_ins = dir(__builtins__)
error_types = [built_in for built_in in built_ins if "Error" in built_in]

for line in helpers.tabulate(
#                            built_ins,
                             error_types,
                             max_width=150,
                             separator = " "):
    print(line)


