"""
a class to handle all the api interfaces
we use this to connect to an external api
all of these functions return a string
TODO: error handling and/or size constraints
I've noticed that at times the text is really large
and makes the screen terrible :\
"""
from os import path
from datetime import datetime, timedelta
import string
import COVID19Py
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def getquotes():
    """returns a list of all the quotes"""
    results = []
    deaths, cases = getcovid()

    results.append(gettips())
    results.append(getstage())
    results.append(getsummer())
    results.append(getkanye())
    results.append(getquote())
    results.append(getyomomma())
    results.append(deaths)
    results.append(cases)
    return results


def getyomomma():
    """returns a yo momma joke from a public API """
    results = "yo momma is very fat"
    joke = requests.get('https://yomomma-api.herokuapp.com/jokes')
    if joke.status_code == 200:
        jsonres = joke.json()
        if len(jsonres) > 0:
            results = jsonres["joke"]
    return results


def getkanye():
    """returns a random kanye quote from this cool api"""
    results = "kanye is awesome"
    kanye = requests.get('https://api.kanye.rest')
    if kanye.status_code == 200:
        jsonres = kanye.json()
        if len(jsonres) > 0:
            results = jsonres['quote'] + " - kanye"
    return results


def getquote():
    """returns a random quote from this cool api"""
    results = "dad quotes are cool"
    randomquote = requests.get(
        'https://quote-garden.herokuapp.com/api/v3/quotes/random')
    if randomquote.status_code == 200:
        jsonres = randomquote.json()
        if len(jsonres) > 0:
            data = jsonres['data']
            results = data[0]['quoteText'] + " -" + data[0]['quoteAuthor']
    return results


def getstage():
    """returns a the current coronavirus stage from travis county"""
    results = "travis county is overrun by zombies"
    travisurl = "https://www.traviscountytx.gov/news/2020/1945-novel-coronavirus-covid-19-information"
    # travisurl = "https://www.traviscountytx.gov/news/2020/' \
    #         '1945-novel-coronavirus-covid-19-information#:~:text=' \
    #         'Austin%2DTravis%20County%20is%20currently,%2D19%20Risk%2DBased%20Guidelines."
    request = requests.get(travisurl)
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, 'html.parser')
        stages = soup.findAll('strong')
        current = "currently in Stage"
        for stage in stages:
            thisstage = str(stage)
            if current in thisstage:
                longtext = thisstage
                longtext = longtext.replace('<strong>', '')
                results = longtext.split(".")
        return results[0]
    return results


def getsummer():
    """returns the countdown to spring break"""
    if getdelta(2022, 5, 26) > 0:
        return "There are {0} days until summer break!".format(getdelta(2022, 5, 26))
    return "I love christmas"


def getdelta(year, month, day):
    """returns the time between today and date in argument"""
    currentdate = datetime.now()
    givendate = datetime(year, month, day)
    converteddate = datetime(
        currentdate.year, currentdate.month, currentdate.day)
    return (givendate - converteddate).days


def gettips():
    """returns tips of the day from an awesome website"""
    results = "Love your father"
    url = "http://fuckinghomepage.com/"
    urllib3.disable_warnings()
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        row = soup.find_all("p")[1:7]
        results = string.capwords(row[1].string)
    return results


def getcovid():
    """get the count of covid cases and deaths to display"""
    try:
        covid = COVID19Py.COVID19()
        location = covid.getLocationByCountryCode("US")
        deaths = location[0]['latest']['deaths']
        cases = location[0]['latest']['confirmed']
        prevdeaths = getprev(deaths, '/home/pi/my_magic_mirror/coviddeaths')
        prevcases = getprev(cases, '/home/pi/my_magic_mirror/covidhistory')
        delta = int(cases) - int(prevcases)
        changedeaths = int(deaths) - int(prevdeaths)

        if delta > 0:
            cases = "{0:,} new people got covid yesterday.".format(delta)

        if delta > 0:
            deaths = "{0:,} People have died from COVID19 in the US yesterday.".format(
                changedeaths)

    except:
        deaths = "COVID sucks"
        cases = "Wear a mask"
    finally:
        return deaths, cases


def writenew(cases, historyfile):
    """writes new cases to the file onthe server"""
    with open(historyfile, "w") as fileofhistory:
        datedelta = datetime.now() - timedelta(days=1)
        fileofhistory.write(
            "{0} {1}\n".format(datedelta.strftime("%m%d%Y"), 500))
        fileofhistory.write(
            "{0} {1}\n".format(datetime.now().strftime("%m%d%Y"), cases))


def getprev(cases, historyfile):
    """returns the count of the cases from the previous day"""
    if not path.exists(historyfile):
        writenew(cases, historyfile)

    with open(historyfile) as fileofhistory:
        lines = fileofhistory.read().splitlines()

    # expecting mmddyyyy 1111111 format
    # we have data for today
    if lines[len(lines) - 1].split()[0] == datetime.now().strftime("%m%d%Y"):
        return lines[len(lines) - 2].split()[1]

    # if we don't have data for today
    with open(historyfile, "a") as fileofhistory:
        fileofhistory.write(
            "{0} {1}\n".format(datetime.now().strftime("%m%d%Y"), cases))
        return lines[len(lines) - 1].split()[1]
