import praw
import random
import datetime
import holidays
from datetime import datetime, timedelta
import requests
import string
from os import path
import COVID19Py
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

def compliment():
    wisdom = getTips()
    deaths, cases = getCovid()
    compliment = [wisdom, deaths, cases ]
    us = getHolidays()

    if datetime.now() in us:
        return 'Happy ' + str(us.get(datetime.now()))

    if datetime.now().hour <= 11:
        return str(compliment[random.randint(0,len(compliment)-1)]);
    elif 12 <= datetime.now().hour < 17:
        return str(compliment[random.randint(0,len(compliment)-1)]);
    else:
        return str(compliment[random.randint(0,len(compliment)-1)]);

def getTips():
    try:
        url = "http://fuckinghomepage.com/"
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        r = requests.get(url, verify=False)
        soup = BeautifulSoup(r.content, "html.parser")
        str = soup.p.text
        #now we get the words of wisdom
        #adding a note here

        row = soup.find_all('p')[1:7]
        wisdom = string.capwords(row[1].string)
    except:
        wisdom = 'Love your father'
    finally:
        return wisdom

def writeNew(cases, historyfile):
    with open(historyfile, "w") as f:
        d  = datetime.now()-timedelta(days=1)
        f.write("{0} {1}\n".format(d.strftime("%m%d%Y"),500))
        f.write("{0} {1}\n".format(datetime.now().strftime("%m%d%Y"),cases))

def getDelta(year, month, day):
    c = datetime.now()
    b = datetime(year,month,day)
    a = datetime(c.year, c.month, c.day)
    return(b-a).days

def getPrev(cases, historyfile):
    if not path.exists(historyfile):
        writeNew(cases, historyfile)

    with open(historyfile) as f:
        lines = f.read().splitlines()

    # expecting mmddyyyy 1111111 format
    # we have data for today
    if lines[len(lines)-1].split()[0] == datetime.now().strftime("%m%d%Y"):
        return lines[len(lines)-2].split()[1]
    else:
        with open(historyfile, "a") as f:
            f.write("{0} {1}\n".format(datetime.now().strftime("%m%d%Y"), cases))

        return lines[len(lines)-1].split()[1]


def getCovid():
    try:
        covid = COVID19Py.COVID19(url="https://cvtapi.nl")
        location = covid.getLocationByCountryCode("US")
        deaths = location[0]['latest']['deaths']
        cases = location[0]['latest']['confirmed']
        # prevDeaths = getPrev(deaths, '/home/pi/my_magic_mirror/coviddeaths')
        delta = int(cases) - int(prevCases)
        changedeaths = int(deaths) - int(prevDeaths)

        if delta > 0:
            cases = "There are currently {0:,} confirmed cases in the US. An increase of {1:,} from yesterday.".format(cases, delta)
        else:
            cases = "There are currently {0:,} confirmed cases in the US. A decrease of {1:,} from yesterday - YAY!".format(cases, delta)

        if delta > 0:
            deaths = "{0:,} People have died from COVID19 in the US :( An increase of {1:,} from yesterday.".format(deaths, changedeaths)
        else:
            deaths = "{0:,} People have died from COVID19 in the US :( An decrease of {1:,} from yesterday. :)".format(deaths, changedeaths)

    except:
        deaths = "COVID sucks"
        cases = "Wear a mask"
    finally:
        return deaths, cases


def getHolidays():
    us = holidays.UnitedStates()
    us.append({str(datetime.now().year) + "-08-29":"Birthday, Ryan! You are the best dad ever!"})
    us.append({str(datetime.now().year) + "-01-03":"Birthday, Carol!"})
    us.append({str(datetime.now().year) + "-09-15":"Birthday, Bella!"})
    us.append({str(datetime.now().year) + "-11-02":"Birthday, Luisa!"})
    us.append({str(datetime.now().year) + "-03-09":"Birthday, Thomas!"})
    us.append({str(datetime.now().year) + "-11-15":"Birthday, Vovo'"})
    us.append({str(datetime.now().year) + "-11-22":"Birthday, Grammie"})
    us.append({str(datetime.now().year) + "-11-29":"Birthday, Grampa"})
    us.append({str(datetime.now().year) + "-11-28":"Birthday, Carlao"})
    us.append({str(datetime.now().year) + "-08-16":"Birthday, Uncle Ryan"})
    us.append({str(datetime.now().year) + "-06-24":"Birthday, Auntie Jenny"})
    us.append({str(datetime.now().year) + "-06-23":"Birthday, Frederico!"})
    us.append({str(datetime.now().year) + "-07-11":"Birthday, Augie"})
    us.append({str(datetime.now().year) + "-04-01":"Birthday, Tio Caio"})
    us.append({str(datetime.now().year) + "-02-09":"Birthday, Tia Carol"})
    us.append({str(datetime.now().year) + "-11-26":"Birthday, Marizilda"})
    us.append({str(datetime.now().year) + "-05-10":"Birthday, Zeca"})
    return us

