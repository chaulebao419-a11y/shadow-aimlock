import random, os, sys

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
TOTAL = 2_000_000
TYPES = ["v", "f", "o", "t"]

rng = random.SystemRandom()
counts = {"v": 0, "f": 0, "o": 0, "t": 0}

with open("keys.js", "w", encoding="utf-8") as f:
    f.write("var externalKeys={")
    for i in range(TOTAL):
        k = f"DAT-{rng.choice(CHARS)}{rng.choice(CHARS)}{rng.choice(CHARS)}-{rng.choice(CHARS)}{rng.choice(CHARS)}{rng.choice(CHARS)}"
        t = TYPES[i % 4]
        counts[t] += 1
        if i > 0:
            f.write(",")
        f.write(f'"{k}":"{t}"')
        if (i + 1) % 100000 == 0:
            print(f"  {i+1:,}/{TOTAL:,} ({(i+1)/TOTAL*100:.0f}%)", end="\r")
            sys.stdout.flush()
    f.write("};var keysLoaded=true;")

size = os.path.getsize("keys.js") / (1024 * 1024)
print(f"\nDone: keys.js ({size:.1f} MB)")
print(f"v(vinhvien): {counts['v']:,} | f(5gio): {counts['f']:,} | o(1thang): {counts['o']:,} | t(3thang): {counts['t']:,}")
