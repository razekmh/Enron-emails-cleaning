import csv
from pathlib import Path
from py2neo import NodeMatcher,Graph,Node,Relationship
graph = Graph("http://170.187.154.119:7474/db/data/", auth=("neo4j", "somepassword"))

#tx = graph.begin()
selector = NodeMatcher(graph)
node_cache = {}

rel = Path("/opt/enron_processed/enron_neo4j/relationships_subset.csv")
nodes = Path()

with open(nodes, "r") as nodes:
    reader = csv.DictReader(nodes)
    for row in reader: 
        tx =graph.begin()
        n = Node("User", user_id=row['user_id'] 
        "user_id","user_email","first_name","last_name","rank","role","company"


with open(rel, "r") as relations: 
    reader = csv.DictReader(relations)
    for row in reader:
        tx = graph.begin()
        prop = {"email_date":row["email_date"], "email_subject":row["email_subject"],"email_message_id":row["email_message_id"], "routing":row["routing"]}
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
