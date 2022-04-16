#!/usr/bin/python3
'''
create a neo4j input file from the enron dataset
'''

# import libraries
import pathlib
import pandas as pd
import csv
import pytz
from dateutil import parser

# set timezone and format
utc = pytz.utc
fmt = '%Y-%m-%d %H:%M:%S'

# define path to postgresql data
enron_pg_path = pathlib.Path("/opt/enron_processed/enron_postgresql")

# define the path to the neo4j file
enron_neo4j_path = pathlib.Path('/opt/enron_processed/enron_neo4j')

# read users csv
df_users = pd.read_csv(enron_pg_path / 'unique_users_with_names.csv')

# read emails csv
df_emails = pd.read_csv(enron_pg_path / 'emails.csv', usecols=['email_message_id', 'email_date', 'email_subject','email_body'])

# read transactions csv
df_transactions = pd.read_csv(enron_pg_path / 'unique_email_users.csv')

node_count = 0
# create user nodes
with open (enron_neo4j_path / 'nodes_subset.csv', "w") as users_file:
    fieldnames = ["user_id","user_email","first_name","last_name","rank","role","company"]  
    nodes_writer = csv.DictWriter( users_file, delimiter=',', quoting=csv.QUOTE_ALL, fieldnames=fieldnames, restval="")
    nodes_writer.writeheader()
    nodes_writer.writerow({"user_id":"user_000000"})
    for index, row in df_users.iterrows():
        write_dict = {}
        write_dict['user_email'] = row['user_email'].replace("'", "")
        #standardize user id
        write_dict['user_id'] = "user_" + str(row['user_id']).zfill(6)
        if row['first_name'] != 'None' and not pd.isna(row['first_name']):
            write_dict['first_name'] = row['first_name'].replace("'", "")
        if row['last_name'] != 'None' and not pd.isna(row['last_name']):
            write_dict['last_name'] = row['last_name'].replace("'", "")
        if not pd.isna(row['rank']):
            write_dict["rank"] = row['rank']
        if not pd.isna(row['role']) and row['role'] != "None":
            write_dict["role"] = row["role"]
        if not pd.isna(row["company"]) and row["company"] != "None":
            write_dict["company"] = row["company"]

        nodes_writer.writerow(write_dict)
#        node_count += 1
#        if node_count > 500:
#           break


# create user nodes
#with open (enron_neo4j_path / 'nodes.csv', "w") as users_file:
#    fieldnames = ["user_id","user_email","first_name","last_name","rank","role","company"]  
#    nodes_writer = csv.DictWriter( users_file, delimiter=',', quoting=csv.QUOTE_ALL, fieldnames=fieldnames, restval="")
#    nodes_writer.writerow({"user_id":"user_id:ID","user_email":"user_email","first_name":"first_name","last_name":"last_name","rank":"rank","role":"role","company":"company"}) 
#    nodes_writer.writerow({"user_id":"user_000000"})
#    for index, row in df_users.iterrows():
#        write_dict = {}
#        write_dict['user_email'] = row['user_email'].replace("'", "")
#       #standardize user id
#        write_dict['user_id'] = "user_" + str(row['user_id']).zfill(6)
#        if row['first_name'] != 'None' and not pd.isna(row['first_name']):
#            write_dict['first_name'] = row['first_name'].replace("'", "")
#        if row['last_name'] != 'None' and not pd.isna(row['last_name']):
#            write_dict['last_name'] = row['last_name'].replace("'", "")
#        if not pd.isna(row['rank']):
#            write_dict["rank"] = row['rank']
#        if not pd.isna(row['role']) and row['role'] != "None":
#            write_dict["role"] = row["role"]
#        if not pd.isna(row["company"]) and row["company"] != "None":
#            write_dict["company"] = row["company"]
#
#        nodes_writer.writerow(write_dict)

# # create email relationships
df_relationships = pd.merge(df_transactions, df_emails, on='email_message_id', how='left')

rel_count = 0
with open (enron_neo4j_path / 'relationships_subset.csv', "w") as rel_file:
    fieldnames = ["sender","email_date","email_body","email_subject","email_message_id","transaction_type","routing","receiver","rel_type"]
    rel_writer = csv.DictWriter( rel_file, delimiter=',', quoting=csv.QUOTE_ALL, fieldnames=fieldnames, restval="")
    rel_writer.writeheader()
    for index, row in df_relationships.iterrows():
            rel_dict = {}
            rel_dict["sender"] = "user_" + str(row['sender']).zfill(6)
            rel_dict["receiver"] = "user_" + str(row['receiver']).zfill(6)
            rel_dict['email_date'] = parser.parse(row["email_date"]).astimezone(utc).strftime(fmt)
            if not pd.isna(row['email_subject']):
                email_subject = row['email_subject'].replace("'", "")
                rel_dict["email_subject"] = email_subject.replace(":", " ")
            rel_dict['email_body'] = row['email_body']
            rel_dict['email_message_id'] = row['email_message_id']
            if row["transaction_type"] != "None":
                rel_dict['transaction_type'] = row['transaction_type']
            rel_dict["routing"] = row['external_or_internal']
            rel_dict["rel_type"] = "SENT_TO"
            rel_writer.writerow(rel_dict)    
            rel_count += 1
#            if rel_count > 4000:
#                break 

#with open (enron_neo4j_path / 'relationships.csv', "w") as rel_file:
#    rel_writer.writerow({"sender":":START_ID","email_date":"email_date","email_subject":"email_subject","email_message_id":"email_message_id","transaction_type":"transaction_type","routing":"routing","receiver":":END_ID","rel_type":":TYPE"})
#    for index, row in df_relationships.iterrows():
#        rel_dict = {}
#        rel_dict["sender"] = "user_" + str(row['sender']).zfill(6)
#        rel_dict["receiver"] = "user_" + str(row['receiver']).zfill(6)
#        rel_dict['email_date'] = parser.parse(row["email_date"]).astimezone(utc).strftime(fmt)
#        if not pd.isna(row['email_subject']):
#            email_subject = row['email_subject'].replace("'", "")
#            rel_dict["email_subject"] = email_subject.replace(":", " ")
#        rel_dict['email_message_id'] = row['email_message_id']
#        if row["transaction_type"] != "None":
#            rel_dict['transaction_type'] = row['transaction_type']
#        rel_dict["routing"] = row['external_or_internal']
#        rel_dict["rel_type"] = "SENT_TO"
#        rel_writer.writerow(rel_dict)    
