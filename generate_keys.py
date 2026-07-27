import json, random, os, sys

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
TOTAL = 10_000_000
OUT_FILE = "keys.json"
NAMES = {"vinhvien": "Key Vĩnh Viễn", "3thang": "Key 3 Tháng", "1thang": "Key 1 Tháng"}

rng = random.SystemRandom()
counts = {"vinhvien": 0, "3thang": 0, "1thang": 0}
written = 0

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("{")
    for i in range(TOTAL):
        k = f"DAT-{rng.choice(CHARS)}{rng.choice(CHARS)}{rng.choice(CHARS)}-{rng.choice(CHARS)}{rng.choice(CHARS)}{rng.choice(CHARS)}"
        t = ["vinhvien","vinhvien","vinhvien","3thang","3thang","3thang","3thang","1thang","1thang","1thang"][i%10]
        counts[t] += 1
        if written > 0:
            f.write(",")
        f.write(f'"{k}":{{"type":"{t}","name":"{NAMES[t]}"}}')
        written += 1
        if written % 100000 == 0:
            print(f"  {written:,}/{TOTAL:,} ({written/TOTAL*100:.1f}%)", end="\r")
            sys.stdout.flush()
    f.write("}")

size = os.path.getsize(OUT_FILE) / (1024 * 1024)
print(f"\n\nDone: {written:,} keys -> {OUT_FILE} ({size:.1f} MB)")
print(f"vinhvien: {counts['vinhvien']:,} | 3thang: {counts['3thang']:,} | 1thang: {counts['1thang']:,}")
