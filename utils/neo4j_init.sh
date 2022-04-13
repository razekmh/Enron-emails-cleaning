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

echo $username
echo $password

cypher-shell -u $username -p $password "
MATCH (n)
DETACH DELETE n"

