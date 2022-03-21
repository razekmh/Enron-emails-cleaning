#!/usr/bin/python3

import pathlib
import pandas as pd

# define the location of the enron dataset
enron_postgres = pathlib.Path('/opt/enron_processed/enron_postgresql/')

# read users table
users_table = enron_postgres / 'users.csv'
users_df = pd.read_csv(users_table, encoding="utf-8")

# count number of unique emails vs number of all emails
print(users_df['user_email'].nunique() / len(users_df['user_email']))

# drop duplicates emails
users_df = users_df.drop_duplicates(subset=['user_email'])

# export to csv
output_path = enron_postgres / 'unique_users.csv'
users_df.to_csv(output_path, index=False)
