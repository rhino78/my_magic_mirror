import datetime
import pytz
from dateutil.relativedelta import relativedelta


def process_event(summary, ev_date, entries, rule, until):
    d = datetime.timedelta(days=1)
    todays_date = datetime.datetime.today()
    uct = pytz.UTC
    localized_start = uct.localize(todays_date)

    if rule == "DAILY":
        d = datetime.timedelta(days=1)
    elif rule == "WEEKLY":
        d = datetime.timedelta(days=7)
    elif rule == "MONTHLY":
        d = relativedelta(months=+1)
    elif rule == "YEARLY":
        d = datetime.timedelta(days=365)

    for _ in range(0, 52):
        # increment the date
        ev_date = ev_date + d

        # if we reach the until date - we don't need to process anymore
        if ev_date > until:
            return

        # we only want to add an entry if its in the future
        if localized_start < ev_date:
            event_info = {}
            event_info['summary'] = summary
            event_info['date'] = str(ev_date)
            entries.append(event_info)


def ical_parser(cal):
    entries = []
    todays_date = datetime.datetime.today()

    for event in cal.walk('vevent'):
        if (event.get('summary') is not None):
            event_start = str(event.get('dtstart').dt)
            event_start = datetime.datetime.strptime(
                event_start[:10], '%Y-%m-%d')
            event_info = {}
            if (event.get('rrule')):
                rule = event.get('rrule')['FREQ'][0]
                ev_date = event.get('dtstart').dt

                if 'UNTIL' in event.get('rrule'):
                    until = event.get('rrule')['UNTIL'][0]

                    uct = pytz.UTC
                    localized_start = uct.localize(todays_date)

                    if until > localized_start:
                        process_event(event.get('summary'),
                                      ev_date, entries, rule, until)

            else:
                # here we have single events
                if todays_date < event_start:
                    event_info = {}
                    event_info['summary'] = event.get('summary')
                    event_info['date'] = str(event.get('dtstart').dt)
                    entries.append(event_info)

    return entries
