from datetime import datetime, date, timedelta
from dateutil import parser
import calendar
import pytz
from dateutil.relativedelta import relativedelta


def smart_date(raw_date):
    dt = parser.parse(raw_date[:19])
    dt_now = datetime.now()
    diff = dt - dt_now
    today = date.today()
    tomorrow = today + timedelta(1)

    if today.year == dt.year:
        if today.day == dt.day:
            return "Today at {}".format(dt.strftime("%I:%M %p"))
        elif tomorrow.day == dt.day:
            return "Tomorrow at {}".format(dt.strftime("%I:%M %p"))
        elif diff.days < 7:
            return "{} at {}".format(
                calendar.day_name[dt.weekday()], dt.strftime("%I:%M %p")
            )

    return "in {} days".format(diff.days)


def process_event(summary, ev_date, entries, rule, until):
    print("processing event: {}".format(summary))
    print("processing ev_date: {}".format(ev_date))
    d = timedelta(days=1)
    todays_date = datetime.today()
    uct = pytz.UTC
    localized_start = uct.localize(todays_date)

    if rule == "DAILY":
        d = timedelta(days=1)
    elif rule == "WEEKLY":
        d = timedelta(days=7)
    elif rule == "MONTHLY":
        d = relativedelta(months=+1)
    elif rule == "YEARLY":
        d = timedelta(days=365)

    for _ in range(0, 52):
        # increment the date
        ev_date = ev_date + d

        # if we reach the until date - we don't need to process anymore
        if ev_date > until:
            return

        # we only want to add an entry if its in the future
        if localized_start < ev_date:
            event_info = {}
            event_info["summary"] = summary
            event_info["date"] = str(ev_date)
            entries.append(event_info)


def get_until(count, event_start):
    # we need to loop through the count until we geto the count
    d = timedelta(weeks=count)
    my_date = event_start + d
    uct = pytz.UTC
    return uct.localize(my_date)


def ical_parser(cal):
    entries = []
    todays_date = datetime.today()
    uct = pytz.UTC
    localized_start = uct.localize(todays_date)

    for event in cal.walk("vevent"):
        if event.get("summary") is not None:
            event_start = str(event.get("dtstart").dt)
            # seems dumb but I do this to strip the times off
            # found as bug where we weren't taking in to account the time
            if len(event_start) > 10:
                event_start = datetime.strptime(event_start[:18], "%Y-%m-%d %H:%M:%S")
            else:
                event_start = datetime.strptime(event_start[:10], "%Y-%m-%d")

            event_info = {}
            if event.get("rrule"):
                rule = event.get("rrule")["FREQ"][0]
                ev_date = event.get("dtstart").dt

                if "COUNT" in event.get("rrule"):
                    count = event.get("rrule")["COUNT"][0]
                    process_event(
                        event.get("summary"),
                        ev_date,
                        entries,
                        rule,
                        get_until(count, event_start),
                    )

                if "UNTIL" in event.get("rrule"):
                    until = event.get("rrule")["UNTIL"][0]
                    if until > localized_start:
                        process_event(
                            event.get("summary"), ev_date, entries, rule, until
                        )

            else:
                # here we have single events
                if todays_date < event_start:
                    event_info = {}
                    event_info["summary"] = event.get("summary")
                    event_info["date"] = str(event.get("dtstart").dt)
                    entries.append(event_info)

    return entries
