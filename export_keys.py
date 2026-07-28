import re

with open("aimlockapp.html", "r", encoding="utf-8") as f:
    html = f.read()

# Extract externalKeys
m = re.search(r'var externalKeys=\{(.*?)\};var keysLoaded=true;', html, re.DOTALL)
if m:
    entries = re.findall(r'"([^"]+)":"([^"]+)"', m.group(1))
    type_map = {"v": "vinhvien", "f": "5gio", "o": "1thang", "t": "3thang"}
    with open("all_keys.txt", "w", encoding="utf-8") as out:
        out.write(f"{'KEY':<20} {'TYPE':<15}\n")
        out.write("-" * 35 + "\n")
        for k, t in entries:
            out.write(f"{k:<20} {type_map.get(t, t):<15}\n")
    print(f"Exported {len(entries)} keys from externalKeys to all_keys.txt")

# Also extract DATABASE_KEYS
m2 = re.search(r'const DATABASE_KEYS = \{(.*?)\};', html, re.DOTALL)
if m2:
    entries2 = re.findall(r'"([^"]+)":\s*\{ type: "([^"]+)", name: "[^"]+" \}', m2.group(1))
    with open("sample_keys.txt", "w", encoding="utf-8") as out:
        out.write(f"{'KEY':<20} {'TYPE':<15}\n")
        out.write("-" * 35 + "\n")
        for k, t in entries2:
            out.write(f"{k:<20} {t:<15}\n")
    print(f"Exported {len(entries2)} keys from DATABASE_KEYS to sample_keys.txt")
