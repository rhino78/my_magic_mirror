"""a class to return the compliment text of the main page"""
import random
import datetime
from datetime import datetime, timedelta
import string
from os import path
import holidays
import requests
import COVID19Py
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


def compliment():
    """returns a random compliment to display"""
    wisdom = gettips()
    deaths, cases = getcovid()
    stage = getstage()
    summer = getsummer()
    kanye = getkanye()
    quote = getquote()
    yomomma = getyomomma()

    complimentlist = [stage, wisdom, deaths, cases, summer, kanye, quote, yomomma]
    usholidays = getholidays()

    if datetime.now() in usholidays:
        return "Happy " + str(usholidays.get(datetime.now()))

    if datetime.now().hour <= 11:
        return str(complimentlist[random.randint(0, len(complimentlist) - 1)])

    return str(complimentlist[random.randint(0, len(complimentlist) - 1)])

def getyomomma():
    """returns a yo momma joke from a public API """
    results = "yo momma is very fat"
    joke = requests.get('https://yomomma-api.herokuapp.com/jokes')
    if joke.status_code == 200:
        jsonres = joke.json()
        if len(jsonres) >0:
            results = jsonres["joke"]
    return results


def getquote():
    """returns a random quote from this cool api"""
    results = "dad quotes are cool"
    randomquote = requests.get('https://quote-garden.herokuapp.com/api/v3/quotes/random')
    if randomquote.status_code == 200:
        jsonres = randomquote.json()
        if len(jsonres) >0:
            data = jsonres['data']
            results = data[0]['quoteText'] + " -" + data[0]['quoteAuthor']
    return results

def getkanye():
    """returns a random kanye quote from this cool api"""
    results = "kanye is awesome"
    kanye = requests.get('https://api.kanye.rest')
    if kanye.status_code == 200:
        jsonres = kanye.json()
        if len(jsonres) >0:
            results = jsonres['quote'] + " - kanye"
    return results

def getstage():
    """returns a the current coronavirus stage from travis county"""
    results = "travis county is overrun by zombies"
    travisurl = "https://www.traviscountytx.gov/news/2020/1945-novel-coronavirus-covid-19-information#:~:text=Austin%2DTravis%20County%20is%20currently,%2D19%20Risk%2DBased%20Guidelines."
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


def getsummer():
    """returns the countdown to christmas break"""
    if getdelta(2021, 12, 17) > 0:
        return "There are {0} days until christmas break!".format(getdelta(2021, 12, 17))
    return "I love christmas"


def gettips():
    """returns tips of the day from an awesome website"""
    try:
        url = "http://fuckinghomepage.com/"
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.content, "html.parser")
        row = soup.find_all("p")[1:7]
        wisdom = string.capwords(row[1].string)
    except:
        wisdom = "Love your father"
    finally:
        return wisdom


def writenew(cases, historyfile):
    """writes new cases to the file onthe server"""
    with open(historyfile, "w") as fileofhistory:
        datedelta = datetime.now() - timedelta(days=1)
        fileofhistory.write("{0} {1}\n".format(datedelta.strftime("%m%d%Y"), 500))
        fileofhistory.write("{0} {1}\n".format(datetime.now().strftime("%m%d%Y"), cases))


def getdelta(year, month, day):
    """returns the time between today and date in argument"""
    currentdate = datetime.now()
    givendate = datetime(year, month, day)
    converteddate = datetime(currentdate.year, currentdate.month, currentdate.day)
    return (givendate - converteddate).days


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

    #if we don't have data for today
    with open(historyfile, "a") as fileofhistory:
        fileofhistory.write("{0} {1}\n".format(datetime.now().strftime("%m%d%Y"), cases))
        return lines[len(lines) - 1].split()[1]


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
            deaths = "{0:,} People have died from COVID19 in the US yesterday.".format(changedeaths)

    except:
        deaths = "COVID sucks"
        cases = "Wear a mask"
    finally:
        return deaths, cases


def getholidays():
    """if today is a holiday, display that all day"""
    usholidays = holidays.UnitedStates()
    usholidays.append(
        {
            str(datetime.now().year)
            + "-08-29": "Birthday, Ryan! You are the best dad ever!!"
        }
    )
    usholidays.append({str(datetime.now().year) + "-01-03": "Birthday, Carol!"})
    usholidays.append({str(datetime.now().year) + "-09-15": "Birthday, Bella!"})
    usholidays.append({str(datetime.now().year) + "-11-02": "Birthday, Luisa!"})
    usholidays.append({str(datetime.now().year) + "-03-09": "Birthday, Thomas!"})
    usholidays.append({str(datetime.now().year) + "-11-15": "Birthday, Vovo'"})
    usholidays.append({str(datetime.now().year) + "-11-22": "Birthday, Grammie"})
    usholidays.append({str(datetime.now().year) + "-11-29": "Birthday, Grampa"})
    usholidays.append({str(datetime.now().year) + "-11-28": "Birthday, Carlao"})
    usholidays.append({str(datetime.now().year) + "-08-16": "Birthday, Uncle Ryan"})
    usholidays.append({str(datetime.now().year) + "-06-24": "Birthday, Auntie Jenny"})
    usholidays.append({str(datetime.now().year) + "-06-23": "Birthday, Frederico!"})
    usholidays.append({str(datetime.now().year) + "-07-11": "Birthday, Augie"})
    usholidays.append({str(datetime.now().year) + "-04-01": "Birthday, Tio Caio"})
    usholidays.append({str(datetime.now().year) + "-02-09": "Birthday, Tia Carol"})
    usholidays.append({str(datetime.now().year) + "-11-26": "Birthday, Marizilda"})
    usholidays.append({str(datetime.now().year) + "-05-10": "Birthday, Zeca"})
    return usholidays
