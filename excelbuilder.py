import requests
import json
import pandas as pd

class Game:
    def __init__(self, ht, at, h_s, a_s):
        self.home_team = ht
        self.away_team = at
        self.home_score = h_s
        self.away_score = a_s


url = "https://api.foxsports.com/bifrost/v1/nfl/league/scores-segment/w12"

querystring = {"apikey":"jE7yBJVRNAwdDesMgTzTXUUSx1It41Fq"}

headers = {
    'Accept': "application/json, text/plain, */*",
    'Referer': "https://www.foxsports.com/",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    }

r = requests.get(url, headers=headers, params=querystring)

week_data_raw = r.json()

df = pd.json_normalize(week_data_raw['sectionList'][0]['events'][0]['upperTeam'])

df.to_excel("team.xlsx")