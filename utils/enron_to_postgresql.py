#!/usr/bin/python3

# TO DO
# change writeline to csv methods

'''convert the extracted emails from enron to a format accpetable by postgres'''

import json
from dateutil import parser
import pathlib

# define the location of the enron dataset
enron_file = pathlib.Path('/opt/enron_processed/enron_emails.json')

# define the path to the output folder
postgres_folder = pathlib.Path('/opt/enron_processed/enron_postgresql/')

# define the path to the emails table
emails_table = postgres_folder / 'emails.csv'

# define the path to the users table
users_table = postgres_folder / 'users.csv'

# define the path to the email_users table
email_users_table = postgres_folder / 'email_users.csv'

# set counter for transactions (emails sent and received) and users
transaction_no = 0
user_no = 0

# set line counter for debugging
line_no = 0

def extract_name_from_email(email):
    if email is None:
        return [None, None]
    user_name = email.split('@')[0]
    if '..' in user_name:
        return [None, None]
    elif '.' in user_name:
        return [user_name.split('.')[0], user_name.split('.')[-1]]
    else:
        return [None, None]

# write the headers for the emails table
with open(emails_table, 'w', encoding="utf-8") as outfile:
    outfile.write('"email_message_id","email_date","email_subject","email_body"')

# write the headers for the users table
with open(users_table, 'w', encoding="utf-8") as outfile:
    outfile.write('user_id,user_email,first_name,last_name')

# write the headers for the email_users table
with open(email_users_table, 'w', encoding="utf-8") as outfile:
    outfile.write('transaction_id,email_message_id,sender,receiver,transaction_type')

# read the enron dataset
with open(enron_file) as file:
    lines = file.readlines()

for line in lines:

    # increment line counter
    line_no += 1
    if line_no % 10000 == 0:
        print(f"Processing line: {line_no}")

    # set null to None
    null = None

    # convert the line to a dictionary
    line_dict = json.loads(line)

    # write the email data to the emails table
    with open(emails_table, 'a', encoding="utf-8") as outfile:
        outfile.write(f'\n"{line_dict["email_message_id"]}","{parser.parse(line_dict["email_date"]).strftime("%Y-%m-%d %H:%M:%S %Z")}","{line_dict["email_subject"]}","{line_dict["email_body"]}"')
    
    # write the user data to the users table
    with open(users_table, 'a', encoding="utf-8") as outfile:
        recipient_list = []
        # write the sender data to the users table
        user_no += 1
        first_name, last_name = extract_name_from_email(line_dict["email_from"])
        outfile.write(f'\n{user_no},{line_dict["email_from"]},{first_name},{last_name}')
        # write the receiver data to the users table
        if line_dict["email_to"]:
            for user in line_dict["email_to"].split(','):
                user_no += 1
                first_name, last_name = extract_name_from_email(user)
                outfile.write(f'\n{user_no},{user},{first_name},{last_name}')
                recipient_list.append((user,'to'))
        # write the cc data to the users table
        if line_dict["email_cc"]:
            for user in line_dict["email_cc"].split(','):
                user_no += 1
                first_name, last_name = extract_name_from_email(user)
                outfile.write(f'\n{user_no},{user},{first_name},{last_name}')
                recipient_list.append((user,'cc'))
        # write the bcc data to the users table
        if line_dict["email_bcc"]:
            for user in line_dict["email_bcc"].split(','):
                user_no += 1
                first_name, last_name = extract_name_from_email(user)
                outfile.write(f'\n{user_no},{user},{first_name},{last_name}')
                recipient_list.append((user,'bcc'))

    # write the email_users data to the email_users table
    with open(email_users_table, 'a', encoding="utf-8") as outfile:
        if len(recipient_list) > 0:
            for recipient in recipient_list:
                transaction_no += 1
                outfile.write(f'\n{transaction_no},{line_dict["email_message_id"]},{line_dict["email_from"]},{recipient[0]},{recipient[1]}')
        else:
            transaction_no += 1
            outfile.write(f'\n{transaction_no},{line_dict["email_message_id"]},{line_dict["email_from"]},{None},{None}')
