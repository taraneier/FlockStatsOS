#!/bin/bash
mkdir -p ${OPENSHIFT_DATA_DIR}/weekly
dbs=`mysql -h ${OPENSHIFT_MYSQL_DB_HOST} -u ${OPENSHIFT_MYSQL_DB_USERNAME} -p${OPENSHIFT_MYSQL_DB_PASSWORD} -e 'show databases' -B | sed /Database/d | sed /information_schema/d | sed /mysql/d | sed /performance_schema/d`
for db in $dbs
do
    BACKUP_NAME=$(date +'%Y_%m_%d')_${OPENSHIFT_NAMESPACE}_${OPENSHIFT_GEAR_NAME}_$db
    mysqldump --password=${OPENSHIFT_MYSQL_DB_PASSWORD} -u ${OPENSHIFT_MYSQL_DB_USERNAME} -h ${OPENSHIFT_MYSQL_DB_HOST} -P ${OPENSHIFT_MYSQL_DB_PORT} $db | gzip > ${OPENSHIFT_DATA_DIR}/weekly/${BACKUP_NAME}.sql.gz
done
find ${OPENSHIFT_DATA_DIR}/weekly/*.sql.gz -type f -mtime +8 -delete