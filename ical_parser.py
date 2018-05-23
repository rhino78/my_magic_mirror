from icalendar import Calendar, Event
import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser
import calendar
import pytz
from pytz import timezone

def ical_parser(cal):
        utc = pytz.UTC
        entries = []
        for event in cal.walk('vevent'):
            if (event.get('summary') != None):
                event_info = {}
                if (event.get('rrule')):
                    if('Until' in event.get('rrule')):
                        trydate = str(event.get('rrule')['Until'][0])
                        dt = parser.parse(trydate[:19])
                        ev_date = event.get('dtstart').dt

                        if datetime.datetime.today() < dt:
                            if event.get('rrule')['FREQ'][0] == "DAILY":
                                dt = utc.localize(dt)
                                while(ev_date < dt):
                                    d = datetime.timedelta(days=1)
                                    ev_date = ev_date +d
                                    event_info = {}
                                    event_info['summary'] = event.get('summary')
                                    event_info['date'] = str(ev_date)
                                    entries.append(event_info)

                            elif event.get('rrule')['FREQ'][0] == "WEEKLY":
                                dt = utc.localize(dt)
                                while(ev_date < dt):
                                    d = datetime.timedelta(days=7)
                                    ev_date = ev_date +d
                                    event_info = {}
                                    event_info['summary'] = event.get('summary')
                                    event_info['date'] = str(ev_date)
                                    entries.append(event_info)

                            elif event.get('rrule')['FREQ'][0] == "MONTHLY":
                                dt = utc.localize(dt)
                                while(ev_date < dt):
                                    ev_date = ev_date +relativedelta(months=+1)
                                    event_info = {}
                                    event_info['summary'] = event.get('summary')
                                    event_info['date'] = str(ev_date)
                                    entries.append(event_info)

                            elif event.get('rrule')['FREQ'][0] == "YEARLY":
                                dt = utc.localize(dt)
                                while(ev_date < dt):
                                    d = datetime.timedelta(days=365)
                                    ev_date = ev_date +d
                                    event_info = {}
                                    event_info['summary'] = event.get('summary')
                                    event_info['date'] = str(ev_date)
                                    entries.append(event_info)

                    else:
                        ev_date = event.get('dtstart').dt
                        if event.get('rrule')['FREQ'][0] == "DAILY":
                            print('Daily for {} until infinity'.format(event.get('summary')))
                            #TODO
                        elif event.get('rrule')['FREQ'][0] == "WEEKLY":
                            print('weekly for {} until infinity'.format(event.get('summary')))
                            #TODO
                        elif event.get('rrule')['FREQ'][0] == "MONTHLY":
                            #just adding three months for now
                            for x in range(0,3):
                                d = datetime.timedelta(days=30)
                                ev_date = ev_date +d
                                event_info = {}
                                event_info['summary'] = event.get('summary')
                                event_info['date'] = str(ev_date)
                                entries.append(event_info)

                        elif event.get('rrule')['FREQ'][0] == "YEARLY":
                            #lets add ten years
                            for x in range(0,10):
                                d = datetime.timedelta(days=365)
                                ev_date = ev_date +d
                                event_info = {}
                                event_info['summary'] = event.get('summary')
                                event_info['date'] = str(ev_date)
                                entries.append(event_info)

                else:
                    event_info = {}
                    event_info['summary'] = event.get('summary')
                    event_info['date'] = str(event.get('dtstart').dt)
                    entries.append(event_info)

        return entries
