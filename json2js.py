import json, sys, os

d = json.load(open("keys.json", "r"))
with open("keys.js", "w", encoding="utf-8") as f:
    f.write("var externalKeys={")
    first = True
    for k, v in d.items():
        if not first:
            f.write(",")
        f.write(f'"{k}":"{v}"')
        first = False
    f.write('};var keysLoaded=true;')

size = os.path.getsize("keys.js") / (1024 * 1024)
print(f"Done: keys.js ({size:.1f} MB)")
