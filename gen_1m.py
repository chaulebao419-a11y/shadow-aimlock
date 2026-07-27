import random, os, sys

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
TOTAL = 1_000_000
OUT_FILE = "keys.txt"

TYPES = (["vinhvien"]*3 + ["3thang"]*4 + ["1thang"]*3)
NAMES = {"vinhvien": "Vinhvien", "3thang": "3thang", "1thang": "1thang"}

rng = random.SystemRandom()

with open(OUT_FILE, "w", encoding="utf-8") as f:
    for i in range(TOTAL):
        k = f"DAT-{rng.choice(CHARS)}{rng.choice(CHARS)}{rng.choice(CHARS)}-{rng.choice(CHARS)}{rng.choice(CHARS)}{rng.choice(CHARS)}"
        t = TYPES[i % 10]
        f.write(f"{k} | {t}\n")
        if (i + 1) % 50000 == 0:
            print(f"  {i+1:,}/{TOTAL:,} ({(i+1)/TOTAL*100:.1f}%)", end="\r")
            sys.stdout.flush()

size = os.path.getsize(OUT_FILE) / (1024 * 1024)
print(f"\nDone: {OUT_FILE} ({size:.1f} MB)")
