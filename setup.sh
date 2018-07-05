#!/bin/bash
docker stack deploy -c stack.yml  simpleflaskapp
echo 'waiting to setup the cluster'
sleep 30
mongo_instance=$(docker ps --format "{{.Names}}" | grep mongo)
docker exec -it $mongo_instance bash -c '/usr/bin/mongoimport --db testdb  -c songs /dumpfile/songs.json'
echo 'The application has been deployed successfully, you can access the application using the url http://0.0.0.0:5000/songs'
