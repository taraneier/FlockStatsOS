#!/bin/bash
dbs=`mysql -h ${OPENSHIFT_MYSQL_DB_HOST} -u ${OPENSHIFT_MYSQL_DB_USERNAME} -p${OPENSHIFT_MYSQL_DB_PASSWORD} -e 'show databases' -B | sed /Database/d | sed /information_schema/d`
for db in $dbs
do
    BACKUP_NAME=$(date +'%Y_%m_%d')_${OPENSHIFT_NAMESPACE}_${OPENSHIFT_GEAR_NAME}_$db
    mysqldump --password=${OPENSHIFT_MYSQL_DB_PASSWORD} -u ${OPENSHIFT_MYSQL_DB_USERNAME} -h ${OPENSHIFT_MYSQL_DB_HOST} -P ${OPENSHIFT_MYSQL_DB_PORT} ${OPENSHIFT_GEAR_NAME} | gzip > ${OPENSHIFT_DATA_DIR}/${BACKUP_NAME}.sql.gz
done
find ${OPENSHIFT_DATA_DIR}/*.sql.gz -type f -mtime +5 -delete