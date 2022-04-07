#!/usr/bin/python3

import pathlib
from collections import defaultdict

# define json file location 
enron_unfiltered = pathlib.Path('/opt/enron_processed/enron_emails.json')

with open(enron_unfiltered) as file:
        lines = file.readlines()
        for line in lines:
            print(line)


