import json

with open("data/raw_matches.json") as f:
    matches = json.load(f)

print("Total matches:", len(matches))

# Look at one match's structure, just the useful fields
sample = matches[0]
print("\nSample match:")
print("Date:", sample["utcDate"])
print("Home:", sample["homeTeam"]["name"])
print("Away:", sample["awayTeam"]["name"])
print("Status:", sample["status"])
print("Winner:", sample["score"]["winner"])
print("Score:", sample["score"]["fullTime"])

# Check how many matches are actually finished (have real results)
finished = [m for m in matches if m["status"] == "FINISHED"]
print("\nFinished matches:", len(finished))
print("Not finished:", len(matches) - len(finished))