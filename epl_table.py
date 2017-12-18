from bs4 import BeautifulSoup
import requests
from datetime import datetime

class Teams():
	position = ""
	p = ""
	w = ""
	d = ""
	l = ""
	f = ""
	a = ""
	gd = ""
	pt = ""
	movement = ""
	last_5 = []
	def __init__(self, name):
		self.name = name
		
def my_time(string):
        english_time = datetime.strptime(string, '%H:%M').time()
        print(english_time)
        return str('{0}:{1}'.format(english_time.hour-6, english_time.minute))

def results():
        print('getting results')
        url = 'http://www.bbc.com/sport/football/tables'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        main = False
        team_list = []
        mast_list = ['Manchester City', 'Everton', 'Tottenham Hotspur', 'Arsenal', 'Chelsea', 'Liverpool', 'Manchester United', 'Crystal Palace', 'Watford', 'West Bromwich Albion', 'Leicester City', 'Hull City', 'Middlesbrough', 'Southampton', 'Swansea City', 'Burnley', 'Bournemouth', 'West Ham United', 'Sunderland', 'Stoke City']
        for s in soup.strings:
                if not s.isspace():
                        if s == "This table charts the Premier League teams":
                                main = True
                        elif s == "Please note: All times UK. Tables are subject to change. The BBC is not responsible for any changes that may be made.":
                                main = False

                if main and not s.isspace(): #found the table
                        if s == "This table charts the Premier League teams": # we don't want the header here
                                team_list = []
                        elif "Report" not in s or "last match" not in s:
                                team_list.append(s)

        k = -1
        table = []
        for i in team_list:
                k+=1
                if i in mast_list:
                        n = Teams(i)
                        n.movement = team_list[k-2]
                        n.position = team_list[k-1]
                        n.p = team_list[k+1]
                        n.w = team_list[k+2]
                        n.d = team_list[k+3]
                        n.l = team_list[k+4]
                        n.f = team_list[k+5]
                        n.a = team_list[k+6]
                        n.gd = team_list[k+7]
                        n.pt= team_list[k+8]
                        n.last_5 = team_list[k+16], team_list[k+15], team_list[k+14], team_list[k+13], team_list[k+12]
                        print(n.position)
                        table.append(n)

        return table

def last_match():
        url = 'http://www.bbc.com/sport/football/teams/arsenal'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        last = soup.find(id="last-match")

        last_data = []

        for s in last.strings:
                text = str(s.strip())
                if text and "View match report" not in text:
                        last_data.append(text)

        return last_data

def next_match():
        url = 'http://www.bbc.com/sport/football/teams/arsenal'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        next_match = soup.find(id="next-match")

        next_data = []
        i = 0

        for s in next_match.strings:
                i = i+1
                text = str(s.strip())
                if text:
                        next_data.append(text)

        return next_data
