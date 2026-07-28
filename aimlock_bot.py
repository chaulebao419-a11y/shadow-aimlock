import json, os, random, sys, logging

from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DATA_FILE = "bot_keys.json"
ADMIN_FILE = "admins.json"

TYPE_MAP = {
    "vinhvien": "v",
    "3thang": "t",
    "1thang": "o",
    "10gio": "h",
    "5gio": "f",
    "7ngay": "s"
}
TYPE_NAMES = {
    "vinhvien": "Vĩnh Viễn",
    "3thang": "3 Tháng",
    "1thang": "1 Tháng",
    "10gio": "10 Giờ",
    "5gio": "5 Giờ",
    "7ngay": "7 Ngày"
}

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
rng = random.SystemRandom()

def load_admins():
    if not os.path.exists(ADMIN_FILE):
        return []
    with open(ADMIN_FILE, "r") as f:
        return json.load(f)

def save_admins(admins):
    with open(ADMIN_FILE, "w") as f:
        json.dump(admins, f)

def load_keys():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_keys(keys):
    with open(DATA_FILE, "w") as f:
        json.dump(keys, f, separators=(",", ":"))

def is_admin(user_id):
    return user_id in load_admins()

def gen_key():
    return f"DAT-{rng.choice(CHARS)}{rng.choice(CHARS)}{rng.choice(CHARS)}-{rng.choice(CHARS)}{rng.choice(CHARS)}{rng.choice(CHARS)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 <b>Shadow AimLock Key Bot</b>\n\n"
        "Lệnh:\n"
        "/dangkiadmin - Đăng ký quyền Admin\n"
        "/genkey - Tạo key (Admin)\n"
        "/genkey &lt;loại&gt; - Tạo key nhanh (Admin)\n"
        "/listkeys - Danh sách key (Admin)\n"
        "/delkey &lt;key&gt; - Xóa key (Admin)\n"
        "/myid - Xem ID Telegram của bạn",
        parse_mode="HTML"
    )

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Your Telegram ID: <code>{update.effective_user.id}</code>", parse_mode="HTML")

async def dangkiadmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    admins = load_admins()
    if user.id in admins:
        await update.message.reply_text("✅ Bạn đã là Admin rồi!")
        return
    admins.append(user.id)
    save_admins(admins)
    await update.message.reply_text(
        f"🎉 <b>Đăng ký Admin thành công!</b>\n"
        f"User: {user.first_name} (ID: {user.id})\n\n"
        f"Dùng /genkey để tạo key.",
        parse_mode="HTML"
    )

async def genkey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Bạn không phải Admin. Dùng /dangkiadmin để đăng ký.")
        return

    if context.args:
        key_type = context.args[0].lower()
        if key_type not in TYPE_MAP:
            types = ", ".join(TYPE_MAP.keys())
            await update.message.reply_text(f"❌ Sai loại. Chọn: {types}")
            return
        code = TYPE_MAP[key_type]
        key = gen_key()
        keys = load_keys()
        keys[key] = code
        save_keys(keys)
        await update.message.reply_text(
            f"✅ <b>Key Created</b>\n"
            f"<code>{key}</code>\n"
            f"Loại: {TYPE_NAMES[key_type]}\n"
            f"Tổng: {len(keys)} key",
            parse_mode="HTML"
        )
        return

    keyboard = [
        [InlineKeyboardButton("♾ Vĩnh Viễn", callback_data="g_vinhvien")],
        [InlineKeyboardButton("📅 3 Tháng", callback_data="g_3thang"),
         InlineKeyboardButton("📅 1 Tháng", callback_data="g_1thang")],
        [InlineKeyboardButton("⏰ 10 Giờ", callback_data="g_10gio"),
         InlineKeyboardButton("⏰ 5 Giờ", callback_data="g_5gio")],
        [InlineKeyboardButton("📆 7 Ngày", callback_data="g_7ngay")]
    ]
    await update.message.reply_text("Chọn loại key:", reply_markup=InlineKeyboardMarkup(keyboard))

async def genkey_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except Exception:
        pass
    if not is_admin(query.from_user.id):
        try:
            await query.edit_message_text("❌ Bạn không phải Admin.")
        except Exception:
            pass
        return

    key_type = query.data[2:]
    code = TYPE_MAP[key_type]
    key = gen_key()
    keys = load_keys()
    keys[key] = code
    save_keys(keys)
    try:
        await query.edit_message_text(
            f"✅ <b>Key Created</b>\n"
            f"<code>{key}</code>\n"
            f"Loại: {TYPE_NAMES[key_type]}\n"
            f"Tổng: {len(keys)} key",
            parse_mode="HTML"
        )
    except Exception:
        pass

async def listkeys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Bạn không phải Admin.")
        return
    keys = load_keys()
    if not keys:
        await update.message.reply_text("📂 Chưa có key nào.")
        return
    code_to_name = {v: k for k, v in TYPE_MAP.items()}
    lines = [f"📂 <b>Danh sách key ({len(keys)}):</b>"]
    for i, (k, v) in enumerate(keys.items()):
        name = code_to_name.get(v, v)
        lines.append(f"{i+1}. <code>{k}</code> - {name}")
        if i >= 30:
            lines.append(f"... và {len(keys) - 31} key nữa")
            break
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

async def delkey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Bạn không phải Admin.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /delkey DAT-XXX-XXX")
        return
    key = context.args[0].upper()
    keys = load_keys()
    if key in keys:
        del keys[key]
        save_keys(keys)
        await update.message.reply_text(f"✅ Deleted <code>{key}</code>", parse_mode="HTML")
    else:
        await update.message.reply_text(f"❌ Key not found: <code>{key}</code>", parse_mode="HTML")

async def export_json(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Bạn không phải Admin.")
        return
    keys = load_keys()
    if not keys:
        await update.message.reply_text("📂 Chưa có key nào.")
        return
    output = json.dumps(keys, separators=(",", ":"))
    await update.message.reply_text(f"<code>{output[:4000]}</code>", parse_mode="HTML")
    if len(output) > 4000:
        await update.message.reply_text("(Nội dung bị cắt - dùng /export_file để tải file)")

async def export_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Bạn không phải Admin.")
        return
    keys = load_keys()
    if not keys:
        await update.message.reply_text("📂 Chưa có key nào.")
        return
    output = json.dumps(keys, separators=(",", ":"))
    with open("_export.json", "w", encoding="utf-8") as f:
        f.write(output)
    await update.message.reply_document(document="_export.json", filename="keys_export.json")

def main():
    from config import BOT_TOKEN
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("dangkiadmin", dangkiadmin))
    app.add_handler(CommandHandler("genkey", genkey))
    app.add_handler(CommandHandler("listkeys", listkeys))
    app.add_handler(CommandHandler("delkey", delkey))
    app.add_handler(CommandHandler("export", export_json))
    app.add_handler(CommandHandler("export_file", export_file))
    app.add_handler(CallbackQueryHandler(genkey_callback, pattern="^g_"))

    async def error_handler(update, context):
        logger.error(f"Update {update} caused error {context.error}")

    app.add_error_handler(error_handler)

    logger.info("Bot started. Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
