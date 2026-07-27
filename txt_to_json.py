import sys, os

OUT_FILE = "keys.json"
TYPE_MAP = {"vinhvien": "v", "3thang": "t", "1thang": "o"}
first = True

with open("keys.txt", "r", encoding="utf-8") as src, open(OUT_FILE, "w", encoding="utf-8") as dst:
    dst.write("{")
    for i, line in enumerate(src):
        line = line.strip()
        if not line: continue
        parts = line.split(" | ")
        if len(parts) != 2: continue
        k, t = parts[0], parts[1]
        code = TYPE_MAP.get(t, "v")
        if not first:
            dst.write(",")
        dst.write(f'"{k}":"{code}"')
        first = False
        if (i + 1) % 50000 == 0:
            print(f"  {i+1:,}", end="\r")
            sys.stdout.flush()
    dst.write("}")

size = os.path.getsize(OUT_FILE) / (1024 * 1024)
print(f"\nDone: {OUT_FILE} ({size:.1f} MB)")
