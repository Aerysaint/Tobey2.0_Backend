import json
a = {"a" : "hello"}

with open("testing.json", "w") as f:
    json.dump(a, f)