def get_team_form(team_name, before_date, all_matches, num_games=5):
    team_matches = []
    for m in all_matches:
        if m["utcDate"] >= before_date:
            continue
        if m["homeTeam"]["name"] != team_name and m["awayTeam"]["name"] != team_name:
            continue
        team_matches.append(m)

    recent = team_matches[-num_games:]
    points = 0
    for m in recent:
        is_home = m["homeTeam"]["name"] == team_name
        winner = m["score"]["winner"]
        if winner == "DRAW":
            points += 1
        elif (winner == "HOME_TEAM" and is_home) or (winner == "AWAY_TEAM" and not is_home):
            points += 3
    return points, len(recent)


def get_head_to_head(home_team, away_team, before_date, all_matches, num_games=5):
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

def get_goals_stats(team_name, before_date, all_matches, num_games=5):
    """Average goals scored and conceded in a team's last N games."""
    team_matches = []
    for m in all_matches:
        if m["utcDate"] >= before_date:
            continue
        if m["homeTeam"]["name"] != team_name and m["awayTeam"]["name"] != team_name:
            continue
        team_matches.append(m)

    recent = team_matches[-num_games:]
    if len(recent) == 0:
        return 0, 0

    goals_scored = 0
    goals_conceded = 0
    for m in recent:
        is_home = m["homeTeam"]["name"] == team_name
        home_goals = m["score"]["fullTime"]["home"]
        away_goals = m["score"]["fullTime"]["away"]
        if is_home:
            goals_scored += home_goals
            goals_conceded += away_goals
        else:
            goals_scored += away_goals
            goals_conceded += home_goals

    avg_scored = goals_scored / len(recent)
    avg_conceded = goals_conceded / len(recent)
    return avg_scored, avg_conceded