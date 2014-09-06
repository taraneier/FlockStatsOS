import pytz
from datetime import datetime, timedelta
import os

__author__ = 'tneier'

date = pytz.utc.localize(datetime.today()).strftime('%Y%m%d--%h%m%s')
f = open(os.environ['OPENSHIFT_DATA_DIR'] + '/run_python.log', 'a')
f.write(date)
f.close()