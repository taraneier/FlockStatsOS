import pytz
from datetime import datetime, timedelta

__author__ = 'tneier'

date = pytz.utc.localize(datetime.today()).strftime('%Y%m%d--%h%m%s')
f = open('${OPENSHIFT_DATA_DIR}/crontest.log', 'a')
f.write(date)
f.close()