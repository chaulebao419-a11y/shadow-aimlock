import random, os, sys

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
TOTAL = 10_000_000
OUT_FILE = "keys.txt"
TYPES = {0: "vinhvien", 1: "vinhvien", 2: "vinhvien",
         3: "3thang", 4: "3thang", 5: "3thang", 6: "3thang",
         7: "1thang", 8: "1thang", 9: "1thang"}

rng = random.SystemRandom()

with open(OUT_FILE, "w", encoding="utf-8") as f:
    for i in range(TOTAL):
        k = f"DAT-{rng.choice(CHARS)}{rng.choice(CHARS)}{rng.choice(CHARS)}-{rng.choice(CHARS)}{rng.choice(CHARS)}{rng.choice(CHARS)}"
        f.write(f"{k} | {TYPES[i%10]}\n")
        if (i + 1) % 100000 == 0:
            print(f"  {i+1:,}/{TOTAL:,} ({(i+1)/TOTAL*100:.1f}%)", end="\r")
            sys.stdout.flush()

size = os.path.getsize(OUT_FILE) / (1024 * 1024)
print(f"\nDone: keys.txt ({size:.1f} MB)")
