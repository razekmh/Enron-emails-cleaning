#!/usr/bin/python3
'''
create a neo4j input file from the enron dataset
'''

# import libraries
import pathlib
import pandas as pd
import csv

# define the path to the enron dataset
enron_pg_path = pathlib.Path('/opt/enron_processed/enron_postgresql')

# define the path to the neo4j file
enron_neo4j_path = pathlib.Path('/opt/enron_processed/enron_neo4j')

# read users csv
df_users = pd.read_csv(enron_pg_path / 'unique_users_with_names.csv')

# read emails csv
df_emails = pd.read_csv(enron_pg_path / 'emails.csv', usecols=['email_message_id', 'email_date', 'email_subject'])

# read transactions csv
df_transactions = pd.read_csv(enron_pg_path / 'unique_email_users.csv')

# create user nodes
with open (enron_neo4j_path / 'nodes.csv', "w") as users_file:
    fieldnames = ["user_id","user_email","first_name","last_name","rank"]  
    nodes_writer = csv.DictWriter( users_file, delimiter=',', quoting=csv.QUOTE_ALL, fieldnames=fieldnames)
    nodes_writer.writerow({"user_id":"user_id:ID","user_email":"user_email","first_name":"first_name","last_name":"last_name","rank":"rank"}) 
    nodes_writer.writerow({"user_id":"user_000000"})
    for index, row in df_users.iterrows():
        #clean email address
        row['user_email'] = row['user_email'].replace("'", "")
        #standardize user id
        row['user_id'] = "user_" + str(row['user_id']).zfill(6)
        if row['first_name'] != 'None' and not pd.isna(row['first_name']):
            # clean first name
            row['first_name'] = row['first_name'].replace("'", "")
        else:
            row['first_name'] = ''
        if row['last_name'] != 'None' and not pd.isna(row['last_name']):
            # clean last name
            row['last_name'] = row['last_name'].replace("'", "")
        else: 
            row['last_name'] = ''
        if not pd.isna(row['rank']):
            pass
        else:
            row['rank'] = ''
        
        nodes_writer.writerow(row)

# # create email relationships
df_relationships = pd.merge(df_transactions, df_emails, on='email_message_id', how='left')

# with open (enron_neo4j_path / 'relationships.txt', 'w') as emails_file:
#     for index, row in df_relationships.iterrows():
#         sender_id = "user_" + str(row['sender']).zfill(6)
#         receiver_id = "user_" + str(row['receiver']).zfill(6)
#         emails_file.write(f"MATCH (sender:Person {{user_id:'{sender_id}'}}), (receiver:Person {{user_id:'{receiver_id}'}})")
#         emails_file.write(f"MERGE (sender)-[:SENT_EMAIL {{date:'{row['email_date']}'")
#         if not pd.isna(row['email_subject']):
#             email_subject = row['email_subject'].replace("'", "")
#             email_subject = email_subject.replace(":", " ")
#             emails_file.write(f", subject:'{email_subject}'")
#         emails_file.write(f", message_id:'{row['email_message_id']}'")
#         emails_file.write(f", type: '{row['transaction_type']}'")
#         emails_file.write(f", routing: '{row['external_or_internal']}'")
#         emails_file.write("}]->(receiver)")
#         emails_file.write(";\n")


# create list of files for neo4j relationship import
rel_counter = 0
rel_file_stem = 'relationships'
rel_file_name = rel_file_stem + str(rel_counter) + '.txt'

for index, row in df_relationships.iterrows():
    if rel_counter % 100000 == 0:
        rel_file_name = rel_file_stem + str(rel_counter).zfill(9) + '.txt'
    with open (enron_neo4j_path / rel_file_name, 'a+') as rel_file:
        sender_id = "user_" + str(row['sender']).zfill(6)
        receiver_id = "user_" + str(row['receiver']).zfill(6)
        rel_file.write(f"MATCH (sender:Person {{user_id:'{sender_id}'}}), (receiver:Person {{user_id:'{receiver_id}'}})")
        rel_file.write(f"MERGE (sender)-[:SENT_EMAIL {{date:'{row['email_date']}'")
        if not pd.isna(row['email_subject']):
            email_subject = row['email_subject'].replace("'", "")
            email_subject = email_subject.replace(":", " ")
            rel_file.write(f", subject:'{email_subject}'")
        rel_file.write(f", message_id:'{row['email_message_id']}'")
        rel_file.write(f", type: '{row['transaction_type']}'")
        rel_file.write(f", routing: '{row['external_or_internal']}'")
        rel_file.write("}]->(receiver)")
        rel_file.write(";\n")
        rel_counter += 1
            


#     #     emails_file.write(f"CREATE ({sender_id})-[:SENT_TO{{message_id:'{row['email_message_id']}', subject:'{row['email_subject']}', date:'{row['email_date']}', type: '{row['transaction_type']}', routing: '{row['external_or_internal']}'}}]->({receiver_id})\n")
#     # emails_file.write(";")

# rel_file.write("USING PERIODIC COMMIT 1000\n")
#             rel_file.write("LOAD CSV WITH HEADERS FROM 'file:///relationships.txt' AS row\n")
#             rel_file.write("CREATE (sender:Person {{user_id:row.sender}}), (receiver:Person {{user_id:row.receiver}})")
#             rel_file.write("MERGE (sender)-[:SENT_EMAIL {{date:row.email_date")
#             if not pd.isna(row['email_subject']):
#                 email_subject = row['email_subject'].replace("'", "")
#                 email_subject = email_subject.replace(":", " ")
#                 rel_file.write(f", subject:'{email_subject}'")
#             rel_file.write(f", message_id:'{row['email_message_id']}'")
#             rel_file.write(f", type: '{row['transaction_type']}'")
#             rel_file.write(f", routing: '{row['external_or_internal']}'")
#             rel_file.write("}]->(receiver)")
#             rel_file.write(";\n")
