#!/usr/bin/env python3

"""
Utility to print CDRs from the Twilio API.

usage: cdrs.py [-h] [--start START] [--end END] [--account ACCOUNT]
               [--password PASSWORD] [--subaccount SUBACCOUNT]

Prints CDRs to cdrs_<end date>.csv, between and including the two given dates.

optional arguments:
  -h, --help            show this help message and exit
  --start START         yyyy-mm-dd, at 00:00:00 (default: None)
  --end END, -e END     yyyy-mm-dd, at 23:59:59 (default: None)
  --account ACCOUNT, -a ACCOUNT
                        Account SID; if not given, value of environment
                        variable TWILIO_ACCOUNT_SID (default: None)
  --password PASSWORD, -p PASSWORD
                        Auth token; if not given, value of environment
                        variable TWILIO_AUTH_TOKEN (default: None)
  --subaccount SUBACCOUNT, -s SUBACCOUNT
                        If present, subaccount to use (default: None)
"""


import sys
import os
import time
from datetime import datetime, timedelta
import begin
from twilio.rest import Client


@begin.start
def main(start:      "yyyy-mm-dd, at 00:00:00" = None,
         end:        "yyyy-mm-dd, at 23:59:59" = None,
         account:    "Account SID; if not given, value of environment variable TWILIO_ACCOUNT_SID" = None,
         password:   "Auth token; if not given, value of environment variable TWILIO_AUTH_TOKEN" = None,
         subaccount: "If present, subaccount to use" = None):
    """
    Prints CDRs to cdrs_<end date>.csv, between and including the two given dates.
    """

    # Validate command line arguments.
    if account is None:
        try:
            account = os.environ['TWILIO_ACCOUNT_SID']
        except KeyError:
            sys.exit("Error: no account, nor environment variable TWILIO_ACCOUNT_SID")

    if password is None:
        try:
            password = os.environ['TWILIO_AUTH_TOKEN']
        except KeyError:
            sys.exit("Error: no password, nor environment variable TWILIO_AUTH_TOKEN")

    if start:
        try:
            start = datetime.strptime(start, '%Y-%m-%d')
        except ValueError:
            sys.exit("Error: invalid start date")
    else:
        sys.exit("Error: start date missing")

    if end:
        try:
            end = datetime.strptime(end, '%Y-%m-%d')
        except ValueError:
            sys.exit("Error: invalid end date")
    else:
        sys.exit("Error: end date missing")

    # Create filename for CDRs, based on given end date.
    cdrs_filename = "cdrs_{}-{:02}-{:02}.csv".format(end.year, end.month, end.day)
    
    # Create client object
    client = Client(account, password, subaccount)

    # Read CDRs for the given date range.  Get the local timezone offset, 
    # and start on the start day at 00:00:00, and end on the end day at 23:59:59.
    local_tz_offset = timedelta(seconds=time.timezone)
    interval_start = datetime(start.year, start.month, start.day) + \
                     local_tz_offset
    interval_end = datetime(end.year, end.month, end.day) + \
                   local_tz_offset + timedelta(hours=23, minutes=59, seconds=59)
    calls = client.calls.list(start_time_after=interval_start,
                              start_time_before=interval_end)

    # Print CDRs.
    with open(cdrs_filename, 'w') as cdr_file:
        print("SID,Parent Call SID,Date Created,Date Updated,Account SID,"
              "To,From,Phone Number SID,Status,Start Time,End Time,Duration,"
              "Price,Price Unit,Direction,Answered By,Forwarded From,"
              "To Formatted,From Formatted,Caller Name", file=cdr_file)
            
        for call in calls:
            print("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".
                  format(call.sid,
                         call.parent_call_sid,
                         call.date_created,
                         call.date_updated,
                         call.account_sid,
                         call.to,
                         call.from_,
                         call.phone_number_sid,
                         call.status,
                         call.start_time,
                         call.end_time,
                         call.duration,
                         call.price,
                         call.price_unit,
                         call.direction,
                         call.answered_by,
                         call.forwarded_from,
                         call.to_formatted,
                         call.from_formatted,
                         call.caller_name), file=cdr_file)
