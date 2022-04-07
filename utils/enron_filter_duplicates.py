#!/usr/bin/python3

import json
import pathlib
from collections import defaultdict

# define input and output file location 
enron_unfiltered = pathlib.Path('/opt/enron_processed/enron_emails_unfiltered.json')
enron_filtered = pathlib.Path('/opt/enron_processed/enron_emails.json')


# init dict
main_dict = defaultdict(list)


with open(enron_unfiltered) as file:
        lines = file.readlines()
        for string_line in lines:
            line = json.loads(string_line)
            line_dict = {}
            line_dict['email_message_id'] = line['email_message_id']
            line_dict['email_date'] = line['email_date']
            line_dict['email_from'] = line['email_from']
            line_dict['email_to'] = line['email_to']
            line_dict['email_bcc'] = line['email_bcc']
            line_dict['email_cc'] = line['email_cc']
            line_dict['email_subject'] = line['email_subject']
            line_dict['email_body'] = line['email_body']

            main_dict[line['email_subject']+line['email_body']].append(line_dict)

def clean_email_duplicates(emails_string):
    email_list = emails_string.split(',')
    email_list = list(set(email_list))
    return (",".join(email_list))

duplicate = 0
# itterate through the dict
for key, value in main_dict.items():
    if len(value) > 1 :
        output_dict = {}
        output_dict['email_message_id'] = value[0]['email_message_id']
        output_dict['email_date'] = value[0]['email_date']
        output_dict['email_from'] = value[0]['email_from']
        email_to, email_bcc, email_cc = "", "", ""
        for item in value:
            if item['email_to']:
                email_to = email_to + ',' + item['email_to']
            if item['email_bcc']:
                email_bcc = email_bcc + ',' + item['email_bcc']
            if item['email_cc']:
                email_cc = email_cc + ',' + item['email_cc']

        output_dict['email_to'] = clean_email_duplicates(email_to[1:])
        output_dict['email_bcc'] = clean_email_duplicates(email_bcc[1:])
        output_dict['email_cc'] = clean_email_duplicates(email_cc[1:])
        output_dict['email_subject'] = value[0]['email_subject']
        output_dict['email_body'] = value[0]['email_body']

        with open(enron_filtered, 'a', encoding="utf-8") as outfile:
            json.dump(output_dict, outfile)
            outfile.write('\n')

    else:
        with open(enron_filtered, 'a', encoding="utf-8") as outfile:
            json.dump(value[0], outfile)
            outfile.write('\n')



