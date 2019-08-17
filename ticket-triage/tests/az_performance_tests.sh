#! /bin/bash

A=43

curl -H "Content-Type: application/json" -X POST -d '[{"ticket_id":31, "summary": "test summary - (ignored)", "description": "$A - Hey there it looks like that our moodle instance ia not working properly, and it seems that the database is down. Could you please look into it?"}]' http://localhost:7071/api/ticket_classifier
