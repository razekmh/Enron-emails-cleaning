#!/usr/bin/python3

'''
converts enron json dump data to elasticsearch format
'''

# import modules
import json
import pathlib
import pytz
from dateutil import parser


# set timezone and format
utc = pytz.utc
fmt = '%Y-%m-%d %H:%M:%S'

# set the input and output paths
input_path = pathlib.Path('/opt/enron_processed/enron_emails.json')
output_path = pathlib.Path('/opt/enron_processed/enron_es/enron_emails_elasticsearch.json')

# set counter for the records
counter = 0 

# writer function
def write_line(line):
    '''
    writes a line to the output file
    '''
    with open(output_path, 'a') as f:
        f.write(json.dumps(line))
        f.write('\n')

# read in json file line by line
with open(input_path, 'r') as f:
    for line in f:
#        if counter < 30000:
            # convert line to json
            email = json.loads(line)
            # convert date to utc
            email['email_date'] = parser.parse(email["email_date"]).astimezone(utc).strftime(fmt)
            # # convert date to utc
            # email['email_date'] = email['email_date'].astimezone(utc).strftime(fmt)
            write_line(email)
            counter += 1
