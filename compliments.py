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
    stage = getStage()
    summer = getSummer()

    compliment = [stage, wisdom, deaths, cases, summer]
    us = getHolidays()

    if datetime.now() in us:
        return "Happy " + str(us.get(datetime.now()))

    if datetime.now().hour <= 11:
        return str(compliment[random.randint(0, len(compliment) - 1)])
    elif 12 <= datetime.now().hour < 17:
        return str(compliment[random.randint(0, len(compliment) - 1)])
    else:
        return str(compliment[random.randint(0, len(compliment) - 1)])

def getStage():
    r = requests.get("https://www.traviscountytx.gov/news/2020/1945-novel-coronavirus-covid-19-information#:~:text=Austin%2DTravis%20County%20is%20currently,%2D19%20Risk%2DBased%20Guidelines.")
    soup = BeautifulSoup(r.text, 'html.parser')
    stage = soup.findAll('strong')
    c = "currently in Stage"
    for s in stage:
        foo = str(s)
        if c in foo:
            longtext = foo
            longtext = longtext.replace('<strong>', '')
    results = longtext.split(".")
    return results[0]


def getSummer():
    if getDelta(2021, 12, 17) > 0:
        return "There are {0} days until christmas break!".format(getDelta(2021, 12, 17))


def getTips():
    try:
        url = "http://fuckinghomepage.com/"
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        r = requests.get(url, verify=False)
        soup = BeautifulSoup(r.content, "html.parser")
        str = soup.p.text
        # now we get the words of wisdom
        # adding a note here

        row = soup.find_all("p")[1:7]
        wisdom = string.capwords(row[1].string)
    except:
        wisdom = "Love your father"
    finally:
        return wisdom


def writeNew(cases, historyfile):
    with open(historyfile, "w") as f:
        d = datetime.now() - timedelta(days=1)
        f.write("{0} {1}\n".format(d.strftime("%m%d%Y"), 500))
        f.write("{0} {1}\n".format(datetime.now().strftime("%m%d%Y"), cases))


def getDelta(year, month, day):
    c = datetime.now()
    b = datetime(year, month, day)
    a = datetime(c.year, c.month, c.day)
    return (b - a).days


def getPrev(cases, historyfile):
    if not path.exists(historyfile):
        writeNew(cases, historyfile)

    with open(historyfile) as f:
        lines = f.read().splitlines()

    # expecting mmddyyyy 1111111 format
    # we have data for today
    if lines[len(lines) - 1].split()[0] == datetime.now().strftime("%m%d%Y"):
        return lines[len(lines) - 2].split()[1]
    else:
        with open(historyfile, "a") as f:
            f.write("{0} {1}\n".format(
                datetime.now().strftime("%m%d%Y"), cases))

        return lines[len(lines) - 1].split()[1]


def getCovid():
    try:
        covid = COVID19Py.COVID19()
        location = covid.getLocationByCountryCode("US")
        deaths = location[0]['latest']['deaths']
        cases = location[0]['latest']['confirmed']
        prevDeaths = getPrev(deaths, '/home/pi/my_magic_mirror/coviddeaths')
        prevCases = getPrev(cases, '/home/pi/my_magic_mirror/covidhistory')
        delta = int(cases) - int(prevCases)
        changedeaths = int(deaths) - int(prevDeaths)

        if delta > 0:
            cases = "{0:,} new people got covid yesterday.".format(delta)

        if delta > 0:
            deaths = "{0:,} People have died from COVID19 in the US yesterday.".format(changedeaths)

    except:
        deaths = "COVID sucks"
        cases = "Wear a mask"
    finally:
        return deaths, cases


def getHolidays():
    us = holidays.UnitedStates()
    us.append(
        {
            str(datetime.now().year)
            + "-08-29": "Birthday, Ryan! You are the best dad ever!!"
        }
    )
    us.append({str(datetime.now().year) + "-01-03": "Birthday, Carol!"})
    us.append({str(datetime.now().year) + "-09-15": "Birthday, Bella!"})
    us.append({str(datetime.now().year) + "-11-02": "Birthday, Luisa!"})
    us.append({str(datetime.now().year) + "-03-09": "Birthday, Thomas!"})
    us.append({str(datetime.now().year) + "-11-15": "Birthday, Vovo'"})
    us.append({str(datetime.now().year) + "-11-22": "Birthday, Grammie"})
    us.append({str(datetime.now().year) + "-11-29": "Birthday, Grampa"})
    us.append({str(datetime.now().year) + "-11-28": "Birthday, Carlao"})
    us.append({str(datetime.now().year) + "-08-16": "Birthday, Uncle Ryan"})
    us.append({str(datetime.now().year) + "-06-24": "Birthday, Auntie Jenny"})
    us.append({str(datetime.now().year) + "-06-23": "Birthday, Frederico!"})
    us.append({str(datetime.now().year) + "-07-11": "Birthday, Augie"})
    us.append({str(datetime.now().year) + "-04-01": "Birthday, Tio Caio"})
    us.append({str(datetime.now().year) + "-02-09": "Birthday, Tia Carol"})
    us.append({str(datetime.now().year) + "-11-26": "Birthday, Marizilda"})
    us.append({str(datetime.now().year) + "-05-10": "Birthday, Zeca"})
    return us
