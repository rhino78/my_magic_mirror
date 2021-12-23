from flask import Flask, jsonify, render_template
import xml.etree.ElementTree as ET
from icalendar import Calendar
import datetime
from datetime import datetime
import time
import urllib.request
from operator import itemgetter
import calendar
import ical_parser
import compliments
from dateutil import parser
import pytz

app = Flask(__name__, static_url_path='/static', template_folder='./templates')
app.config['SECRET_KEY'] = 'secret!'
app.config['CURR_TEMPLATE'] = 'index'


def smart_date(date):
    dt = parser.parse(date[:19])
    utc = pytz.UTC
    dt = utc.localize(dt)
    dt_now = utc.localize(datetime.now())
    diff = dt - dt_now

    if (diff.days < 1):
        if(diff.days < 0):  # these are in the past
            return "Today at {}".format(dt.strftime("%I:%M %p"))
        elif(diff.days == 0):  # possible bug here
            if(dt.day - dt_now.day == 1):  # definately tomorrow
                return "Tomorrow at {}".format(dt.strftime("%I:%M %p"))
            else:  # false alarm it's today
                return "Today at {}".format(dt.strftime("%I:%M %p"))
        else:  # get here if the days diff is 0 probably late tomorrow
            if (dt.day - dt_now.day == 1):  # definately tomorrow
                return "Tomorrow at {}".format(dt.strftime("%I:%M %p"))
            else:  # still today
                return "Today at {}".format(dt.strftime("%I:%M %p"))
    elif(diff.days == 1):
        return "{0} at {1}".format(
                calendar.day_name[dt.weekday()], dt.strftime("%I:%M %p"))
    else:
        return "in {0} days".format(diff.days)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_compliment')
def get_compliment():
    return jsonify({'compliment': compliments.compliment()})


@app.route('/get_news_headlines')
def get_news_headlines():
    xml_response = urllib.request.urlopen(
            'http://feeds.bbci.co.uk/news/rss.xml?edition=us').read()
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
        url = 'http://p27-calendars.icloud.com/published/2/sAKB2qXoM7Kj0E4v8n2nzd3naihwmKKZqvpklvflY9V-xB0-vg5pkFqB2dAyd_84'
        ics = urllib.request.urlopen(url).read()
        cal = Calendar.from_ical(ics)
        entries = []
        entries = ical_parser.ical_parser(cal)
        sorted_events = sorted(entries, key=itemgetter('date'))
        # at this point, we don't need entries anymore
        entries = []
        filtered = [i for i in sorted_events if i['date'] >= time.strftime(
            "%Y-%m-%d %H:%M:%S")]
        # now that we have filtered, we don't need sorted anymore either
        sorted_events = []
        final = []
        for f in filtered:
            info = {}
            info['summary'] = f['summary']
            info['date'] = smart_date(f['date'])
            final.append(info)

        return jsonify({'calendar': final})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
