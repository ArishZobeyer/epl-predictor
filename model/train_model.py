import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

with open("data/features.json") as f:
    dataset = json.load(f)

# Build X (features) and y (labels)
X = []
y = []

for row in dataset:
    features = [
        row["home_form"],
        row["away_form"],
        row["h2h_home_wins"],
        row["h2h_away_wins"],
        row["h2h_draws"],
        row["home_avg_scored"],
        row["home_avg_conceded"],
        row["away_avg_scored"],
        row["away_avg_conceded"]
    ]
    X.append(features)
    y.append(row["result"])

print("Number of examples:", len(X))
print("Sample features:", X[0])
print("Number of features per example:", len(X[0]))
print("Sample label:", y[0])
print("Unique labels:", set(y))

# Convert text labels to numbers
label_map = {"HOME_TEAM": 0, "DRAW": 1, "AWAY_TEAM": 2}
y_numeric = [label_map[label] for label in y]

# Split, train, predict, score
X_train, X_test, y_train, y_test = train_test_split(X, y_numeric, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("\nTraining set size:", len(X_train))
print("Test set size:", len(X_test))
print("Accuracy:", accuracy)

# Baseline: what if we always predicted Home Team wins?
baseline_predictions = [0] * len(y_test)  # 0 = HOME_TEAM
baseline_accuracy = accuracy_score(y_test, baseline_predictions)
print("Baseline (always predict home win):", baseline_accuracy)

import pickle

with open("model/trained_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved to model/trained_model.pkl")

feature_names = ["home_form", "away_form", "h2h_home_wins", "h2h_away_wins", "h2h_draws",
                  "home_avg_scored", "home_avg_conceded", "away_avg_scored", "away_avg_conceded"]

importances = model.feature_importances_
for name, importance in sorted(zip(feature_names, importances), key=lambda x: -x[1]):
    print(f"{name}: {importance:.3f}")