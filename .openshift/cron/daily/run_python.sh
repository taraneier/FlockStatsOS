#!/bin/bash
echo 'bash script is running'
date >> ${OPENSHIFT_DATA_DIR}/ticktock.log
source ~/python/virtenv/bin/activate
python ${OPENSHIFT_REPO_DIR}/.openshift/cron/daily/fetch_weather.py >> ${OPENSHIFT_DATA_DIR}/run_python_daily.log
