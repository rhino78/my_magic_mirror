import logging
import calendar
import time
import datetime
from datetime import datetime, date, timedelta
from operator import itemgetter
import urllib.request
import xml.etree.ElementTree as ET
from dateutil import parser
from flask import Flask, jsonify, render_template
from icalendar import Calendar
import compliments
import ical_parser


app = Flask(__name__, static_url_path='/static', template_folder='./templates')
app.config['SECRET_KEY'] = 'secret!'
app.config['CURR_TEMPLATE'] = 'index'

log = logging.getLogger(__name__)


def smart_date(raw_date):
    dt = parser.parse(raw_date[:19])
    dt_now = datetime.now()
    diff = dt - dt_now
    today = date.today()
    tomorrow = today + timedelta(1)
    tomorrow_plus_1 = today + timedelta(2)

    if today.year == dt.year:
        if today.day == dt.day:
            return "Today at {}".format(dt.strftime("%I:%M %p"))
        elif tomorrow.day == dt.day:
            return "Tomorrow at {}".format(dt.strftime("%I:%M %p"))
        elif tomorrow_plus_1.day == dt.day:
            return f"{0} at {1}".format(
                calendar.day_name[dt.weekday()], dt.strftime("%I:%M %p"))
        else:
            return "in {} days".format(diff.days)


@ app.route('/')
def index():
    return render_template('index.html')


@ app.route('/get_compliment')
def get_compliment():
    return jsonify({'compliment': compliments.compliment()})


@ app.route('/get_news_headlines')
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


@ app.route('/get_calendar')
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
        "%Y-%m-%d %H:%M:%S")][:25]
    # now that we have filtered, we don't need sorted anymore either
    sorted_events = []
    final = []
    for f in filtered:
        info = {}
        info['summary'] = f['summary']
        bruh = f['summary']
        print(f'working {bruh}')
        info['date'] = smart_date(f['date'])
        final.append(info)

    return jsonify({'calendar': final})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
