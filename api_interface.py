"""
a class to handle all the api interfaces
we use this to connect to an external api
all of these functions return a string
"""
# from os import path
from datetime import datetime  # , timedelta
import string
import random
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
    logging.basicConfig(filename='unittest.log',
                        encoding='utf-8', level=logging.ERROR)
    results = []
    results.append(gettips())
    results.append(getsummer())
    results.append(getstockquotes())
    results.append(getconfuciousquotes())
    results.append(getquote())

    DO_NOT_CARE_LIST = [Default.kanye, Default.dad, Default.father]

    filtered_results = [word for word in results if len(word) < 150]

    for f in filtered_results:
        if f in str(DO_NOT_CARE_LIST):
            filtered_results.remove(f)

    return filtered_results

def getconfuciousquotes():
    """some cool confucious quotes"""
    results = [
        "Everything has beauty, but not everyone sees it. -Confucius",
        "They must often change who would be constant in happiness or wisdom. -Confucius",
        "What the superior man seeks is in himself; what the small man seeks is in others. -Confucius",
        "In a country well governed, poverty is something to be ashamed of. In a country badly governed, wealth is something to be ashamed of. -Confucius",
        "It does not matter how slowly you go so long as you do not stop. -Confucius",
        "When anger rises, think of the consequences. -Confucius",
        "When it is obvious that the goals cannot be reached, don't adjust the goals; adjust the action steps. -Confucius",
        "Faced with what is right, to leave it undone shows a lack of courage. -Confucius",
        "To be able under all circumstances to practice five things constitutes perfect virtue; these five things are gravity, generosity of soul, sincerity, earnestness, and kindness. -Confucius",
        "To see what is right, and not to do it, is want of courage or of principle. -Confucius",
        "Fine words and an insinuating appearance are seldom associated with true virtue. -Confucius",
        "Before you embark on a journey of revenge, dig two graves. -Confucius",
        "Success depends upon previous preparation, and without such preparation, there is sure to be failure. -Confucius",
        "Do not impose on others what you yourself do not desire. -Confucius",
        "Men's natures are alike, it is their habits that carry them far apart. -Confucius",
        "Our greatest glory is not in never falling, but in rising every time we fall. -Confucius",
        "Real knowledge is to know the extent of one's ignorance. -Confucius",
        "Hold faithfulness and sincerity as first principles. -Confucius",
        "I hear and I forget. I see and I remember. I do and I understand. -Confucius",
        "Respect yourself and others will respect you. -Confucius",
        "Silence is a true friend who never betrays. -Confucius",
        "The superior man, when resting in safety, does not forget that danger may come. When in a state of security he does not forget the possibility of ruin. When all is orderly, he does not forget that disorder may come. Thus his person is not endangered, and his States and all their clans are preserved. -Confucius",
        "The will to win, the desire to succeed, the urge to reach your full potential... these are the keys that will unlock the door to personal excellence. -Confucius",
        "Better a diamond with a flaw than a pebble without. -Confucius",
        "Study the past if you would define the future. -Confucius",
        "Wheresoever you go, go with all your heart. -Confucius",
        "Wisdom, compassion, and courage are the three universally recognized moral qualities of men. -Confucius",
        "Forget injuries, never forget kindnesses. -Confucius",
        "Have no friends not equal to yourself. -Confucius",
        "He who exercises government by means of his virtue may be compared to the north polar star, which keeps its place and all the stars turn towards it. -Confucius",
        "He who learns but does not think is lost! He who thinks but does not learn is in great danger. -Confucius",
        "He who speaks without modesty will find it difficult to make his words good. -Confucius",
        "Life is really simple, but we insist on making it complicated. -Confucius",
        "A superior man is modest in his speech but exceeds in his actions. -Confucius",
        "Be not ashamed of mistakes and thus make them crimes. -Confucius",
        "The more man meditates upon good thoughts, the better will be his world and the world at large. -Confucius",
        "The superior man understands what is right; the inferior man understands what will sell. -Confucius",
        "By nature, men are nearly alike; by practice, they get to be wide apart. -Confucius",
        "He who will not economize will have to agonize. -Confucius",
        "When we see men of a contrary character, we should turn inwards and examine ourselves. -Confucius",
        "He with whom neither slander that gradually soaks into the mind, nor statements that startle like a wound in the flesh, are successful may be called intelligent indeed. -Confucius",
        "If I am walking with two other men, each of them will serve as my teacher. I will pick out the good points of the one and imitate them, and the bad points of the other and correct them in myself. -Confucius",
        "Choose a job you love, and you will never have to work a day in your life. -Confucius",
        "If you look into your own heart, and you find nothing wrong there, what is there to worry about? What is there to fear?",
        "Ignorance is the night of the mind, but a night without moon and star. -Confucius",
        "It is easy to hate and it is difficult to love. This is how the whole scheme of things works. All good things are difficult to achieve, and bad things are very easy to get. -Confucius",
        "Without feelings of respect, what is there to distinguish men from beasts? -Confucius",
    ]
    return str(results[random.randint(0, len(results) - 1)])

def getstockquotes():
    """some stock quotes from the classic magic mirror"""
    results = [
        "Strive not to be a success, but rather to be of value -Albert Einstein ",
        "The most difficult thing is the decision to act, the rest is merely tenacity -Amelia Earhart ",
        " The best time to plant a tree was 20 years ago. The second best time is now -Chinese Proverb ",
        "Every child is an artist.  The problem is how to remain an artist once he grows up -Pablo Picasso ",
        "There is nothing to writing. All you do is sit down at a typewriter and bleed -Mark Twain ",
        "There is a time when the operation of the machine becomes so odious, makes you so sick at heart, that you can't take part -Mario Savio ",
        "Those who do not move, do not notice their chains -Rosa Luxemburg ",
        "What are thooooooose? -Ryan Shave"
    ]
    return str(results[random.randint(0, len(results) - 1)])

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
    if getdelta(2023, 12, 14) > 0:
        return "There are {0} days until winter break".format(getdelta(2023, 12, 14))
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
