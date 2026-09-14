from flask import Flask, jsonify, request
import pickle

app = Flask(__name__)

# Load the trained model once, when the server starts
with open("model/trained_model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/")
def home():
    return jsonify({"message": "EPL Predictor API is running"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    home_form = data["home_form"]
    away_form = data["away_form"]
    h2h_home_wins = data["h2h_home_wins"]
    h2h_away_wins = data["h2h_away_wins"]
    h2h_draws = data["h2h_draws"]

    features = [[home_form, away_form, h2h_home_wins, h2h_away_wins, h2h_draws]]

    probabilities = model.predict_proba(features)[0]

    return jsonify({
        "home_win_prob": probabilities[0],
        "draw_prob": probabilities[1],
        "away_win_prob": probabilities[2]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)