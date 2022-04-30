#!/usr/bin/env python

# File: code/mail.py

import os
import csv
import json
import shutil
from code import helpers, funcs, content, globals, send

def display_emails(email_json_file):
    """
    Returns a human readable string displaying
    all the emails in <email_json_file>.
    """
    print("Displaying emails NOT YET IMPLEMENTED.")
    records = helpers.get_json(email_json_file, report=True)
    all_emails = []
    n_emails = 0
    for record in records:
        email = []
        for field in record:
            email.append("{}: {}".format(field, record[field]))
        email.append('')
        all_emails.extend(email)
        n_emails += 1
    print("Processed {} emails...".format(n_emails))
    return "\n".join(all_emails)


def send_emails(gbls):
    """
    Sends emails prepared by prepare_mailing_cmd.
    See also content.authors_DOCSTRING.
    """
    print("Sending emails found in {}..."
            .format(gbls.d['-j']))
#   print("NOT YET IMPLEMENTED")
    mta = gbls.d["--mta"]
    wait = mta.endswith('g')
    message = None
    data = helpers.get_json(gbls.d['-j'], report=True)
    send.send(data, mta, include_wait=wait)
    print("...finished sending emails.")

    
def generate_mailing(gbls):
    # give user opportunity to abort if files are still present:
    helpers.check_before_deletion((gbls.d['-j'], gbls.d['--dir']))
    if os.path.exists(gbls.d['--dir']): shutil.rmtree(gbls.d['--dir'])
    os.mkdir(gbls.d['--dir'])
    gbls.json_data = []
    gbls.email_template = content.prepare_email_template(
            gbls.d['--which'])
    gbls.letter_template = content.prepare_letter_template(
            gbls.d['--which'], gbls.d['-p'])
    traverse_records(gbls.d['-i'],
                 content.content_types[gbls.d['--which']]["funcs"],
                 gbls)  # 'which' comes from content
    # No point in creating a json file if no emails:
    if hasattr(gbls, 'json_data') and gbls.json_data:
        with open(gbls.d['-j'], 'w') as file_obj:
            print('Dumping emails (JSON) to "{}".'
                    .format(file_obj.name))
            file_obj.write(json.dumps(gbls.json_data))
    else:
        print("There are no emails to send.")
    # Check if any letters are filed and if not, delete mailing dir:
    if os.path.isdir(gbls.d['--dir']) and not len(
            os.listdir(gbls.d['--dir'])):
        os.rmdir(gbls.d['--dir'])
        print("Empty mailing directory deleted.")
    else:
        print("Letters exist..")
        print("""..next step might be to:
    $ cd {}
    $ zip -r 4Peter MailDir
... or using tar:
    $ tar -vczf 4Peter.tar.gz MailDir""".format(globals.DATA_DIR))


def append_email(record, gbls):
    """
    gbls.which has already been assigned to one of the values
    of content.content_types
    Appends an email to gbls.json_data
    """
#   print(gbls.email)
    body = gbls.email.format(**record)
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
    if gbls.cc: ccs = gbls.cc
    else: ccs = ''
    email['Cc'] = helpers.join_email_listings(
                                    sponsor_email_addresses, ccs)
    if gbls.bcc:
        email['Bcc'] = gbls.bcc
    gbls.json_data.append(email)


def file_letter(record, gbls):
    entry = gbls.letter.format(**record)
    path2write = os.path.join(gbls.MAILING_DIR,
                              "_".join((record["last"],
                                        record["first"])))
    with open(path2write, 'w') as file_obj:
        file_obj.write(helpers.indent(entry,
                                      gbls.lpr["indent"]))


def q_mailing(record, gbls):
    """
    Dispatches email &/or letter to appropriate 'bin'.
    """
    record["subject"] = gbls.which["subject"]
    # ^ the above should be assigned elsewhere!!
    # check how to send:
    how = gbls.which["e_and_or_p"]
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


## the following lived in member.py:

def traverse_records(infile, custom_funcs, gbls):
    # Fundamentally different from <modify_data>/<modified_data>!
    # This function is to collect specific data, not change it.
    """
    Opens <infile> for dict_reading (and in the process
    assigns gbls.fieldnames.
    Applies <custom_funcs> to each record.
    <custom_funcs> can be a single function or a
    list of functions. These functions typically populate
    attributes of gbls, an instance of the rbc.Gbls class.
    Required gbls attributes are set up using the
    setup_required_attributes function (see end of module.)
    Also assigns gbls.fieldnames and gbls.n_fields which are
    sometimes useful.
    """
    if callable(custom_funcs):  # If only one function provided
        custom_funcs = [custom_funcs]  # place it into a list.
    funcs.setup_required_attributes(custom_funcs, gbls)
    with open(infile, 'r', newline='') as file_object:
        print("DictReading {}...".format(file_object.name))
        dict_reader = csv.DictReader(file_object)
        # fieldnames is used by get_usps and restore_fees cmds.
        gbls.fieldnames = dict_reader.fieldnames
        gbls.n_fields = len(gbls.fieldnames)  # to check db integrity
        for record in dict_reader:
            for custom_func in custom_funcs:
                custom_func(record, gbls)


def prepare_mailing(gbls):
    """
    Clients of this method: utils.prepare_mailing_cmd
                            utils.thank_cmd
    Both use utils.prepare4mailing to assign attributes to <gbls>
    (See Notes/call_flow.)
    """


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
    if gbls.which["test"](record):
        record["subject"] = gbls.which["subject"]
        if gbls.cc_sponsors:
            pass
        if gbls.owing_only:
            if record['owing']:
                q_mailing(record, gbls)
        else:
            q_mailing(record, gbls)


def bad_address_mailing_func(record, gbls):
    if gbls.which["test"](record):
        record["subject"] = gbls.which["subject"]
        record['extra'] = ("{address}\n{town}, {state} {postal_code}"
                           .format(**record))
        q_mailing(record, gbls)


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

### above comes from member.py


def prepare4mailing(gbls):
    """
    Set up configuration in an instance of rbc.Gbls.
    ## Need to implement sending of copies to       ##
    ## sponsors if "-cc sponsors" option is chosen. ##
    """

def prepare_mailing_cmd(args):
    """
    See description under 'Commands' heading in the docstring.
    Sets up an instance of rbc.Gbls with necessary attributes and
    then calls member.prepare_mailing.
    ## Need to implement sending of copies to       ##
    ## sponsors if "-cc sponsors" option is chosen. ##
    """
    # ***** Set up configuration in an instance of # Gbls:
    gbls = Gbls(args)
    prepare4mailing(gbls)
    # ***** Done with configuration & checks ...
    member.prepare_mailing(gbls)  # Populates gbls.mail_dir
    #                               and moves json_data to file.
    # Check if any letters are filed and if not, delete mailing dir:
    if os.path.isdir(gbls.mail_dir) and not len(
            os.listdir(gbls.mail_dir)):
        os.rmdir(gbls.mail_dir)
        print("Empty mailing directory deleted.")
    else:
        print("""..next step might be the following:
    $ zip -r 4Peter {0:}
    (... or using tar:
    $ tar -vczf 4Peter.tar.gz {0:}"""
            .format(gbls.mail_dir))
    print("prepare_mailing completed..")

