#!/usr/bin/env python3

# File: code/globals.py

import os


def set_file_name(root, name):
    return os.path.join(root,name)

VERSION='0.0.0'
N_FIELDS=10
DATA_DIR = '/home/alex/Git/Data'
DEFAULT_CSV_FILE = set_file_name(DATA_DIR, 'my.csv')
DEFAULT_ERROR_FILE = set_file_name(DATA_DIR, 'errors.txt')
DEFAULT_JSON_FILE = set_file_name(DATA_DIR, 'emails.json')
DEFAULT_MAIL_DIR = set_file_name(DATA_DIR, 'MailDir')
DEFAULT_MTA = 'easy'
DEFAULT_RECIPIENT = 'all'  # everyone in db will recieve letter/email
DEFAULT_PRINTER =  'X6505_e1'


class Gbls(object):

    n_instances = 0

    @classmethod
    def inc_n_instances(cls):
        cls.n_instances += 1


    def __init__(self, args):
        """
        Many attributes are assigned by other code: see
        code/rec.py traverse_records docstring.
        """
        if self.n_instances > 0:
            raise NotImplementedError("Only one instance allowed.")
        self.inc_n_instances()
        self.d = args
        if not self.d['--dir']:
            self.d['--dir'] = DEFAULT_MAIL_DIR  # letters are here
        if not self.d['-e']:
            self.d['-e'] = DEFAULT_ERROR_FILE
        if not self.d['-i']:
            self.d['-i'] = DEFAULT_CSV_FILE
        if not self.d['-j']:
            self.d['-j'] = DEFAULT_JSON_FILE   # emails are here
        if not self.d['--mta']:
            self.d['--mta'] = DEFAULT_MTA
        if not self.d['--to']:
            self.d['--to'] = DEFAULT_RECIPIENT
        if not self.d['-p']:
            self.d['-p'] = DEFAULT_PRINTER

        if self.d['-d']:
            for key, val in self.d.items():
                print("{}: {}".format(key, val))

