#!/bin/bash

pwd 
ls /import
while getopts u:p: flag
do
    case "${flag}" in
        u) username=${OPTARG};;
        p) password=${OPTARG};;
    esac
done

cypher-shell -u $username -p $password "
MATCH (n)
DETACH DELETE n"

#cypher-shell -u beo4j -p somepassword "
#USING PERIODIC COMMIT 50
#LOAD CSV WITH HEADERS FROM 'file:///nodes_subset.csv' AS row
#MERGE (u:User {user_id: row.user_id, user_email:row.user_email, first_name: row.first_name, last_name:row.last_name, rank:row.rank, role:row.role, company:row.company})
#RETURN count(u);"

#cypher-shell -u neo4j -p somepassword "
#USING PERIODIC COMMIT 50
#LOAD CSV WITH HEADERS FROM 'file:///relationships_subset.csv' AS row
#WITH row
#MATCH (s:User {user_id: row.sender})
#MATCH (r:User {user_id: row.receiver})
#FOREACH (_ IN CASE WHEN row.transaction_type='to' THEN [1] ELSE [] END |
#MERGE (s)-[:TO {email_date:row.email_date, email_subject:row.email_subject, email_message_id:row.email_message_id, routing:row.routing}]->(r)
#  )
#FOREACH (_ IN CASE WHEN row.transaction_type='bcc' THEN [1] ELSE [] END |
#MERGE (s)-[:BCC {email_date:row.email_date, email_subject:row.email_subject, email_message_id:row.email_message_id, routing:row.routing}]->(r)
#  )
#FOREACH (_ IN CASE WHEN row.transaction_type='cc' THEN [1] ELSE [] END |
#MERGE (s)-[:CC {email_date:row.email_date, email_subject:row.email_subject, email_message_id:row.email_message_id, routing:row.routing}]->(r)
#  )
#;"

#cypher-shell -u neo4j -p somepassword "
#CREATE USER user01 IF NOT EXISTS
#SET PASSWORD ENCRYPTED 'simplepassword'
#SET STATUS ACTIVE
#SET HOME DATABASE neo4j
#"

