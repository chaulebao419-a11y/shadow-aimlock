import re, os

with open("aimlockapp.html", "r", encoding="utf-8") as f:
    html = f.read()

with open("keys.js", "r", encoding="utf-8") as f:
    keys_js = f.read()

# Replace the old externalKeys line with the new one
html = re.sub(
    r'var externalKeys=\{[^}]*\};var keysLoaded=true;',
    keys_js,
    html
)

with open("aimlockapp.html", "w", encoding="utf-8") as f:
    f.write(html)

size = os.path.getsize("aimlockapp.html") / (1024 * 1024)
print(f"Done: aimlockapp.html ({size:.1f} MB)")
