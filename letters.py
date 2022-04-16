#!/usr/bin/env python3

# File: ~/Git/Lib/letters.py

"""
To provide myself with ability to print mailing and return addresses
on a letter so they'll show up in the envelope windows.
Data is kept out of the repository in ../Data (i.e. my.csv)

Usage:
  ./letters.py [-O ] [ -? | --help | --version]
  ./letters.py --which <letter>  [-O -d -p <printer> -i <infile> -e <error_file> -j <json_file> --dir <mail_dir> --mta <mta> --to <to> --cc <cc> --bcc <bcc> ATTACHMENTS...]
  ./letters.py send [-d -j <json>]

Options:
  -h --help  Print this docstring. Best piped through pager.
  -?  Print allowed commands and their options.
  --version  Print version.
  --to <to>  name of recipient: if not set, all who are in data base
  --cc <cc>   Comma separated listing of cc recipients
        sponsors. Implementation of this feature is still underway-
        implementation within the "--which" option vs the command
        line level.
  --bcc <bcc>   Comma separated listing of blind copy recipients
  -d  Debug mode
  --dir <mail_dir>   The directory (to be created) for storage of
         letters for subsequent batch printing. 
  -e <error_file>   Specify name of a file to which an
            error report can be written.
  -i <infile>  Specify file used as input.
  -j <json>  Specify a json formated file to contain emails.
  --mta <mta>  Specify mail transfer agent to use. Choices are:
                clubg     club's gmail account
                akg       my gmail account
                easy      my easydns account
  -O  Show Options/commands/arguments.  Used for debugging.
  -p <printer>  Deals with printer variablility; ensures correct
        alignment of text when printing letters.
  --which <letter>  Which letter to prepare.

Commands:
  send: Send out emails.
"""

import sys
import docopt
import code.helpers

VERSION='0.0.0'
DATA_DIR = '/home/alex/Git/Data'
SPECS_SOURCE = '/home/alex/Git/Data/specs.py'
SPECS = ''
DEFAULT_CSV_FILE = 'contacts.csv'
DEFAULT_ERROR_FILE = 'errors.txt'
DEFAULT_JSON_FILE = 'emails.json'
DEFAULT_MAIL_DIR = 'MailDir'
DEFAULT_MTA = 'easy'
DEFAULT_RECIPIENT = 'all'  # everyone in db will recieve letter/email
DEFAULT_PRINTER =  'X6505_e1'


class Gbls(object):

    n_instances = 0

    @classmethod
    def inc_n_instances(cls):
        cls.n_instances += 1


    def __init__(self):
        """
        Many attributes are assigned by other code: see
        code/rec.py traverse_records docstring.
        """
        if self.n_instances > 0:
            raise NotImplementedError("Only one instance allowed.")
        self.inc_n_instances()
        self.d = docopt.docopt(__doc__, version=VERSION)
        if not self.d['-i']:
            self.d['-i'] = DEFAULT_CSV_FILE
        if not self.d['-e']:
            self.d['-e'] = DEFAULT_ERROR_FILE
        if not self.d['-j']:
            self.d['-j'] = DEFAULT_JSON_FILE
        if not self.d['--dir']:
            self.d['--dir'] = DEFAULT_MAIL_DIR
        if not self.d['--mta']:
            self.d['--mta'] = DEFAULT_MTA
        if not self.d['--to']:
            self.d['--to'] = DEFAULT_RECIPIENT
        if not self.d['-p']:
            self.d['-p'] = DEFAULT_PRINTER
        if self.d['-d']:
            for key, val in self.d.items():
                print("{}: {}".format(key, val))


def send_emails(email_json_file):
    print("Sending emails...")
    print("...finished sending emails.")
    


def mailing_cmd():
    gbls = Gbls()
    if gbls.d['send']:
        send_emails(gbls.d['--dir'])
        sys.exit()
    print("Preparing letter(s): content_type= " +
            gbls.d['--which'])


def testing_func(record, gbls):
    """
    For mailings which require no special processing.
    Mailing is sent if the "test" lambda => True.
    Otherwise the record is ignored.
    """
    if gbls.which["test"](record):
        record["subject"] = gbls.which["subject"]
        record['extra'] = "Blah, Blah, Blah!"
        q_mailing(record, gbls)


if __name__ == "__main__":
    # main()
    mailing_cmd()
    print("content.py compiles OK")
else:  # disable printing...
    def print(*args, **kwargs):
        pass


