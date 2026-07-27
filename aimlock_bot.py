import json
import os
import random
import string
import logging
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DATA_FILE = "keys.json"
ADMIN_IDS = [7970298273]  # Thêm Telegram user ID của bạn vào đây, ví dụ: [123456789]

def load_keys():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_keys(keys):
    with open(DATA_FILE, "w") as f:
        json.dump(keys, f, indent=2, ensure_ascii=False)

def generate_key():
    parts = []
    for _ in range(2):
        part = "".join(random.choices(string.digits, k=4))
        parts.append(part)
    return f"AIMLOCK-SAE-{parts[0]}-{parts[1]}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "AIMLOCK Key Bot\n"
        "Commands:\n"
        "/genkey vinhvien - Generate permanent key\n"
        "/genkey 3thang - Generate 3-month key\n"
        "/listkeys - List all keys\n"
        "/delkey <key> - Delete a key\n"
        "/export - Export keys as JSON\n"
        "/export_html - Export keys for HTML (paste into DATABASE_KEYS)"
    )

async def genkey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if ADMIN_IDS and user_id not in ADMIN_IDS:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return

    key_type = "vinhvien"
    if context.args:
        if context.args[0] in ("vinhvien", "3thang"):
            key_type = context.args[0]
        else:
            await update.message.reply_text("Sai định dạng. Dùng: /genkey vinhvien hoặc /genkey 3thang")
            return

    keys = load_keys()
    new_key = generate_key()
    while new_key in keys:
        new_key = generate_key()

    keys[new_key] = {
        "type": key_type,
        "name": "Key Vĩnh Viễn" if key_type == "vinhvien" else "Key 3 Tháng",
        "created": datetime.now().isoformat()
    }
    save_keys(keys)

    await update.message.reply_text(
        f"Key created:\n"
        f"`{new_key}`\n"
        f"Type: {keys[new_key]['name']}",
        parse_mode="Markdown"
    )

async def listkeys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if ADMIN_IDS and user_id not in ADMIN_IDS:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return

    keys = load_keys()
    if not keys:
        await update.message.reply_text("No keys found.")
        return

    msg_parts = [f"Total keys: {len(keys)}\n"]
    for k, v in keys.items():
        created = v.get("created", "unknown")[:10]
        msg_parts.append(f"`{k}` | {v['name']} | {created}")
        if len(msg_parts) > 40:
            break

    await update.message.reply_text("\n".join(msg_parts), parse_mode="Markdown")

async def delkey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if ADMIN_IDS and user_id not in ADMIN_IDS:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /delkey AIMLOCK-SAE-XXXX-XXXX")
        return

    key = context.args[0].upper()
    keys = load_keys()
    if key in keys:
        del keys[key]
        save_keys(keys)
        await update.message.reply_text(f"Deleted: `{key}`", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"Key not found: `{key}`", parse_mode="Markdown")

async def export_keys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if ADMIN_IDS and user_id not in ADMIN_IDS:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return

    keys = load_keys()
    if not keys:
        await update.message.reply_text("No keys to export.")
        return

    output = json.dumps(keys, indent=2, ensure_ascii=False)
    await update.message.reply_text(f"```json\n{output}\n```", parse_mode="Markdown")

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(f"Your Telegram User ID: `{user_id}`", parse_mode="Markdown")

async def export_html(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if ADMIN_IDS and user_id not in ADMIN_IDS:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return

    keys = load_keys()
    if not keys:
        await update.message.reply_text("No keys to export.")
        return

    lines = []
    for k, v in keys.items():
        lines.append(f'            "{k}": {{ "type": "{v["type"]}", "name": "{v["name"]}" }}')
    output = ",\n".join(lines)
    text = f"Copy this into DATABASE_KEYS in aimlockapp.html:\n\n```\n{output}\n```"
    await update.message.reply_text(text, parse_mode="Markdown")

def main():
    token = "7970298273:AAE7QFYafp4G3a1QY3W7sCHSV6DjPTcQ3uA"
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("genkey", genkey))
    app.add_handler(CommandHandler("listkeys", listkeys))
    app.add_handler(CommandHandler("delkey", delkey))
    app.add_handler(CommandHandler("export", export_keys))
    app.add_handler(CommandHandler("export_html", export_html))

    logger.info("Bot started. Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
