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

def get_showerthought():
    thoughts = []
    reddit = praw.Reddit(client_id='JgiAaoEUbf86tA',
                         client_secret='bz4rt2sUhhQs0suOR_2uq4QuIhA',
                         password='thomas08',
                         user_agent='testscript by /u/rhino_78',
                         username='rhino_78')
    for submission in reddit.subreddit('Showerthoughts').hot(limit=2):
        thoughts.append(submission.title)

    return thoughts[1]

def get_delta(year, month, day):
    c = datetime.now()
    b = datetime(year,month,day)
    a = datetime(c.year, c.month, c.day)
    return(b-a).days

def compliment():
    summerbreak='there are {0} days until summer break'.format(get_delta(2018,5,29))
    showerthought = get_showerthought()
    print(showerthought)
    tip, wisdom = get_tips()

    evening = [showerthought, summerbreak, tip, wisdom, 'ready for bed?', 'boa noite']
    afternoon = [showerthought, summerbreak, tip, wisdom, 'Good afternoon', 'boa tarde (Portuguese)', 'buon pomeriggio (Italian)', 'guten Nachmittag (German)', 'bonne apres-midid(French)', 'Kon''ichiwa (Japanese)']
    morning = [showerthought, summerbreak, tip, wisdom, 'bom dia', 'buen dia (spanish)', 'Bonjour (French)', 'Buongiorno (Italian)', 'guten Morgen (German)', 'Ohayo (Japanese)','Suprabhat (Hindi)', 'Good morning, beauty', 'Good Morning, Kids!']
    
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
        return str(morning[random.randint(0,len(morning)-1)]);
    elif 12 <= datetime.now().hour < 17:
        return str(afternoon[random.randint(0,len(afternoon)-1)]);
    else:
        return str(evening[random.randint(0,len(evening)-1)]);
