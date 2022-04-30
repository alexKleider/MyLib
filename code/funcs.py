#!/usr/bin/env python3

# File: code/funcs.py

"""
Most functions in this module pertain to contact records and many (so
called 'collector' functions) store data in one or more attributes of
an instance of letters.Gbls; hence the extra (named) parameter which
can be left as 'gbls=None' when it's not needed.
"""

import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])
import csv
import json
from code import content, helpers


demographic_f = (
    "{first} {last}  {address}, {town}, {state} {postal_code}")
demographic_f_w_phone_and_email = (
    "{first} {last} [{phone}] {address}, {town}, {state} " +
    "{postal_code} [{email}]")
demographic_f_last_first = (
    "{last}, {first}  {address}, {town}, {state} {postal_code}")
demographic_f_last_first_w_phone_and_email = (
    "{last}, {first} [{phone}] {address}, {town}, {state} " +
    "{postal_code} [{email}]")
demographic_f_last_first_w_staggered_data = '\n'.join((
    "{last}, {first} [{phone}]",
    "\t{address}, {town}, {state} {postal_code}",
    "\t[{email}]"))
demographic_f_first_last_w_staggered_data = '\n'.join((
    "{first}, {last} [{phone}]",
    "\t{address}, {town}, {state} {postal_code}",
    "\t[{email}]"))
fstrings = {
        'first_last': "{first} {last}",
        "last_first": "{last}, {first}",
        'first_last_w_address_only': demographic_f, 
        'first_last_w_all_data': demographic_f_w_phone_and_email,
        'last_first_w_address_only': demographic_f_last_first,
        'last_first_w_all_data':
                    demographic_f_last_first_w_phone_and_email,
        'first_last_w_all_staggered':
                    demographic_f_last_first_w_staggered_data,
        'last_first_w_all_staggered': 
                    demographic_f_first_last_w_staggered_data,
    }


def format_record(record, f_str=fstrings['last_first']):
    """
    Retrieves a string representation of a record.
    Default is to return the name in last, first format.
    """
    return f_str.format(**record)



def names_reversed(name):
    """
    Changes 'first last' to 'last, first'
    and 'last, first' to 'first last'.
    # Should be able to organize code such that this is never needed.
    """
    if ', ' in name:
        parts = name.split(', ')
        return '{} {}'.format(parts[1].strip(), parts[0].strip())
    else:
        parts = name.rsplit(maxsplit=1)
        return '{}, {}'.format(parts[1].strip(), parts[0].strip())


def traverse_records(infile, custom_funcs, gbls):
    # This function is to collect specific data.
    """
    Opens <infile> for dict_reading (and in the process
    assigns gbls.fieldnames.
    Applies <custom_funcs> to each record.
    <custom_funcs> can be a single function or a
    list of functions. These functions typically populate
    attributes of gbls, an instance of the letters.Gbls class.
    Required gbls attributes are set up using the
    setup_required_attributes function (see end of module.)
    Also assigns gbls.fieldnames and gbls.n_fields which are
    sometimes useful.
    """
    if callable(custom_funcs):  # If only one function provided
        custom_funcs = [custom_funcs]  # place it into a list.
    setup_required_attributes(custom_funcs, gbls)
    with open(infile, 'r', newline='') as file_object:
        print("DictReading {}...".format(file_object.name))
        dict_reader = csv.DictReader(file_object)
        gbls.fieldnames = dict_reader.fieldnames  # may be unnecessary
        gbls.n_fields = len(gbls.fieldnames)  # to check db integrity
        for record in dict_reader:
            for custom_func in custom_funcs:
                custom_func(record, gbls)


def report_error(report, gbls):
    """
    <report> is appended to gbls.errors (if the attribute exists,
    else <report> is printed to the terminal.)
    """
    try:
        gbls.errors.append(report)
    except AttributeError:
        print(report)


def increment_nrecords(record, gbls):
    gbls.nrecords += 1


def ck_number_of_fields(record, gbls=None):
    """
    Checks that there are the correct number of fields in "record".
    If "gbls" is specified, errors are appended to gbls.errors
    which must be set up by client;
    if not: error is reported by printing to stdout.
    """
    n_fields = len(record)
    possible_error = ("{last} {first} has {N_FIELDS}".format(
                                                    **record))
    if ((gbls and (n_fields != gbls.n_fields))
            or n_fields != N_FIELDS):
        report_error(possible_error, gbls)


