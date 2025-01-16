#!/bin/bash


#creating the admin user, the values will be readed from the docker-compose.yml
superset fab create-admin --username "$ADMIN_USERNAME" --firstname Superset --lastname User --email "$ADMIN_EMAIl" --password "$ADMIN_PASSWORD"


#Upgrading Superset metastore
superset db upgrade

# setup roles and permissions
superset superset init

#Starting the server
/bin/sh -c /usr/bin/run-server.sh

