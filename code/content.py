#!/usr/bin/env python3

# File: code/content.py

import os
import sys
from code import funcs, helpers

from_address_format = """{first} {last}
{address}
{town}, {state} {postal_code}
{country}"""

to_address_format = """{first} {last}
{company}
{address}
{town}, {state} {postal_code}
{country}"""

custom_lambdas = dict(
    QuattroSolar=(lambda record: True if 'Quattro Solar' in
                  record["company"] else False),
    MarinMechanical=(lambda record: True if 'Marin Mechanical'
                     in record["company"] else False),)


letter_bodies_docstring = """
Some of these 'bodies' are subject to the format method
and those must have {{double}} parens for the format fields
that must be subsequently filled in by the '..._funcs'.
"""

### !!!!!!!!!!!!!!! BODIES !!!!!!!!!!!!!!!!!!! ###
# # single braces are for fields populated by the content_type data.
# # double braces fields are populated by the record data.
letter_bodies = dict(

    request_address_change="""
The enclosed letter caused the Post Office much distress!

Please change my address to include a "PO Box 277" line
or expand the postal code to "94924-0277".

I believe either (or better still, both) would appease the USPS.

Also, I'm puzzled by the mailing since there was nothing therein
except blank pages.  Was there something that was supposed to come to
me but which got forgotten?
""",

    enclosure_only="""
Please find enclosed.
""",

    addresses_only="""
""",

    bill_payment="""
Please find enclosed payment.
""",

    for_testing="""
Blah, Blah-
more Blah blah

etc

First extra content is
{extra}

May have as many 'extra's as required as long as each one
has a corresponding entry in the record dict (typically arranged
by the custom function.
""",

)



### !!!!!!!!!!!!!!!!!!!! POSTSCRIPTS !!!!!!!!!!!!!!!!! ##
post_scripts = dict(

    forgive_duplicate="""This may be a duplication of an email
    already sent in which case please forgive.""",

    )


### !!!!!!!!!!!!!!!!!!!! AUTHORS !!!!!!!!!!!!!!!!! ##
authors_DOCSTRING = """   ## NOTE ##
A "Sender:" field, determined by the --mta is added to each email at
the time it is sent.  The value of the 'email' field is entered into
the 'From: ' header of the email. A "reply2" field is also available.
"""

authors = dict(  # from
    bc=dict(  # AK in British Columbia
        first="Alex",
        last="Kleider",
        address="3727 Cavin Rd.",
        town="Duncan",
        state="BC",
        postal_code="V9L 6T2",
        country="Canada",
        email_signature="\nSincerely,\nAlex Kleider",
        email="akleider@sonic.net",
        reply2="akleider@sonic.net",
        mail_signature="\nSincerely,\n\n\nAlex Kleider",
        ),
    ak=dict(  # AK in Bolinas
        first="Alex",
        last="Kleider",
        address="PO Box 277",
        town="Bolinas",
        state="CA",
        postal_code="94924",
        country="USA",
        email_signature="\nSincerely,\nAlex Kleider",
        email="akleider@sonic.net",
        reply2="akleider@sonic.net",
        mail_signature="\nSincerely,\n\n\nAlex Kleider",
        ),
    )


content_type_docstring = """
One of the following content_types is assigned to the 'which'
attribute of an instance of utils.Club for mailing purposes.

  Each item in the following dict specifies:
      subject: re line in letter_bodies, subject line in emails
      from: expect a value from the 'authors' dict
          each value is itself a dict specifying more info...
          names, address, signatures, reply to, ..
      body: text of the letter which may or may not have
          one or more 'extra' sections.
      post_scripts:  a list of optional postscripts
      funcs: a list of functions used on each record during
          the data gathering traversal of the membership csv.
      test: a (usually 'lambda') function that determines
          if the record is to be considered at all.
      e_and_or_p: possibilities are:
          'both' email and usps,
          'email' email only,
          'usps' mail only,
       or 'one_only' email if available, otherwise usps.
  One of the following becomes the 'which' attribute
  of a Membership instance.
"""

