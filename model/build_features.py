from features import get_team_form, get_head_to_head
import json

with open("data/raw_matches.json") as f:
    matches = json.load(f)

# Sort matches chronologically - critical for calculating "form" correctly
matches.sort(key=lambda m: m["utcDate"])

print("Earliest match:", matches[0]["utcDate"])
print("Latest match:", matches[-1]["utcDate"])

def get_team_form(team_name, before_date, all_matches, num_games=5):
    """
    Calculate a team's form (points from last N games) before a given date.
    Win = 3 points, Draw = 1 point, Loss = 0 points
    """
    team_matches = []
    
    for m in all_matches:
        if m["utcDate"] >= before_date:
            continue  # skip matches on/after this date - avoid data leakage
        if m["homeTeam"]["name"] != team_name and m["awayTeam"]["name"] != team_name:
            continue  # this team wasn't in this match
        team_matches.append(m)
    
    recent = team_matches[-num_games:]  # last N matches
    
    points = 0
    for m in recent:
        is_home = m["homeTeam"]["name"] == team_name
        winner = m["score"]["winner"]
        
        if winner == "DRAW":
            points += 1
        elif (winner == "HOME_TEAM" and is_home) or (winner == "AWAY_TEAM" and not is_home):
            points += 3
        # else: loss, 0 points
    
    return points, len(recent)


# Test it on one team
test_match = matches[50]  # some match partway through the data
team = test_match["homeTeam"]["name"]
date = test_match["utcDate"]

points, games_played = get_team_form(team, date, matches)
print(f"{team}'s form before {date}: {points} points from {games_played} games")

def get_head_to_head(home_team, away_team, before_date, all_matches, num_games=5):
    """Get points earned by home_team against away_team in their recent meetings."""
    h2h_matches = []
    
    for m in all_matches:
        if m["utcDate"] >= before_date:
            continue
        teams = {m["homeTeam"]["name"], m["awayTeam"]["name"]}
        if teams == {home_team, away_team}:
            h2h_matches.append(m)
    
    recent = h2h_matches[-num_games:]
    home_wins = sum(1 for m in recent if m["score"]["winner"] == "HOME_TEAM" and m["homeTeam"]["name"] == home_team)
    away_wins = sum(1 for m in recent if m["score"]["winner"] == "AWAY_TEAM" and m["awayTeam"]["name"] == home_team)
    draws = sum(1 for m in recent if m["score"]["winner"] == "DRAW")
    
    return home_wins, away_wins, draws, len(recent)


# Build the full feature dataset
dataset = []

for m in matches:
    home = m["homeTeam"]["name"]
    away = m["awayTeam"]["name"]
    date = m["utcDate"]
    
    home_form, home_games = get_team_form(home, date, matches)
    away_form, away_games = get_team_form(away, date, matches)
    
    # Skip early-season matches with no real history yet
    if home_games < 3 or away_games < 3:
        continue
    
    h2h_home_wins, h2h_away_wins, h2h_draws, h2h_games = get_head_to_head(home, away, date, matches)
    
    dataset.append({
        "home_team": home,
        "away_team": away,
        "date": date,
        "home_form": home_form,
        "away_form": away_form,
        "h2h_home_wins": h2h_home_wins,
        "h2h_away_wins": h2h_away_wins,
        "h2h_draws": h2h_draws,
        "result": m["score"]["winner"]
    })

print("Dataset size:", len(dataset))
print("Sample row:", dataset[0])

with open("data/features.json", "w") as f:
    json.dump(dataset, f, indent=2)