def get_usps(record, gbls):
    """
    Selects members who get their copy of meeting minutes by US
    Postal Service. i.e. Those with no email.
    Populates gbls.usps_only with a line for each such member
    using csv format: first, last, address, town, state, and
    postal_code.
    """
    if not record['email']:
        gbls.usps_only.append(demographic_f.format(**record))


# # Beginning of 'add2' functions:

def add2email_by_m(record, gbls):
    """
    Populates dict- gbls.email_by_name.
    """
    record = code.helpers.Rec(record)
    name = record(fstrings['last_first'])
    email = record['email']
    if email:
        gbls.email_by_m[name] = email


def add2db_emails(record, gbls):
    """
    Populates gbls.db_emails
    'ex' for experimental
    db_emails is a dict with all members included but
    with a special key for those without email
    """
#   print("called add2db_emails")
    record = helpers.Rec(record)
    name = record(fstrings['last_first'])
    email = record['email']
    if not email:
        email = NO_EMAIL_KEY
    gbls.db_emails[name] = email


def add2ms_by_email(record, gbls):
    """
    Populates gbls.ms_by_email, a dict keyed by emails one of which
    is NO_EMAIL_KEY to capture members without an email address.
    """
    record = helpers.Rec(record)
    name = record(fstrings['last_first'])
    email = record['email']
    if not email:
        email = NO_EMAIL_KEY
    _ = gbls.ms_by_email.setdefault(email, [])
    gbls.ms_by_email[email].append(name)


def add2demographics(record, gbls):
    """
    Appends a record to gbls.demographics:
        Each key is a member name in last_first format
        Each value is the record in format specified
            by gbls.format
    """
    record = helpers.Rec(record)
    gbls.demographics[record(fstrings['last_first'])] = (
          record(gbls.format)) 


def add2member_with_email_set(record, gbls):
    """
    Appends a record to gbls.member_with_email_set if record
    is that of a member and the member has an email address.
    ## Proposal: rename 'add2has_email_set' and store in 
                        'gbls.has_email_set'.
    """
    record = helpers.Rec(record)
    entry = record(fstrings['last_first'])
    if record['email'] and is_member(record):
        gbls.member_with_email_set.add(entry)
    else:
        gbls.no_email_set.add(entry)


def add2malformed(record, gbls):
    """
    Populates gbls.malformed (which must be set up by client.)
    Checks that that for each record:
    1. there are N_FIELDS per record.
    2. the email field contains "@"
    3. the name does not alphabetically preceed the one before
    (... used for comparison re correct ordering.)
    """
    record = helpers.Rec(record)
    name = record(fstrings['last_first'])
    if len(record) != N_FIELDS:
        gbls.malformed.append("{}: Wrong # of fields.".format(name))
    if record["email"] and '@' not in record["email"]:
        gbls.malformed.append("{}: {} Problem /w email.".format(
                                            name, record['email']))
    if name < gbls.previous_name:
        gbls.malformed.append("Record out of order: {}".format(name))
    gbls.previous_name = name

# End of 'add2...' functions


def modify_data(csv_in_file_name, func, gbls):
    # Rename?: 'traverse_csv', 'modified_data'
    # Note: 'traverse_records' collects data, this 
    # does something fundamentally different.
    """
    A generator: reads a csv file and for each entry, yields a record
    modified by func (or, if func==None, the record unchanged.)
    """
    with open(csv_in_file_name, 'r', newline='') as file_obj:
        reader = csv.DictReader(file_obj)
        for rec in reader:
            if func == None:
                yield rec
            else:
                yield func(rec, gbls)


def name_w_demographics(record, gbls):
    stati = get_status_set(record)
    if not record['email']:
        record['email'] = 'no email'
    if not record['phone']:
        record['phone'] = 'no phone'
    line = gbls.PATTERN4WEB.format(**record)
    if "be" in stati:
        line = line + " (bad email!)"
    if "ba" in stati:
        line = line + " (mail returned!)"
    return line


def append_email(record, gbls):
    """
    gbls.which has already been assigned to one of the values
    of content.content_types
    Appends an email to gbls.json_data
    """
#   print(gbls.email)
    body = gbls.email_template.format(**record)
    sender = gbls.which['from']['email']
    email = {
        'From': sender,    # Mandatory field.
        'Sender': sender,   # 0 or 1
        'Reply-To': gbls.which['from']['reply2'],  # 0 or 1
        'To': record['email'],  # at least one ',' separated address
        'Cc': '',             # O or 1 comma separated list.
        'Bcc': '',            # O or 1 comma separated list.
        'Subject': gbls.which['subject'],  # 0 or 1
        'attachments': [],
        'body': body,
    }
    email['Cc'] = gbls.d["--cc"]
    email['Bcc'] = gbls.d["--bcc"]
    email["attachments"] = gbls.d["ATTACHMENTS"]
    gbls.json_data.append(email)


