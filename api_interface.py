"""
a class to handle all the api interfaces
we use this to connect to an external api
all of these functions return a string
"""

import enum
import random

# from os import path
from datetime import datetime

import urllib3

import quotes

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Default(enum.Enum):
    dad = "dad quotes are cool"
    father = "love your father"


def getquotes():
    """returns a list of all the quotes"""
    results = []
    results.append(gettips())
    results.append(getsummer1())
    results.append(getsummer2())

    DO_NOT_CARE_LIST = [Default.dad, Default.father]

    filtered_results = [word for word in results if len(word) < 150]

    for f in filtered_results:
        if f in str(DO_NOT_CARE_LIST):
            filtered_results.remove(f)

    return filtered_results


def getsummer1():
    """returns the countdown to school"""
    if getdelta(2026, 8, 19) > 0:
        return "There are {0} days until Texas State Begins Class".format(
            getdelta(2026, 8, 19)
        )
    return "Ryan is the best"

def getsummer2():
    """returns the countdown to school"""
    if getdelta(2026, 8, 24) > 0:
        return "There are {0} days until LSU Begins Class".format(
            getdelta(2026, 8, 24)
        )
    return "Ryan is the best"


def gettips():
    """returns tips of the day from an awesome philosopher"""
    return quotes.QUOTES[random.randint(0, len(quotes.QUOTES) - 1)] + " -Nick Saban"


def getdelta(year, month, day):
    """returns the time between today and date in argument"""
    currentdate = datetime.now()
    givendate = datetime(year, month, day)
    converteddate = datetime(currentdate.year, currentdate.month, currentdate.day)
    return (givendate - converteddate).days
