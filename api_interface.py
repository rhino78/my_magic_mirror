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
    results = []
    results.append(gettips())
    results.append(getsummer())

    DO_NOT_CARE_LIST = [Default.kanye, Default.dad, Default.father]

    filtered_results = [word for word in results if len(word) < 150]

    for f in filtered_results:
        if f in str(DO_NOT_CARE_LIST):
            filtered_results.remove(f)

    return filtered_results


def getsummer():
    """returns the countdown to winter break"""
    if getdelta(2024, 1, 4) > 0:
        return "There are {0} days until winter break is over!".format(
            getdelta(2024, 1, 4)
        )
    return "Hello Handsome"


def getdelta(year, month, day):
    """returns the time between today and date in argument"""
    currentdate = datetime.now()
    givendate = datetime(year, month, day)
    converteddate = datetime(currentdate.year, currentdate.month, currentdate.day)
    return (givendate - converteddate).days


def gettips():
    """returns tips of the day from an awesome website"""
    results = str(Default.father)
    url = "http://fuckinghomepage.com/"
    urllib3.disable_warnings()
    response = requests.get(url, verify=False)

    if response.status_code != 200:
        logging.error("got an error getting the homepage: {}", response.status_code)
        return results

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        row = soup.find_all("p")[1:7]
        results = string.capwords(row[1].string)
    return results
