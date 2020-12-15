import requests
import sys
import json
from dateutil.relativedelta import relativedelta
from datetime import datetime

class Game:
    def __init__(self, ht, at, h_s, a_s):
        self.home_team = ht
        self.away_team = at
        self.home_score = h_s
        self.away_score = a_s


def getJson():
    
    weekUrl, week = getWeek()
    url = f"https://api.foxsports.com/bifrost/v1/nfl/league/scores-segment/{weekUrl}"

    querystring = {"apikey":"jE7yBJVRNAwdDesMgTzTXUUSx1It41Fq"}

    headers = {
        'Accept': "application/json, text/plain, */*",
        'Referer': "https://www.foxsports.com/",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
        }

    r = requests.get(url, headers=headers, params=querystring)
    
    return r.json()

#TODO: put week dates into an array
def getWeek():
    date = datetime.today()
    week13Start = "2020-12-03"
    week14Start = "2020-12-10"
    week15Start = "2020-12-17"
    week16Start = "2020-12-24"
    week17Start = "2020-12-31"
    week18Start = "2021-01-07"
    if (date < datetime.strptime(week13Start, '%Y-%m-%d')):
        return("w13", "week13")################################
    elif (date < datetime.strptime(week14Start, '%Y-%m-%d')):
        return("w13", "week13")
    elif (date < datetime.strptime(week15Start, '%Y-%m-%d')):
        return("w14", "week14")
    elif (date < datetime.strptime(week16Start, '%Y-%m-%d')):
        return("w15", "week15")
    elif (date < datetime.strptime(week17Start, '%Y-%m-%d')):
        return("w16", "week16")
    elif (date < datetime.strptime(week18Start, '%Y-%m-%d')):
        return("w17", "week17")
    else:
        print(date)

def nextGameDate():
    data = getJson()
    datesList = []
    iterator = len(data['sectionList'])-1 # i = amount of days in the WEEK games are played on
    while(iterator >= 0):
        for dates in data['sectionList'][iterator]['events']:
            gameDate = dates['eventTime'][:10]
            datesList.append(gameDate)
        iterator -= 1
    minDate = '2030-01-01'
    for date in datesList:
        if ((datetime.strptime(date, '%Y-%m-%d') < datetime.strptime(minDate, '%Y-%m-%d')) and (datetime.today() < datetime.strptime(date, '%Y-%m-%d'))):
            minDate = date
    return(minDate)

def gameInProgress():
    data = getJson()
    List = []
    iterator = len(data['sectionList'])-1 # i = amount of days in the WEEK games are played on
    while(iterator >= 0):
        for dates in data['sectionList'][iterator]['events']:
            gameStatus = dates['eventStatus']
            List.append(gameStatus)
        iterator -= 1
    for game in List:
        if (game == 2 or game == 3):
            return False
        else:
            return True

def secondsUntilNextGame():
    nextGame = nextGameDate()
    d = (relativedelta(datetime.today(), datetime.strptime(nextGame, '%Y-%m-%d')).days)
    h = (relativedelta(datetime.today(), datetime.strptime(nextGame, '%Y-%m-%d')).hours)
    s = (relativedelta(datetime.today(), datetime.strptime(nextGame, '%Y-%m-%d')).seconds)
    return(((d*86400)+(h*3600)+s)*-1)
