import random
import datetime
import holidays
from datetime import date
import requests
import string
from bs4 import BeautifulSoup

def get_tips():
    try:
        url = "http://fuckinghomepage.com/"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        str = soup.p.text
        str = str[str.index('.')-len(str)+2:]
        tip = string.capwords(str)
        #now we get the words of wisdom
        row = soup.find_all('p')[1:7]
        wisdom = string.capwords(row[1].string)
    except:
        tip = 'if you do your homework, good things will come'
        wisdom = 'Love your father'
    finally:
        return tip, wisdom
    

def get_delta(year, month, day):
    c = datetime.datetime.now()
    b = date(year,month,day)
    a = date(c.year, c.month, c.day)
    return(b-a).days

def compliment():
    currentTime = datetime.datetime.now()
    summerbreak='there are {0} days until summer break'.format(get_delta(2018,5,29))
    
    tip, wisdom = get_tips()

    evening = [summerbreak, tip, wisdom, 'ready for bed?', 'boa noite']
    afternoon = [summerbreak, tip, wisdom, 'Good afternoon', 'boa tarde', 'Am I a cool mirror, or what?']
    morning = [summerbreak, tip, wisdom, 'bom dia', 'buen dia (spanish)', 'Bonjour (French)', 'Buongiorno (Italian)', 'guten Morgen (German)', 'Ohayo (Japanese)','Suprabhat (Hindi)', 'Good morning, beauty', 'Good Morning, Kids!']
    
    us = holidays.UnitedStates()
    us.append({"2018-08-29":"Birthday, Ryan! You are the best dad ever!"})
    us.append({"2018-01-03":"Birthday, Carol!"})
    us.append({"2018-09-15":"Birthday, Bella!"})
    us.append({"2018-11-02":"Birthday, Luisa!"})
    us.append({"2018-03-09":"Birthday, Thomas!"})
    us.append({"2018-11-15":"Birthday, Vovo'"})
    us.append({"2018-11-22":"Birthday, Grammie"})
    us.append({"2018-11-29":"Birthday, Grampa"})
    us.append({"2018-11-28":"Birthday, Carlao"})
    us.append({"2018-08-16":"Birthday, Uncle Ryan"})
    us.append({"2018-06-24":"Birthday, Auntie Jenny"})
    us.append({"2018-06-23":"Birthday,  Frederico!"})
    us.append({"2018-07-11":"Birthday, Augie"})
    us.append({"2018-04-01":"Birthday, Tio Caio"})
    us.append({"2018-02-09":"Birthday, Tia Carol"})
    us.append({"2018-11-26":"Birthday, Marizilda"})
    us.append({"2018-05-10":"Birthday, Zeca"})

    if currentTime in us:
        return 'Happy ' + str(us.get(currentTime))

    if currentTime.hour <= 11:
        return str(morning[random.randint(0,len(morning)-1)]);
    elif 12 <= currentTime.hour < 17:
        return str(afternoon[random.randint(0,len(afternoon)-1)]);
    else:
        return str(evening[random.randint(0,len(evening)-1)]);
