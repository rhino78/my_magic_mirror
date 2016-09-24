from bs4 import BeautifulSoup
import requests
            

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
		


def results():
        url = 'http://www.bbc.com/sport/football/tables'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        main = False
        team_list = []
        mast_list = ['Man City', 'Everton', 'Tottenham', 'Arsenal', 'Chelsea', 'Liverpool', 'Man Utd', 'Crystal Palace', 'Watford', 'West Brom', 'Leicester', 'Hull', 'Middlesbrough', 'Southhampton', 'Swansea', 'Burnley', 'Bournemouth', 'West Ham', 'Sunderland', 'Stoke']
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
                        n.last_5 = team_list[k+9], team_list[k+10], team_list[k+11], team_list[k+12], team_list[k+13]
                        table.append(n)

        return table


