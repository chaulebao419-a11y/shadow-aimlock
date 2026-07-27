const fs = require("fs");
const JavaScriptObfuscator = require("javascript-obfuscator");

const html = fs.readFileSync("aimlockapp.html", "utf-8");
const match = html.match(/<script>([\s\S]*?)<\/script>/);
if (!match) { console.error("No script found"); process.exit(1); }

const originalJS = match[1];
const obfuscated = JavaScriptObfuscator.obfuscate(originalJS, {
    compact: true,
    controlFlowFlattening: true,
    controlFlowFlatteningThreshold: 0.75,
    numbersToExpressions: true,
    simplify: false,
    shuffleStringArray: true,
    splitStrings: true,
    stringArrayThreshold: 0.75,
    selfDefending: true,
    disableConsoleOutput: false,
}).getObfuscatedCode();

const newHtml = html.replace(originalJS, obfuscated);
fs.writeFileSync("aimlockapp_v2.html", newHtml, "utf-8");
console.log("Done: aimlockapp_v2.html");
