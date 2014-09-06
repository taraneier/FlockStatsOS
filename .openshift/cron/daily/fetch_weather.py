__author__ = 'tneier'

apikey = '13ee97bbedb6e8b1'
pws = 'pws:KCASANTA276'

import urllib2
import simplejson as json
import sys
import pytz
from datetime import datetime, timedelta
import MySQLdb
import os
# import time



def main():
    if len(sys.argv) == 2:
        date = (sys.argv[1])
        if len(date) == 8:
            date = sys.argv[1]
        else:
            print "you must specify the full date in YEARMODA format"
    else:
        yesterday = pytz.utc.localize(datetime.today() - timedelta(1))
        date = yesterday.strftime('%Y%m%d')

    db = MySQLdb.connect(host=int(os.environ['OPENSHIFT_MYSQL_DB_HOST']),
                         port=int(os.environ['OPENSHIFT_MYSQL_DB_PORT']),
                         user="'" + os.environ['OPENSHIFT_MYSQL_DB_USERNAME'] + "'",
                         passwd="'" + os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'] + "'",
                         db="weather")
    process_weather(date, db)

# def main():
#     daysback = 170;
#     db = MySQLdb.connect(host="127.0.0.1", port=8889, user=os.environ['LOCAL_MYSQL_DB_USER'], passwd=os.environ['LOCAL_MYSQL_DB_PASSWORD'], db="weather")
#     while(daysback > 0):
#         date = pytz.utc.localize(datetime.today() - timedelta(daysback)).strftime('%Y%m%d')
#         print date
#         process_weather(date, db)
#         daysback = daysback - 1
#         time.sleep(10)
#     print "done"

def process_weather(date, db):
    parsed_json = get_weather(date)
    save_weather_database(parsed_json, db)


def get_weather( datestr ):
    global apikey, pws
    url_to_open = "http://api.wunderground.com/api/" + apikey + "/history_" + datestr + "/q/" + pws + ".json"
    f = urllib2.urlopen(url_to_open)

    # f = open('/Users/tneier/Desktop/20140801.json', 'r')


    json_string = f.read()
    f.close()
    return json.loads(json_string)


def save_weather_database(parsed_json, db):
    dquery = build_daily_insert(parsed_json['history']['dailysummary'][0])
    cursor = db.cursor()
    try:
        cursor.execute(dquery)
        db.commit()
    except:
        db.rollback()

    # print dquery

    for reading in parsed_json['history']['observations']:
        query = build_observation_insert(reading)
        try:
            cursor.execute(query)
            db.commit()
        except:
            db.rollback()
        # print query

    # return datestr


def build_daily_insert(daily):

    query = "INSERT INTO dailysummary VALUES (NULL," + \
            "STR_TO_DATE('" + daily['date']['pretty'] + "', '%M %d,%Y')," + \
            daily['meantempm'] + ',' + \
            daily['meantempi'] + ',' + \
            daily['meandewptm'] + ',' + \
            daily['meandewpti'] + ',' + \
            daily['meanwindspdm'] + ',' + \
            daily['meanwindspdi'] + ',' + \
            "'" + daily['meanwdire'] + "'" + ',' + \
            "'" + daily['meanwdird'] + "'" + ',' + \
            daily['humidity'] + ',' + \
            daily['maxtempm'] + ',' + \
            daily['maxtempi'] + ',' + \
            daily['mintempm'] + ',' + \
            daily['mintempi'] + ',' + \
            daily['maxhumidity'] + ',' + \
            daily['minhumidity'] + ',' + \
            daily['maxdewptm'] + ',' + \
            daily['maxdewpti'] + ',' + \
            daily['mindewptm'] + ',' + \
            daily['mindewpti'] + ',' + \
            daily['maxpressurem'] + ',' + \
            daily['maxpressurei'] + ',' + \
            daily['minpressurem'] + ',' + \
            daily['minpressurei'] + ',' + \
            daily['maxwspdm'] + ',' + \
            daily['maxwspdi'] + ',' + \
            daily['precipm'] + ',' + \
            daily['precipi'] + \
            ')'
    return query


def build_observation_insert(reading):
    query = "INSERT INTO observation VALUES(NULL," + \
            "STR_TO_DATE('" + reading['date']['pretty'] + "', '%h:%i %p PDT on %M %d,%Y')," + \
            reading['tempm'] + ',' + \
            reading['tempi'] + ',' + \
            reading['dewptm'] + ',' + \
            reading['dewpti'] + ',' + \
            reading['hum'] + ',' + \
            reading['wspdm'] + ',' + \
            reading['wspdi'] + ',' + \
            reading['wgustm'] + ',' + \
            reading['wgusti'] + ',' + \
            reading['pressurem'] + ',' + \
            reading['pressurei'] + ',' + \
            reading['windchillm'] + ',' + \
            reading['windchilli'] + ',' + \
            reading['heatindexm'] + ',' + \
            reading['heatindexi'] + ',' + \
            reading['precip_ratem'] + ',' + \
            reading['precip_ratei'] + ',' + \
            reading['precip_totalm'] + ',' + \
            reading['precip_totali'] + ',"' + \
            reading['solarradiation'] + '","' + \
            reading['UV'] + '"' + \
            ")"
    return query

if __name__ == '__main__':
    main()