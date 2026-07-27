import json, os, sys, random

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
TOTAL = 1_000_000
OUT_FILE = "keys.json"
TYPES = {0: "v", 1: "v", 2: "v", 3: "t", 4: "t", 5: "t", 6: "t", 7: "o", 8: "o", 9: "o"}

rng = random.SystemRandom()
first = True

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("{")
    for i in range(TOTAL):
        k = f"DAT-{rng.choice(CHARS)}{rng.choice(CHARS)}{rng.choice(CHARS)}-{rng.choice(CHARS)}{rng.choice(CHARS)}{rng.choice(CHARS)}"
        if not first:
            f.write(",")
        f.write(f'"{k}":"{TYPES[i%10]}"')
        first = False
        if (i + 1) % 50000 == 0:
            print(f"  {i+1:,}/{TOTAL:,} ({(i+1)/TOTAL*100:.1f}%)", end="\r")
            sys.stdout.flush()
    f.write("}")

size = os.path.getsize(OUT_FILE) / (1024 * 1024)
print(f"\nDone: {OUT_FILE} ({size:.1f} MB)")