content_types = dict(  # which_letter   '--which'
    # ## If a 'salutation' key/value is provided for any of the
    # ## following, the value will be used as the salutation
    # ## instead of a 'Dear {first} {last},' line.
    # ## The first 4 listed values for each are used for first
    # ## stage formatting.
    for_testing={
        "subject": "This is a test.",
        "from": authors["ak"],
        "body": letter_bodies["for_testing"],
        "post_scripts": ('forgive_duplicate',),
        "funcs": [funcs.testing_func, ],
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    enclosure_only={
        "subject": "enclosure",
        "from": authors["ak"],
        "body": letter_bodies["enclosure_only"],
        "post_scripts": (),
        "funcs": [funcs.std_mailing_func,],
        "test": lambda record: record['phone']=='0',
        "e_and_or_p": "usps",
        },
    request_address_change={
        "subject": "request_address_change",
        "from": authors["ak"],
        "body": letter_bodies["request_address_change"],
        "post_scripts": (),
        "funcs": [funcs.std_mailing_func,],
        "test": lambda record: record['first']=='Kaiser',
        "e_and_or_p": "usps",
        },

    addresses_only={
        "subject": "",
        "from": authors["ak"],
        "body": letter_bodies["addresses_only"],
        "post_scripts": (),
        "funcs": [funcs.std_mailing_func,],
        "test": lambda record: True,
        "e_and_or_p": "usps",
        },

    bill_payment={
        "subject": "Payment of Invoice.",
        "from": authors["bc"],
        "body": letter_bodies["bill_payment"],
        "post_scripts": (),
        "funcs": [funcs.std_mailing_func, ],
        "test": lambda record: True,
        "e_and_or_p": "usps",
        },
)
content_keys = set(content_types.keys())

printers = dict(
    # tuples in the case of envelope windows.
    X6505_e1=dict(  # Smaller envelope.
        # e1: envelope with distances (in mm) from top to
        # top of top window       21
        # bottom of top window    43
        # top of lower window     59
        # bottom of lower window  84
        indent=7,
        top=4,  # blank lines at top  1 ..2
        frm=(4, 25),  # return window 3..6
        date=5,  # lines between windows 7..11
        to=(5, 30),  # recipient window 12..16
        re=3,  # lines below bottom window
        ),
    X6505_e2=dict(  # Larger envelope.
        indent=5,
        top=2,  # blank lines at top  1 ..2
        frm=(4, 25),  # return window 3..6
        date=5,  # lines between windows 7..11
        to=(5, 30),  # recipient window 12..16
        re=3,  # lines below bottom window
        ),
    HL2170=dict(  # large envelopes, Cavin Rd usb printer
        indent=3,
        top=1,  # blank lines at top
        frm=(5, 25),  # return window
        date=4,  # between windows
        to=(7, 29),  # recipient window
        re=4,  # below windows => fold
        ),
    loft=dict(
        indent=0,
        top=0,  # blank lines at top
        frm=(5, 25),  # return window
        date=4,  # between windows
        to=(7, 29),  # recipient window
        re=4,  # below windows => fold
        ),
    )
# ## ... end of printers (dict specifying printer being used.)



def get_postscripts(which_letter):
    """
    Returns a list of lines representing the post scripts
    """
    ret = []
    n = 0
    for post_script in content_types[which_letter]["post_scripts"]:
        ret.append("\n" + "P"*n + "PS " + post_script)
        n += 1
    return ret


def prepare_letter_template(which_letter, lpr):
    """
    Prepares the template for a letter.
    <which_letter>: one of the <content_types> and
    <printer>: one of the keys to the <printers> dict
    Returns a 'letter' /w formatting fields.
    """
    lpr = printers[lpr]
    ret = [""] * lpr["top"]  # add blank lines at top
    # return address:
    ret_addr = from_address_format.format(
            **content_types[which_letter]["from"])
    ret.append(helpers.expand(ret_addr, lpr['frm'][0]))
    # format string for date:
    ret.append(helpers.expand(
            (helpers.get_datestamp()), lpr['date']))
    # format string for recipient adress:
    ret.append(helpers.expand(to_address_format, lpr['to'][0]))
    if which_letter == "addresses_only":
        return '\n'.join(ret)
    # subject/Re: line
    ret.append(helpers.expand(
        "Re: {}".format(content_types[which_letter]["subject"]),
        lpr['re']))
    # format string for salutation:
    try:
        ret.append(content_types[which_letter]["salutation"] + "\n")
    except KeyError:
        ret.append("Dear {first} {last},\n")
    # body of letter (with or without {extra}(s))
    ret.append(content_types[which_letter]["body"])
    # signarue:
    ret.append(content_types[which_letter]["from"]["mail_signature"])
    # post script:
    ret.extend(get_postscripts(which_letter))
    return '\n'.join(ret)


def prepare_email_template(which_letter):
    """
    Prepares the template for an email.
    Used by utils.prepare_mailing_cmd,
    Format fields are subsequently filled by **record.
    """
    ret = ["Dear {first} {last},"]
    ret.append(content_types[which_letter]["body"])
    ret.append(content_types[which_letter]["from"]["email_signature"])
    ret.extend(get_postscripts(which_letter))
    return '\n'.join(ret)


def contents():
    """
    Provides a way of getting a quick glimpse
    of the various contents provided.
    Typical usage:
        print('\n'.join(contents()))
    """
    tuples = (('custom_lambdas', custom_lambdas),
              ('letter_bodies', letter_bodies),
              ('post_scripts', post_scripts),
              ('authors', authors),
              ('content_types', content_types),
              ('printers', printers),
              )
    ret = []
    for tup in tuples:
        ret.append('')
        ret.append(tup[0])
        ret.append('=' * len(tup[0]))
        r = []
        for key in tup[1]:
            r.append(key)
        ret.extend(helpers.tabulate(r,
                                    alignment='<',
                                    max_width=140,
                                    separator=' | ')
                   )
    return ret


def categories():
    """
    Needs to be rewritten to take advantage of the -T and -w <width>
    options.
    """
    ret = ["Possible choices for the '--which' option are: ", ]
    ret.extend(
        helpers.tabulate(
            sorted([key for key in content_types.keys()]),
            separator='  '))
#   ret.extend((("\t" + key) for key in content.content_types.keys()))
    return '\n'.join(ret)


if __name__ == "__main__":
    print(categories())
    print('\n'.join(contents()))
    print("code/content.py compiles OK")
