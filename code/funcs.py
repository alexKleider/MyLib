#!/usr/bin/env python3

# File: code/funcs.py


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

