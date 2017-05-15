#!/usr/bin/env python

"""
Lists and/or deletes Twilio recording files, optionally archiving them.

usage: recordings.py [-h] [--delete] [--no-delete] [--archive ARCHIVE]
                     [--after AFTER] [--before BEFORE] [--summary]
                     [--no-summary] [--verbose] [--no-verbose] [--confirm]
                     [--no-confirm] [--account ACCOUNT] [--password PASSWORD]

optional arguments:
  -h, --help            show this help message and exit
  --delete              Delete recordings (default: False)
  --no-delete
  --archive ARCHIVE     Path to local directory (default: None)
  --after AFTER         yyyy-mm-dd (default: None)
  --before BEFORE, -b BEFORE
                        yyyy-mm-dd (default: None)
  --summary
  --no-summary          Count recordings (default: True)
  --verbose             List recording details (default: False)
  --no-verbose
  --confirm
  --no-confirm          Confirm deletions (default: True)
  --account ACCOUNT, -a ACCOUNT
                        Account SID; if not given, value of environment
                        variable TWILIO_ACCOUNT_SID (default: None)
  --password PASSWORD, -p PASSWORD
                        Auth token; if not given, value of environment
                        variable TWILIO_AUTH_TOKEN (default: None)
"""

# Author:  Robert Welbourn
# Version: 1.0,  2017-05-15


import os
import sys
import datetime
import begin
import requests
from twilio.rest import Client
from twilio.base.exceptions import TwilioException


def download(url, filename):
    """
    Downloads a file from the given URL and stores it in the local file system.  Based on
    http://masnun.com/2016/09/18/python-using-the-requests-module-to-download-large-files-efficiently.html
    """
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as handle:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk:
                handle.write(chunk)


@begin.start
def main(delete:   "Delete recordings" = False,
         archive:  "Path to local directory" = None,
         after:    "yyyy-mm-dd" = None,
         before:   "yyyy-mm-dd" = None,
         summary:  "Count recordings" = True,
         verbose:  "List recording details" = False,
         confirm:  "Confirm deletions" = True,
         account:  "Account SID; if not given, value of environment variable TWILIO_ACCOUNT_SID" = None,
         password: "Auth token; if not given, value of environment variable TWILIO_AUTH_TOKEN" = None):
    """
    Lists and/or deletes Twilio recording files, optionally archiving them.
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

    if after:
        try:
            after = datetime.datetime.strptime(after, '%Y-%m-%d')
        except ValueError:
            sys.exit("Error: invalid after date")

    if before:
        try:
            before = datetime.datetime.strptime(before, '%Y-%m-%d')
        except ValueError:
            sys.exit("Error: invalid before date")

    if after and before:
        if after >= before:
            sys.exit("Error: after date is not before the before date")
    
    # If archiving, and archive directory does not exist, create it.
    if archive:
        try:
            if not os.path.exists(archive):
                os.mkdir(archive)
            else:
                if os.path.isfile(archive):
                    sys.exit("Error: {0} is not a directory".format(archive))
        except OSError:
            sys.exit("Error: unable to create directory {0}".format(archive))

        # Construct base URL for downloading.
        base_url = "https://api.twilio.com/2010-04-01/Accounts/" + account + "/Recordings/"

    # Get the account name; this is used for the confirmation, and is a useful
    # check for correct username and password.
    client = Client(account, password)
    try:
        account_struct = client.api.accounts(account).fetch()
        account_name = account_struct.friendly_name
    except TwilioException:
        sys.exit("Error: invalid account SID or auth token")

    # Ask for confirmation if delete has been selected and confirmation is required.
    if delete and confirm:
        prompt = ("Delete all recordings for account {0} ".format(account_name) + 
                  ("created " if before or after else "") +
                  ("after {0} ".format(after) if after else "") +
                  ("and " if before and after else "") +
                  ("before {0} ".format(before) if before else "") +
                  "(y/n)? ")

        while True:
            response = input(prompt).strip().lower()
            if response in {'n', 'no'}:
                sys.exit("Aborted")
            if response in {'y', "yes"}:
                break

    # Get recordings list.  
    recordings = client.recordings.list(date_created_before=before, date_created_after=after)

    if verbose:
        print("Date/Time Created,Recording SID,Account SID,URI,Duration,Action")

    count = 0
    downloaded = 0
    skipped = 0

    # Loop through the list, downloading and deleting recordings as required.
    for recording in recordings:
        count += 1
        action = ""

        if archive:
            filename = os.path.join(archive, recording.sid + ".mp3")

            # If the file was downloaded previously, don't do it again.
            if os.path.exists(filename):
                skipped += 1
            else:
                url = base_url + recording.sid + ".mp3"
                download(url, filename)
                action = "downloaded"
                downloaded += 1

        if delete:
            client.recordings(recording.sid).delete()
            action = "deleted" if action == "" else (action + "+deleted")

        if verbose:
            print("{0},{1},{2},{3},{4}".format(
                recording.date_created,
                recording.sid,
                recording.call_sid,
                recording.duration,
                action))

    # Finally, print summary.
    if summary:
        print("{0} recordings".format(count) +
              (" deleted" if delete else "") +
              (", {0} downloaded, {1} skipped".format(downloaded, skipped)) if archive else "")
