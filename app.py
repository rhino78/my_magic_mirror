from flask import Flask, render_template, send_from_directory, jsonify
#import urllib2
import urllib.request
import xml.etree.ElementTree as ET
import subprocess
from icalendar import Calendar, Event
from datetime import datetime
import time
import urllib.request
from operator import itemgetter
from dateutil import parser
import calendar
import pytz
from pytz import timezone


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
	return render_template('index.html')

@app.route('/<path:path>')
def serve_static(path):
	return send_from_directory('static', path)

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
        
        for event in cal.walk('vevent'):
                if (event.get('summary') != None):
                        event_info = {}
                        event_info['summary'] = event.get('summary')
                        event_info['date'] = str(event.get('dtstart').dt)
                        entries.append(event_info)

        sorted_events = sorted(entries, key=itemgetter('date'))
        filtered = [i for i in sorted_events if i['date'] >= time.strftime("%Y-%m-%d")]

        final =[]
        for f in filtered:
        	info = {}
        	info['summary'] = f['summary']
        	info['date'] = smart_date(f['date'])
        	final.append(info)


        return jsonify({'calendar': final})
        

if __name__ == '__main__':
	app.run(debug=DEBUG, port=PORT, host=HOST)


