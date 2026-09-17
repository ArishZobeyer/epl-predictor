from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import os
import json
import sys
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the trained model
MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "trained_model.pkl")
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Make model/features.py importable, then load match data
sys.path.append(os.path.join(BASE_DIR, "..", "model"))
from features import get_team_form, get_head_to_head

DATA_PATH = os.path.join(BASE_DIR, "..", "data", "raw_matches.json")
with open(DATA_PATH) as f:
    all_matches = json.load(f)
all_matches.sort(key=lambda m: m["utcDate"])


@app.route("/")
def home():
    return jsonify({"message": "EPL Predictor API is running"})


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    features = [[
        data["home_form"], data["away_form"],
        data["h2h_home_wins"], data["h2h_away_wins"], data["h2h_draws"]
    ]]
    probabilities = model.predict_proba(features)[0]
    return jsonify({
        "home_win_prob": probabilities[0],
        "draw_prob": probabilities[1],
        "away_win_prob": probabilities[2]
    })


@app.route("/predict-by-teams", methods=["POST"])
def predict_by_teams():
    data = request.get_json()
    home_team = data["home_team"]
    away_team = data["away_team"]

    now = datetime.now(timezone.utc).isoformat()

    home_form, _ = get_team_form(home_team, now, all_matches)
    away_form, _ = get_team_form(away_team, now, all_matches)
    h2h_home_wins, h2h_away_wins, h2h_draws, _ = get_head_to_head(home_team, away_team, now, all_matches)

    features = [[home_form, away_form, h2h_home_wins, h2h_away_wins, h2h_draws]]
    probabilities = model.predict_proba(features)[0]

    return jsonify({
        "home_team": home_team,
        "away_team": away_team,
        "home_form": home_form,
        "away_form": away_form,
        "home_win_prob": probabilities[0],
        "draw_prob": probabilities[1],
        "away_win_prob": probabilities[2]
    })


@app.route("/teams", methods=["GET"])
def get_teams():
    teams = set()
    for m in all_matches:
        teams.add(m["homeTeam"]["name"])
        teams.add(m["awayTeam"]["name"])
    return jsonify(sorted(teams))


if __name__ == "__main__":
    app.run(debug=True, port=5000)