from flask import Flask, render_template, send_from_directory, jsonify, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
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
import sys
import redis

app = Flask(__name__, static_url_path='/static', template_folder='./')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

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


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')
	

@app.route('/')
def index():
        phones = ["iphone", "android", "blackberry"]
        agent = request.headers.get('User-Agent')
        print(request.headers.get('User-Agent'))

        if any(phone in agent.lower() for phone in phones):
                return render_template('indexM.html')
        else:
                return render_template('index.html')

@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my broadcast event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
        'calendar',
         broadcast=True)

@socketio.on('my compliment event', namespace='/test')
def test_compliment_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my compliment response',
         'compliment',
         broadcast=True)

@socketio.on('my weather event', namespace='/test')
def test_weather_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my weather response',
         'weather',
         broadcast=True)

@socketio.on('my news event', namespace='/test')
def test_news_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my news response',
         'news',
         broadcast=True)



#@socketio.on('join', namespace='/test')
#def join(message):
#    join_room(message['room'])
#    session['receive_count'] = session.get('receive_count', 0) + 1
#    emit('my response',-
  
#         {'data': 'In rooms: ' + ', '.join(rooms()),
#          'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my room event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('my ping', namespace='/test')
def ping_pong():
    emit('my pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my connected response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


@app.route('/<path:path>')
def serve_static(path):
	return send_from_directory('static', path)

@app.route('/get_compliment')
def get_compliment():
		return jsonify({'compliment': compliments.compliment()})



@app.route('/display', methods=['POST'])
def client_broadcast():
    state = request.form['state']

    # here you can store the message under a key in Memcached, Redis or another in-memory cache server

    return jsonify(stored=True)

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
    #app.run(debug=DEBUG, port=PORT, host=HOST)
    #app.run(debug=True, host='0.0.0.0', threaded=True, port=8080)        
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)
    #print(request.headers.get('User-Agent'))


