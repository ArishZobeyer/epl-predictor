import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("FOOTBALL_API_KEY")
headers = {"X-Auth-Token": api_key}

# Historical seasons to pull for training data
seasons = [ 2023, 2024, 2025]  # each number = the year the season started

all_matches = []

for season in seasons:
    url = f"https://api.football-data.org/v4/competitions/PL/matches?season={season}"
    response = requests.get(url, headers=headers)
    data = response.json()
    
   
    
    matches = data["matches"]
    all_matches.extend(matches)

print("Total matches collected:", len(all_matches))

# Save to a file
with open("data/raw_matches.json", "w") as f:
    json.dump(all_matches, f, indent=2)

print("Saved to data/raw_matches.json")