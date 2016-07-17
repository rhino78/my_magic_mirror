from flask import Flask, render_template, send_from_directory, jsonify, request
import xml.etree.ElementTree as ET
import subprocess
from icalendar import Calendar, Event
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import urllib.request
from operator import itemgetter
import calendar
import ical_parser
import compliments
import trip_destination
from dateutil import parser
import pytz
from pytz import timezone
import random
import json



app = Flask(__name__, static_url_path='/static', template_folder='./')

DEBUG = True
PORT = 8001
HOST = '127.0.0.1'
        

def smart_date(date):
        dt = parser.parse(date[:19])
        utc = pytz.UTC
        dt = utc.localize(dt)
        dt_now = utc.localize(datetime.now())
        diff = dt - dt_now

        if (diff.days < 1):
                if(diff.days < 0): #these are in the past
                        return "Today at {}".format(dt.strftime("%I:%M %p"))
                elif(diff.days ==0): #this could be today or tomorrow depending on the tod
                        if(dt.day - dt_now.day == 1): #definately tomorrow
                                return "Tomorrow at {}".format(dt.strftime("%I:%M %p"))
                        else: #false alarm it's today
                                return "Today at {}".format(dt.strftime("%I:%M %p"))
                else: #get here if the days diff is 0 probably late tomorrow
                        if (dt.day - dt_now.day == 1): #definately tomorrow
                                return "Tomorrow at {}".format(dt.strftime("%I:%M %p"))
                        else: #still today
                                return "Today at {}".format(dt.strftime("%I:%M %p"))
        elif(diff.days == 1):
                return "{0} at {1}".format(calendar.day_name[dt.weekday()], dt.strftime("%I:%M %p"))
        else:
                return "in {0} days".format(diff.days)
        

@app.route('/')
def index():
        print(request.headers.get('User-Agent'))
        agent = request.headers.get('User-Agent')
        phones = ["iphone", "android"]

        if any(phone in agent.lower() for phone in phones):
                return render_template('index_mobile.html')
        else:
                return render_template('index.html')

@app.route('/<path:path>')
def serve_static(path):
        return send_from_directory('static', path)

@app.route('/get_compliment')
def get_compliment():
                return jsonify({'compliment': compliments.compliment()})

@app.route('/get_trip/destination/<string:destination>')
def get_trip(destination):
        bingMapsKey = "AmlfKIzq70f2tVvlqiTm66fxARmbGTUjl0oF9IDkERG41alTKwjkI2FA9Gt5BK79"
        origin = urllib.parse.quote('Round Rock, tx', safe='')
        dest = urllib.parse.quote(destination, safe='')
        url = 'http://dev.virtualearth.net/REST/V1/Routes?wp.0='+ str(origin)+'&wp.1='+ str(dest) +'&maxSolns=3&key=' + bingMapsKey
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        r = response.read().decode(encoding="utf-8")
        result = json.loads(r)
        itineraryItems = result["resourceSets"][0]["resources"][0]["routeLegs"][0]["itineraryItems"]
        duration = 0
        for i in itineraryItems:
                duration += i["travelDuration"]

        total_duration = trip_destination.trip_destination(duration)
        return jsonify({'trip': "travel time to {0}: {1}".format(destination, total_duration)})

@app.route('/get_news_headlines')
def get_news_headlines():
        xml_response = urllib.request.urlopen('http://feeds.bbci.co.uk/news/rss.xml?edition=us').read()
        xml_root = ET.fromstring(xml_response)
        results = []

        for item in xml_root[0].findall('item'):
                item_info = {}
                item_info['title'] = item[0].text
                item_info['description'] = item[1].text
                results.append(item_info)       

        return jsonify({'headlines': results})

@app.route('/get_calendar')
def get_calendar():
        url = 'http://p04-calendarws.icloud.com/ca/subscribe/1/H40m2cOJve9rWlCvSNhNKLL1XJs1U4XH96G1PqW2Zf9Ihvwm-q9hgdIMqj_LeOrB'
        ics = urllib.request.urlopen(url).read()
        cal = Calendar.from_ical(ics)
        entries = []

        entries = ical_parser.ical_parser(cal);

        sorted_events = sorted(entries, key=itemgetter('date'))
        filtered = [i for i in sorted_events if i['date'] >= time.strftime("%Y-%m-%d %H:%M:%S")]

        final =[]
        for f in filtered:
                info = {}
                info['summary'] = f['summary']
                info['date'] = smart_date(f['date'])
                final.append(info)


        return jsonify({'calendar': final})
        

if __name__ == '__main__':      
        #app.run(debug=DEBUG, port=PORT, host=HOST, ssl_context=('/usr/certificates/server.crt', '/usr/certificates/server.key'))
        app.run(debug=True, host='0.0.0.0')
