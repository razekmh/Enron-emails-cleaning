#!/bin/bash

pwd 
ls /import

cypher-shell -u neo4j -p somepassword "
MATCH (n)
DETACH DELETE n"

cypher-shell -u neo4j -p somepassword "
USING PERIODIC COMMIT 50
LOAD CSV WITH HEADERS FROM 'file:///nodes_subset.csv' AS row
MERGE (u:User {user_id: row.user_id, user_email:row.user_email, first_name: row.first_name, last_name:row.last_name, rank:row.rank, role:row.role, company:row.company})
RETURN count(u);"

cypher-shell -u neo4j -p somepassword "
USING PERIODIC COMMIT 100
LOAD CSV WITH HEADERS FROM 'file:///relationships_subset.csv' AS row
MATCH (s:User {user_id: row.sender})
MATCH (r:User {user_id: row.receiver})
MERGE (s)-[:SENT_TO {email_date:row.email_date, email_subject:row.email_subject, email_message_id:row.email_message_id, routing:row.routing}]->(r)
RETURN count(r);"
