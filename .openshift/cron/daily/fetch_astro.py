__author__ = 'tneier'

apikey = '13ee97bbedb6e8b1'
pws = 'pws:KCASANTA276'
synodic_month = 29.530588853

import urllib2
import simplejson as json
import sys
import pytz
from datetime import datetime, timedelta
import MySQLdb
import os
# import time
today = pytz.utc.localize(datetime.today())


def main():
    global today
    if len(sys.argv) == 2:
        date = (sys.argv[1])
        if len(date) == 8:
            date = sys.argv[1]
        else:
            print "you must specify the full date in YEARMODA format"
    else:
        date = today.strftime('%Y%m%d')
        
    db = MySQLdb.connect(host=os.environ['OPENSHIFT_MYSQL_DB_HOST'],
                         port=int(os.environ['OPENSHIFT_MYSQL_DB_PORT']),
                         user=os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
                         passwd=os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
                         db="weather")
    process_astro(date, db)
    db.close()


def process_astro(date, db):
    parsed_json = get_astro(date)
    save_weather_database(parsed_json, db)
    print date


def get_astro( datestr ):
    global apikey, pws
    url_to_open = "http://api.wunderground.com/api/" + apikey + "/astronomy/q/CA/Santa_Cruz.json"
    f = urllib2.urlopen(url_to_open)

    json_string = f.read()
    f.close()
    return json.loads(json_string)


def save_weather_database(parsed_json, db):
    dquery = build_daily_insert(parsed_json)
    cursor = db.cursor()
    try:
        cursor.execute(dquery)
        db.commit()
    except:
        db.rollback()


def build_daily_insert(daily):
    global today
    global synodic_month
    moon_phase = str(round(int(daily['moon_phase']['ageOfMoon']) % synodic_month, 2))
    query = "INSERT INTO astro VALUES (NULL," + \
            "STR_TO_DATE('" + today.strftime('%Y%m%d') + "', '%Y%m%d')," + \
            daily['sun_phase']['sunrise']['hour'] + ":" + daily['sun_phase']['sunrise']['minute']+":00," + \
            daily['sun_phase']['sunset']['hour'] + ":" + daily['sun_phase']['sunset']['minute']+":00," + \
            daily['moon_phase']['percentIlluminated'] + "," + \
            moon_phase + ");"
    return query


if __name__ == '__main__':
    main()