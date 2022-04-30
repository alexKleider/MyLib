#!/usr/bin/env python3

# File: code/data_cks.py

"""
Code to check on data integrity.

Usage:
    ./code/data_cks.py csv_file [new_sorted]
"""

import os
import sys
import csv
sys.path.insert(0, os.path.split(sys.path[0])[0])
import letters

FILE = '../Data/temp.csv'
FILE = '../Data/my.csv'
FILE_OUT = '../Data/my_new.csv'

if len(sys.argv) > 1:
    new_sorted = True
else:
    new_sorted = False


def comp_key(rec):
    return("{last} {first} {company}".format(**rec))


def ck_data(csv_file, new_sorted=False):
    """
    """
    collector = []
    with open(csv_file, newline='') as stream:
        reader = csv.DictReader(stream)
        fieldnames = reader.fieldnames
        nfieldnames = len(fieldnames)
        print("nfieldnames=" + str(nfieldnames))
        print(fieldnames)
        for rec in reader:
            collector.append(rec)
    if new_sorted:
        writer = csv.DictWriter(
                open(FILE_OUT, 'w', newline=''),
                fieldnames=fieldnames)
        writer.writeheader()
    for rec in sorted(collector,key=comp_key):
        if nfieldnames != len(rec.keys()):
            print("####### Next record is malformed:  ####### ")
        rep = """{first} {last}, {company} [{phone} {email}]
{address}, {town}, {state} {postal_code} {country}"""
        if new_sorted:
            writer.writerow(rec)
        else:
            response = input(rep.format(**rec))
            if not response or ord(response[0]) < 32: break

if __name__ == "__main__":
    ck_data(FILE, new_sorted)
