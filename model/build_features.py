import json
from features import get_team_form, get_head_to_head, get_goals_stats

with open("data/raw_matches.json") as f:
    matches = json.load(f)

matches.sort(key=lambda m: m["utcDate"])

print("Earliest match:", matches[0]["utcDate"])
print("Latest match:", matches[-1]["utcDate"])

dataset = []

for m in matches:
    home = m["homeTeam"]["name"]
    away = m["awayTeam"]["name"]
    date = m["utcDate"]

    home_form, home_games = get_team_form(home, date, matches)
    away_form, away_games = get_team_form(away, date, matches)

    if home_games < 3 or away_games < 3:
        continue

    h2h_home_wins, h2h_away_wins, h2h_draws, h2h_games = get_head_to_head(home, away, date, matches)

    home_avg_scored, home_avg_conceded = get_goals_stats(home, date, matches)
    away_avg_scored, away_avg_conceded = get_goals_stats(away, date, matches)

    dataset.append({
        "home_team": home,
        "away_team": away,
        "date": date,
        "home_form": home_form,
        "away_form": away_form,
        "h2h_home_wins": h2h_home_wins,
        "h2h_away_wins": h2h_away_wins,
        "h2h_draws": h2h_draws,
        "home_avg_scored": home_avg_scored,
        "home_avg_conceded": home_avg_conceded,
        "away_avg_scored": away_avg_scored,
        "away_avg_conceded": away_avg_conceded,
        "result": m["score"]["winner"]
    })

print("Dataset size:", len(dataset))
print("Sample row:", dataset[0])

with open("data/features.json", "w") as f:
    json.dump(dataset, f, indent=2)