def file_letter(record, gbls):
    entry = gbls.letter_template.format(**record)
    path2write = os.path.join(gbls.d['--dir'],
                              "_".join((record["last"],
                                        record["first"])))
    with open(path2write, 'w') as file_obj:
        file_obj.write(helpers.indent(entry,
                          content.printers[gbls.d['-p']]["indent"]))


def q_mailing(record, gbls):
    """
    Dispatches email &/or letter to appropriate
    (email &/or letter) 'bin'.
    """
    content_type = content.content_types[gbls.d['--which']]
    record["subject"] = content_type["subject"]
    # ^ the above should be assigned elsewhere!!
    # check how to send:
    how = content_type["e_and_or_p"]
    if how == "email":
        append_email(record, gbls)
    elif how == "both":
        append_email(record, gbls)
        file_letter(record, gbls)
    elif how == 'one_only':
        if record['email']:
            append_email(record, gbls)
        else:
            file_letter(record, gbls)
    elif how == 'usps':
        file_letter(record, gbls)
    else:
        print("Problem in q_mailing: letter/email not sent to {}."
                .format(fstrings['first_last'].format(**record)))


def prepare_mailing(gbls):
    """
    Clients of this method: utils.prepare_mailing_cmd
                            utils.thank_cmd
    Both use utils.prepare4mailing to assign attributes to <gbls>
    (See Notes/call_flow.)
    """
    traverse_records(gbls.infile,
            content.content_types[gbls.d['--which']]["funcs"],
             gbls)  # 'which' comes from content
#   listing = [func.__name__ for func in gbls.which["funcs"]]
#   print("Functions run by traverse_records: {}".format(listing))
    # No point in creating a json file if no emails:
    if hasattr(gbls, 'json_data') and gbls.json_data:
        with open(gbls.d['-j'], 'w') as file_obj:
            print('Dumping emails (JSON) to "{}".'
                    .format(file_obj.name))
            file_obj.write(json.dumps(gbls.json_data))
    else:
        print("There are no emails to send.")


# ## The following are functions used for mailing. ###
# # These are special functions suitable for the <func_dict>:
# # they provide necessary attributes to their 'record' parameter
# # in order to add custom content (to a letter &/or email.)


def std_mailing_func(record, gbls):
    """
    Assumes any prerequisite processing has been done and
    requisite values added to record.
    Mailing is sent if the "test" lambda => True.
    Otherwise the record is ignored.
    """
    content_type = content.content_types[gbls.d['--which']]
    if content_type["test"](record):
        record["subject"] = content_type["subject"]
        q_mailing(record, gbls)


def bad_address_mailing_func(record, gbls):
    content_type = content.content_types[gbls.d['--which']]
    if content_type["test"](record):
        record["subject"] = content_type["subject"]
        record['extra'] = ("{address}\n{town}, {state} {postal_code}"
                           .format(**record))
        q_mailing(record, gbls)


def testing_func(record, gbls):
    """
    For mailings which require no special processing.
    Mailing is sent if the "test" lambda => True.
    Otherwise the record is ignored.
    """
    content_type = content.content_types[gbls.d['--which']]
    if content_type["test"](record):
        record["subject"] = content_type["subject"]
        record['extra'] = "Blah, Blah, Blah!"
        q_mailing(record, gbls)




def setup_required_attributes(custom_funcs, gbls):
    """
    Ensures that gbls has necessary attributes
    required by all the custom_funcs to be called.
    """
    prerequisites = {   # collectors needed by the
                        # various traversing functions
        add2db_emails: [
            "gbls.db_emails = {}",
            ],
        ck_number_of_fields: [
            "gbls.errors = []",
            ],
        increment_nrecords: [
            "gbls.nrecords = 0",
            ],
        add2malformed: [
            'gbls.malformed = []',
            'gbls.previous_name = ""',
            ],
        std_mailing_func: [
            "gbls.json_data = []",
            ],
        }

    set_of_funcs = set(prerequisites.keys())
    for func in custom_funcs:
        if func in set_of_funcs:
            for code in prerequisites[func]:
                exec(code)


if __name__ == "__main__":
    print("code/funcs.py compiles OK.")

