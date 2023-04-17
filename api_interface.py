"""
a class to handle all the api interfaces
we use this to connect to an external api
all of these functions return a string
"""
# from os import path
from datetime import datetime  # , timedelta
import string
import logging
import enum
# import COVID19Py
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Default(enum.Enum):
    kanye = "kanye is awesome"
    dad = "dad quotes are cool"
    father = "love your father"


def getquotes():
    """returns a list of all the quotes"""
    logging.basicConfig(filename='unittest.log',
                        encoding='utf-8', level=logging.ERROR)
    results = []
    results.append(gettips())
    results.append(getsummer())
    results.append(getkanye())
    results.append(getquote())

    DO_NOT_CARE_LIST = [Default.kanye, Default.dad, Default.father]

    filtered_results = [word for word in results if len(word) < 150]
    for f in filtered_results:
        if f in str(DO_NOT_CARE_LIST):
            filtered_results.remove(f)

    return filtered_results


def getkanye():
    """returns a random kanye quote from this cool api"""
    results = str(Default.kanye)
    kanye = requests.get('https://api.kanye.rest')

    if kanye.status_code != 200:
        logging.error(
            'could not get a kanye quote: {}'.format(kanye.status_code))
        return results

    if kanye.status_code == 200:
        jsonres = kanye.json()
        if len(jsonres) > 0:
            results = jsonres['quote'] + " - kanye"
    return results


def getquote():
    """returns a random quote from this cool api"""
    results = str(Default.dad)
    randomquote = requests.get(
        'https://quote-garden.herokuapp.com/api/v3/quotes/random')

    if randomquote.status_code != 200:
        logging.error('got an error getting a random quote: {}'.format(
            randomquote.status_code))
        return results

    if randomquote.status_code == 200:
        jsonres = randomquote.json()
        if len(jsonres) > 0:
            data = jsonres['data']
            results = data[0]['quoteText'] + " -" + data[0]['quoteAuthor']

    return results


def getsummer():
    """returns the countdown to summer break"""
    if getdelta(2023, 5, 25) > 0:
        return "There are {0} days until summer break starts!!".format(getdelta(2023, 5, 25))
    return "Hello Handsome"


def getdelta(year, month, day):
    """returns the time between today and date in argument"""
    currentdate = datetime.now()
    givendate = datetime(year, month, day)
    converteddate = datetime(
        currentdate.year, currentdate.month, currentdate.day)
    return (givendate - converteddate).days


def gettips():
    """returns tips of the day from an awesome website"""
    results = str(Default.father)
    url = "http://fuckinghomepage.com/"
    urllib3.disable_warnings()
    response = requests.get(url, verify=False)

    if response.status_code != 200:
        logging.error('got an error getting the homepage: {}',
                      response.status_code)
        return results

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        row = soup.find_all("p")[1:7]
        results = string.capwords(row[1].string)
    return results
