# Twilio-Tools
Miscellaneous Python utilities for managing Twilio accounts

## Installation
Clone or unzip this repository into your project directory.  If you're using a [Virtual Environment](https://virtualenv.pypa.io/en/stable/userguide/), do the following in your project directory:
```
python3 -m venv ENV
source ENV/bin/activate
```
Next, install the required Python libraries:
```
pip install -r requirements.txt
```

## recordings.py
Lists and/or deletes Twilio recording files, optionally archiving them.

```
usage: recordings.py [-h] [--delete] [--no-delete] [--archive ARCHIVE]
                     [--after AFTER] [--before BEFORE] [--summary]
                     [--no-summary] [--verbose] [--no-verbose] [--confirm]
                     [--no-confirm] [--account ACCOUNT] [--password PASSWORD]
                     [--subaccount SUBACCOUNT]

Lists and/or deletes Twilio recording files, optionally archiving them.

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
  --subaccount SUBACCOUNT, -s SUBACCOUNT
                        If present, subaccount to use (default: None)
 ```                       

## cdrs.py
Prints Twilio call detail records for a given date range.

```
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
```
