#!/bin/bash

curl -H "Content-Type: application/x-ndjson" -XPOST "localhost:9200/enron_emails/email/_bulk?pretty" --data-binary "@/opt/enron_processed/enron_es/enron_emails_elasticsearch.json"
