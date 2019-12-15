import praw
import random
import datetime
import holidays
from datetime import datetime
import requests
import string
from bs4 import BeautifulSoup

def get_tips():
    try:
        url = "http://fuckinghomepage.com/"
        r = requests.get(url, verify=False)
        soup = BeautifulSoup(r.content, "html.parser")
        str = soup.p.text
        tip = 'if you do your homework, good things will come'
        #now we get the words of wisdom
        row = soup.find_all('p')[1:7]
        wisdom = string.capwords(row[1].string)
    except:
        wisdom = 'Love your father'
    finally:
        return tip, wisdom

def get_delta(year, month, day):
    c = datetime.now()
    b = datetime(year,month,day)
    a = datetime(c.year, c.month, c.day)
    return(b-a).days

def compliment():
    tip, wisdom = get_tips()
    summerbreak = 'there are {0} days until summer break'.format(get_delta(2020, 5, 21))
    springbreak = 'there are {0} days until spring break'.format(get_delta(2020, 3, 13))

    compliment = [tip, wisdom, "you? me? cars 2?", "poo-poo, pee-pee", "bruhhhhh", "what are thooooooooose", summerbreak, springbreak]

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

    if datetime.now() in us:
        return 'Happy ' + str(us.get(datetime.now()))

    if datetime.now().hour <= 11:
        return str(compliment[random.randint(0,len(compliment)-1)]);
    elif 12 <= datetime.now().hour < 17:
        return str(compliment[random.randint(0,len(compliment)-1)]);
    else:
        return str(compliment[random.randint(0,len(compliment)-1)]);
