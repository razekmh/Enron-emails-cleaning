import csv
import sys
import  getopt
from pathlib import Path
from py2neo import NodeMatcher,Graph,Node,Relationship

username = sys.argv[2]
password = sys.argv[4]

print(username,password)
#graph = Graph("http://170.187.154.119:7474/db/data/", auth=("neo4j", "somepassword"))
graph = Graph("bolt://170.187.154.119:7687", auth=(username,password))

#tx = graph.begin()
selector = NodeMatcher(graph)
node_cache = {}

rel = Path("/opt/enron_processed/enron_neo4j/relationships_subset.csv")
nodes = Path("/opt/enron_processed/enron_neo4j/nodes_subset.csv")

#set field maxsize
maxInt = sys.maxsize

while True:
        # decrease the maxInt value by factor 10 
        # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

with open(nodes, "r") as nodes:
    reader = csv.DictReader(nodes)
    for row in reader: 
        tx = graph.begin()
        n = Node("User", user_id=row['user_id'], user_email=row['user_email'], first_name=row['first_name'], last_name=row['last_name'], rank=row['rank'], role=row['role'], company=row['company'])
        tx.create(n)
        tx.commit()

with open(rel, "r") as relations: 
    reader = csv.DictReader(relations)
    for row in reader:
        tx = graph.begin()
        prop = {"email_date":row["email_date"], "email_subject":row["email_subject"],"email_body":row["email_body"],"email_message_id":row["email_message_id"], "routing":row["routing"]}
        sender = row['sender']
        receiver = row['receiver']
        
        # Check if we have this node in the cache
        if sender in node_cache:
            node1 = node_cache[sender]
        else:
            # Query and store for later
            node1 = selector.match(user_id=sender).first()
            node_cache[sender] = node1

        if receiver in node_cache:
            node2 = node_cache[receiver]

        else:
            node2 = selector.match(user_id=receiver).first()
            node_cache[receiver] = node2
        if not row['transaction_type']:
            row['transaction_type'] = "unknown"
        rs = Relationship(node1,row['transaction_type'],node2,**prop)
        tx.create(rs)
        tx.commit()
