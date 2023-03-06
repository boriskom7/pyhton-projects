import requests
import json

url = "https://v3.football.api-sports.io/standings"

headers = {
  'x-rapidapi-key': '65745b60c458dff9865b6046abba0523',
  'x-rapidapi-host': 'v3.football.api-sports.io'
}

class Data():
    def __init__(self, id):
        super().__init__()
        self.teams = {}
        self.league = {}
        self.get_data(id)

    def get_data(self, league_id):
        parameters = {
            "league": league_id,
            "season": "2022",
        }

        #with open("league_data.json") as file:
        #    data = json.load(file)

        response = requests.request("GET", url, headers=headers, params=parameters)
        data = response.json()["response"][0]
        print(data)

        self.teams = data["league"]["standings"]
        self.league = {
            "id": data["league"]["id"],
            "name": data["league"]["name"],
            "country": data["league"]["country"],
            "logo": data["league"]["logo"],
            "flag": data["league"]["flag"],
            "season": data["league"]["season"],
        }






