with open("aimlockapp.html", "r", encoding="utf-8") as f:
    html = f.read()

with open("keys.js", "r", encoding="utf-8") as f:
    keys_js = f.read()

# Remove the script tag loading keys.js
html = html.replace('<script src="keys.js"></script>\n    <script>', '<script>')

# Remove the lines that enable button (they go after externalKeys is defined)
html = html.replace(
    '        document.getElementById("verifyBtn").textContent = "XÁC NHẬN KÍCH HOẠT";\n        document.getElementById("verifyBtn").disabled = false;\n        console.log("Keys loaded from keys.js: " + (typeof externalKeys !== "undefined" ? Object.keys(externalKeys).length : 0));\n',
    '        document.getElementById("verifyBtn").textContent = "XÁC NHẬN KÍCH HOẠT";\n        document.getElementById("verifyBtn").disabled = false;\n'
)

# Insert the externalKeys variable definition right before DATABASE_KEYS
html = html.replace(
    '        const DATABASE_KEYS = {',
    f'        {keys_js}\n\n        const DATABASE_KEYS = {{'
)

# Remove the "disabled" from the button HTML
html = html.replace('id="verifyBtn" onclick="verifyKey()" disabled>ĐANG TẢI KEY...<', 'id="verifyBtn" onclick="verifyKey()">XÁC NHẬN KÍCH HOẠT<')

with open("aimlockapp_all.html", "w", encoding="utf-8") as f:
    f.write(html)

import os
size = os.path.getsize("aimlockapp_all.html") / (1024 * 1024)
print(f"Done: aimlockapp_all.html ({size:.1f} MB)")
