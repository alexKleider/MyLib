#!/usr/bin/env python3

# File: ~/Git/Lib/letters.py

"""
To provide myself with ability to print mailing and return addresses
on a letter so they'll show up in the envelope windows.
Data is kept out of the repository in ../Data (i.e. my.csv)
but from time to time I'll tar them and encrypt the tar file and
include that with the repo so that the data is also backed up but kept
confidential.

Usage:
  ./letters.py [-O ]  -? | --help | --version
  ./letters.py --which <letter>  [-O -d -p <printer> -i <infile> -e <error_file> -j <json_file> --dir <mail_dir> --mta <mta> --to <to> --cc <cc> --bcc <bcc> ATTACHMENTS...]
  ./letters.py display [-d -o outfile] -j <json>
  ./letters.py send [-d] -j <json>

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
  -o <outfile>  File for readable version of emails. [default: 2check]
  -O  Show Options/commands/arguments.  Used for debugging.
  -p <printer>  Deals with printer variablility; ensures correct
        alignment of text when printing letters. [default: X6505_e9]
  --which <letter>  Which letter to prepare.

Commands:
  send: Send out emails.
  dislpay: 
"""

import os
import sys
import docopt
from code import content, mail, globals

args = docopt.docopt(__doc__, version=globals.VERSION)


def main():
    gbls = globals.Gbls(args)  # create an instance
    print(repr(gbls.d['--which']))
    gbls.which = content.content_types[gbls.d['--which']]
    if gbls.d['send']:    ## send CMD
        mail.send_emails(gbls)
    elif gbls.d['display']:    ## send CMD
        with open(gbls.d['-o'], 'w') as stream:
            stream.write( mail.display_emails( gbls.d['-j']))
        print("Human readable version of emails sent to {}"
                .format(gbls.d['-o']))
    elif not (gbls.d['--which'] 
             and gbls.d['--which'] in content.content_keys):
        print("Invalid or missing '--which' parameter.")
    else:                  ## prepare mailing
        print("Preparing letter/email(s): content_type= {}"
                .format(gbls.d['--which']))
        mail.generate_mailing(gbls)


if __name__ == "__main__":
    main()
else:  # disable printing...
    def print(*args, **kwargs):
        pass

