import requests
import re
import unicodedata
import urllib
import csv
from bs4 import BeautifulSoup

# file stuff
output = open('games.csv', 'wb')
writer = csv.writer(output, dialect='excel')
writer.writerow( ('Team', 'opponent', 'score', 'date', 'tournament') )

# make a request to the server
payload = {'CT_Main_0$lnkViewAll': ''}
html = requests.post("http://play.usaultimate.org/teams/events/team_rankings/?RankSet=College-Men", data=payload)
soup1 = BeautifulSoup(html.text, "html.parser")

# get all the links in the HTML
for HTMLLink in soup1.find_all('a'):
    link = HTMLLink.get('href')

    # if this is a link to a team then get the HTML there
    if str(link).startswith('/teams/events/Eventteam'): 

        teamHTML = requests.get("http://play.usaultimate.org" + str(link))
        teamSoup = BeautifulSoup(teamHTML.text, "html.parser")

        # get team info
        teamName = teamSoup.find("div", class_="profile_info")
        team = teamSoup.h4.text
        teams = teamSoup.find_all(href=re.compile("TeamId"))
        scores = teamSoup.find_all(href=re.compile("EventGame"))
        dates = teamSoup.find_all(id=re.compile("lblMonth"))

        tournament = ""
        indexDifference = 0

        # for every date get all the games
        for index in range(len(dates)):
            match = re.search(".* \d\d( |$)", dates[index].text)
            if match:

                try:
                    writer.writerow( (team, \
                                      teams[index - indexDifference].text, \
                                      scores[index - indexDifference].text, \
                                      dates[index].text, \
                                      tournament \
                                   ) )

                    print("[%(team)s, %(opponent)s, %(score)s, \
                            %(date)s, %(tournament)s]" % \
                         {"team": team, \
                          "opponent":teams[index - indexDifference].text, \
                          "score": scores[index - indexDifference].text, \
                          "date": dates[index].text, \
                          "tournament": tournament
                         })
                except:
                    print("index: %(i)i" % {"i" : index})
                    print("indexDifference: %(i)i" %  {"i" : indexDifference})

            else:
                indexDifference = indexDifference + 1
                tournament = dates[index].text
        print ""
