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
    results.append(getsummer())

    DO_NOT_CARE_LIST = [Default.dad, Default.father]

    filtered_results = [word for word in results if len(word) < 150]

    for f in filtered_results:
        if f in str(DO_NOT_CARE_LIST):
            filtered_results.remove(f)

    return filtered_results


def getsummer():
    """returns the countdown to school"""
    if getdelta(2024, 12, 19) > 0:
        return "There are {0} days until christmas break!".format(
            getdelta(2024, 12, 19)
        )
    return "Hello Handsome"


def gettips():
    """returns tips of the day from an awesome philosopher"""
    return (
        quotes.QUOTES[random.randint(0, len(quotes.QUOTES) - 1)] + " -Marcus Aurelius"
    )


def getdelta(year, month, day):
    """returns the time between today and date in argument"""
    currentdate = datetime.now()
    givendate = datetime(year, month, day)
    converteddate = datetime(currentdate.year, currentdate.month, currentdate.day)
    return (givendate - converteddate).days
