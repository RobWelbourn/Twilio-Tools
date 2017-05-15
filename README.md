# Twilio-Tools
Miscellaneous Python utilities for managing Twilio accounts

## recordings.py
Lists and/or deletes Twilio recording files, optionally archiving them.

### Pre-Requisites
`recordings.py` requires the [Twilio](https://github.com/twilio/twilio-python), [Begins](https://pypi.python.org/pypi/begins/0.9) and [Requests](http://docs.python-requests.org/en/master/) packages:

```
pip install twilio
pip install begins
pip install requests
```

It was tested using Python 3.6.

### Usage
```
recordings.py [-h] [--delete] [--no-delete] [--archive ARCHIVE]
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
 ```                       
