import logging
import time
from operator import itemgetter
import urllib.request
import xml.etree.ElementTree as ET
from flask import Flask, jsonify, render_template
from icalendar import Calendar
import compliments
import ical_parser
import weather

app = Flask(__name__, static_url_path="/static", template_folder="./templates")
app.config["SECRET_KEY"] = "secret!"
app.config["CURR_TEMPLATE"] = "index"

log = logging.getLogger(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_weather")
def get_weather():
    print("getting that weather, bruh")
    return jsonify({"weather": weather.weather()})


@app.route("/get_compliment")
def get_compliment():
    return jsonify({"compliment": compliments.compliment()})


@app.route("/get_news_headlines")
def get_news_headlines():
    xml_response = urllib.request.urlopen(
        "http://feeds.bbci.co.uk/news/rss.xml?edition=us"
    ).read()
    xml_root = ET.fromstring(xml_response)
    results = []

    for item in xml_root[0].findall("item"):
        item_info = {}
        item_info["title"] = item[0].text
        item_info["description"] = item[1].text
        results.append(item_info)

    return jsonify({"headlines": results})


@app.route("/get_calendar")
def get_calendar():
    url = "http://p27-calendars.icloud.com/published/2/sAKB2qXoM7Kj0E4v8n2nzd3naihwmKKZqvpklvflY9V-xB0-vg5pkFqB2dAyd_84"
    ics = urllib.request.urlopen(url).read()
    cal = Calendar.from_ical(ics)
    entries = []
    entries = ical_parser.ical_parser(cal)
    sorted_events = sorted(entries, key=itemgetter("date"))
    # at this point, we don't need entries anymore
    entries = []
    filtered = [
        i for i in sorted_events if i["date"] >= time.strftime("%Y-%m-%d %H:%M:%S")
    ][:25]
    # now that we have filtered, we don't need sorted anymore either
    sorted_events = []
    final = []

    for f in filtered:
        info = {}
        info["summary"] = f["summary"]
        info["date"] = ical_parser.smart_date(f["date"])
        final.append(info)

    return jsonify({"calendar": final})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

