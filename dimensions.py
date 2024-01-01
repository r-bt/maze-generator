import json

f = open("letters.json", "r")
letters = json.load(f)
f.close()

lower = ["g"]

for letter in lower:
    letters[letter] = {
        "width": letters[letter]["width"],
        "height": letters[letter]["height"],
        "path": [(x + 1, y) for (x, y) in letters[letter]["path"]],
    }

f = open("letters.json", "w")
json.dump(letters, f)
f.close()
