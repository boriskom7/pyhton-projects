import requests
from bs4 import BeautifulSoup
import re
from prettytable import PrettyTable
import json
import pandas as pd

URL = "https://www.nba.com/stats"

response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

# 1 get categories names
categories = []

# get all stats tables sections 
title_data = soup.find_all(class_="LeaderBoardCard_lbcTitle___WI9J", name="h2") 

for data in title_data:
    to_string = str(data).replace('"','')
    # find table category name -> categories
    title = re.search(r">(.*)<", to_string)
    
    # print(title.group(1))
    categories.append(title.group(1))

# 2.1 get players stats
all_stats = soup.find_all(class_="LeaderBoardPlayerCard_lbpcTableRow___Lod5", name="tr") 

index = 0
previous_category = ""
player_stats = {}

# for every stats row in all tables
for next_element in all_stats:
    category = categories[index // 5]

    to_string = str(next_element).replace('"','')
    # find all row's stats
    stats = re.findall(r">(.*?)<", to_string)
    
    try:
        player = {"index": stats[1], "Player's Name": stats[5], "Team": stats[7], "Score": stats[11]}
        if category == previous_category:
            player_stats[category].append(player)
        else:
            player_stats[category] = []
            player_stats[category].append(player)
    except IndexError:
        pass

    #print(player)
    previous_category = category
    index +=1

#print(player_stats)

# 2.2 get teams stats
all_stats = soup.find_all(class_="LeaderBoadTeamCard_lbtcTableRow__pJljn", name="tr") 

index = 0
previous_category = ""
team_stats = {}

# for every stats row in all tables
for next_element in all_stats:
    category = categories[index // 5]

    to_string = str(next_element).replace('"','')
    # find all row's stats
    stats = re.findall(r">(.*?)<", to_string)
  
    try:
        team = {"index": stats[1], "Team": stats[5], "Score": stats[8]}
        if category == previous_category:
            team_stats[category].append(team)
        else:
            team_stats[category] = []
            team_stats[category].append(team)
    except IndexError:
        pass

    #print(team)
    previous_category = category
    index +=1

#print(team_stats)

# 3 save to json file
with open("player_stats.json", "w") as outfile:
    json.dump(player_stats, outfile)
with open("team_stats.json", "w") as outfile:
    json.dump(team_stats, outfile)    

# 4 save as csv
df = pd.read_json("player_stats.json")
df.to_csv("player_stats.csv")
df = pd.read_json("team_stats.json")
df.to_csv("team_stats.csv")

# 5.1 print player stats as pretty tables
for category,players in player_stats.items():
    print(category)
    t = PrettyTable()
    
    for row in players:
        t.field_names = row.keys()
        t.add_row([*row.values()]) 
    print(t)

# 5.2 print team stats as pretty tables
for category,teams in team_stats.items():
    print(category)
    t = PrettyTable()
    
    for row in teams:
        t.field_names = row.keys()
        t.add_row([*row.values()]) 
    print(t)

