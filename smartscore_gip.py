import requests
import json
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import smartscore_driver as driver

class Game:
    def __init__(self, ht, at, h_s, a_s):
        self.home_team = ht
        self.away_team = at
        self.home_score = h_s
        self.away_score = a_s

def checkScores(curr, weekNumUrl, weekNumFb, ref):
    url = f"https://api.foxsports.com/bifrost/v1/nfl/league/scores-segment/{weekNumUrl}"

    querystring = {"apikey":"jE7yBJVRNAwdDesMgTzTXUUSx1It41Fq"}

    headers = {
        'Accept': "application/json, text/plain, */*",
        'Referer': "https://www.foxsports.com/",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
        }

    r = requests.get(url, headers=headers, params=querystring)

    WEEK_data_raw = r.json()


    WEEK = []

    i = len(WEEK_data_raw['sectionList'])-1 # i = amount of days in the WEEK games are played on

    while i >= 0:
        for game_data in WEEK_data_raw['sectionList'][i]['events']:
            ht = game_data['lowerTeam']['name']
            at = game_data['upperTeam']['name']
            try:
                h_s = game_data['lowerTeam']['score']
                a_s = game_data['upperTeam']['score']
            except Exception:
                print(f"No score found for {at} @ {ht}. Defaulting to 0")
                h_s = 0
                a_s = 0
            WEEK.append(Game(ht, at, h_s, a_s))
        i-=1
    
    gameCount = 0
    update = False
    while (gameCount < len(WEEK) and not update):
        if WEEK[gameCount].away_score != curr[f'game{gameCount+1}']['awayScore']:
            update = True
        elif WEEK[gameCount].home_score != curr[f'game{gameCount+1}']['homeScore']:
            update = True
        gameCount += 1
    
    if (update):
        updateDb(ref, WEEK, weekNumFb)
    
    return(update)

def updateDb(ref, WEEK, weekNum):
    ref.push({
        weekNum:{}
    })
    week_ref=ref.child(weekNum)
    gameCount = 1
    for game in WEEK:
        gameNum = "game"+str(gameCount)
        game_ref = week_ref.child(gameNum)
        week_ref.push({
            gameNum:{}
        })
        game_ref.set({
            'homeTeam': game.home_team,
            'awayTeam': game.away_team,
            'homeScore': game.home_score,
            'awayScore': game.away_score
        })
        gameCount += 1

def updateCurr(weekNumFb):
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('serviceAcc.json')

    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://smartscore-43464.firebaseio.com/'
    })

    # As an admin, the app has access to read and write all data, regradless of Security Rules
    

    return(db.reference(f'schedule/{weekNumFb}/'))

def main():
    weekNumUrl, weekNumFb = driver.getWeek()
    currScoresFB = updateCurr(weekNumFb)
    run = True
    while (run):
        if(not driver.gameInProgress()):
            run = False
        if(checkScores(currScoresFB.get(), weekNumUrl, weekNumFb, currScoresFB)):
            currScoresFB = updateCurr(weekNumFb)
        time.sleep(120)