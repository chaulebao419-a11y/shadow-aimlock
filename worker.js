const B36 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const TELEGRAM_API = "https://api.telegram.org";

const TYPE_CODE = { "vinhvien": "v", "3thang": "t", "1thang": "o", "10gio": "h", "5gio": "f", "7ngay": "s" };
const CODE_TYPE = { "v": "vinhvien", "t": "3thang", "o": "1thang", "h": "10gio", "f": "5gio", "s": "7ngay" };
const TYPE_NAMES = { "vinhvien": "Vĩnh Viễn", "3thang": "3 Tháng", "1thang": "1 Tháng", "10gio": "10 Giờ", "5gio": "5 Giờ", "7ngay": "7 Ngày" };
const DEFAULT_ADMIN = 7909639685;
const IMPORT_TOKEN = "ALB-2026-RESERVE-x9f2k7";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Content-Type": "application/json"
};

function genKey() {
  let s = "";
  for (let i = 0; i < 9; i++) s += B36[Math.floor(Math.random() * 36)];
  return "DAT-" + s.slice(0, 3) + "-" + s.slice(3, 6) + "-" + s.slice(6, 9);
}

async function keyExists(env, key) {
  return (await env.KEYS.get("k:" + key)) !== null;
}

async function genUniqueKey(env) {
  for (let i = 0; i < 1296; i++) {
    const key = genKey();
    if (!(await keyExists(env, key))) return key;
  }
  throw new Error("Hết key không trùng!");
}

async function loadAdmins(env) {
  const raw = await env.ADMINS.get("admins", "json");
  return raw && Array.isArray(raw) ? raw : [];
}

async function saveAdmins(env, admins) {
  await env.ADMINS.put("admins", JSON.stringify(admins));
}

async function isAdmin(env, id) {
  const admins = await loadAdmins(env);
  return id === DEFAULT_ADMIN || admins.includes(id);
}

async function listAllKeys(env) {
  const keys = {};
  let cursor = undefined;
  do {
    const res = await env.KEYS.list({ prefix: "k:", cursor });
    for (const item of res.keys) {
      const key = item.name.slice(2);
      const type = await env.KEYS.get(item.name);
      keys[key] = type;
    }
    cursor = res.cursor;
  } while (cursor);
  return keys;
}

async function api(env, method, body) {
  const token = env.BOT_TOKEN || "";
  const res = await fetch(`${TELEGRAM_API}/bot${token}/${method}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  return res.json();
}

function escapeHtml(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

async function handleMessage(update, env) {
  const msg = update.message;
  if (!msg || !msg.text) return;
  const text = msg.text.trim();
  const chatId = msg.chat.id;
  const userId = msg.from.id;
  const parts = text.split(/\s+/);
  const cmd = parts[0].toLowerCase();
  const args = parts.slice(1);

  if (cmd === "/start" || cmd === "/help") {
    await api(env, "sendMessage", {
      chat_id: chatId,
      text: "🤖 <b>Shadow AimLock Key Bot</b>\n\nLệnh:\n/dangkiadmin - Đăng ký quyền Admin\n/genkey - Tạo key (Admin)\n/genkey &lt;loại&gt; - Tạo key nhanh (Admin)\n/listkeys - Danh sách key (Admin)\n/delkey &lt;key&gt; - Xóa key (Admin)\n/export - Xuất key dạng text (Admin)",
      parse_mode: "HTML"
    });
    return;
  }

  if (cmd === "/myid") {
    await api(env, "sendMessage", {
      chat_id: chatId,
      text: `🆔 Your Telegram ID: <code>${userId}</code>`,
      parse_mode: "HTML"
    });
    return;
  }

  if (cmd === "/dangkiadmin") {
    const admins = await loadAdmins(env);
    if (admins.includes(userId) || userId === DEFAULT_ADMIN) {
      await api(env, "sendMessage", { chat_id: chatId, text: "✅ Bạn đã là Admin rồi!" });
      return;
    }
    admins.push(userId);
    await saveAdmins(env, admins);
    await api(env, "sendMessage", {
      chat_id: chatId,
      text: `🎉 <b>Đăng ký Admin thành công!</b>\nUser: ${escapeHtml(msg.from.first_name || "")} (ID: ${userId})\n\nDùng /genkey để tạo key.`,
      parse_mode: "HTML"
    });
    return;
  }

  if (!(await isAdmin(env, userId))) {
    await api(env, "sendMessage", { chat_id: chatId, text: "❌ Bạn không phải Admin. Dùng /dangkiadmin để đăng ký." });
    return;
  }

  if (cmd === "/genkey") {
    if (args.length > 0) {
      const keyType = args[0].toLowerCase();
      if (!TYPE_CODE[keyType]) {
        await api(env, "sendMessage", {
          chat_id: chatId,
          text: `❌ Sai loại. Chọn: ${Object.keys(TYPE_CODE).join(", ")}`
        });
        return;
      }
      const key = await genUniqueKey(env);
      await env.KEYS.put("k:" + key, TYPE_CODE[keyType]);
      const keys = await listAllKeys(env);
      await api(env, "sendMessage", {
        chat_id: chatId,
        text: `✅ <b>Key Created</b>\n<code>${key}</code>\nLoại: ${TYPE_NAMES[keyType]}\nTổng: ${Object.keys(keys).length} key`,
        parse_mode: "HTML"
      });
      return;
    }
    const keyboard = {
      inline_keyboard: [
        [{ text: "♾ Vĩnh Viễn", callback_data: "g_vinhvien" }],
        [{ text: "📅 3 Tháng", callback_data: "g_3thang" }, { text: "📅 1 Tháng", callback_data: "g_1thang" }],
        [{ text: "⏰ 10 Giờ", callback_data: "g_10gio" }, { text: "⏰ 5 Giờ", callback_data: "g_5gio" }],
        [{ text: "📆 7 Ngày", callback_data: "g_7ngay" }]
      ]
    };
    await api(env, "sendMessage", {
      chat_id: chatId,
      text: "Chọn loại key:",
      reply_markup: JSON.stringify(keyboard)
    });
    return;
  }

  if (cmd === "/listkeys") {
    const keys = await listAllKeys(env);
    const entries = Object.entries(keys);
    if (entries.length === 0) {
      await api(env, "sendMessage", { chat_id: chatId, text: "📂 Chưa có key nào." });
      return;
    }
    const lines = [`📂 <b>Danh sách key (${entries.length}):</b>`];
    for (let i = 0; i < entries.length && i < 30; i++) {
      const [k, v] = entries[i];
      const name = TYPE_NAMES[CODE_TYPE[v] || "vinhvien"];
      lines.push(`${i + 1}. <code>${k}</code> - ${name}`);
    }
    if (entries.length > 30) lines.push(`... và ${entries.length - 31} key nữa`);
    await api(env, "sendMessage", { chat_id: chatId, text: lines.join("\n"), parse_mode: "HTML" });
    return;
  }

  if (cmd === "/delkey") {
    if (!args[0]) {
      await api(env, "sendMessage", { chat_id: chatId, text: "Usage: /delkey DAT-XXX-XXX-XXX" });
      return;
    }
    const key = args[0].toUpperCase();
    if (await keyExists(env, key)) {
      await env.KEYS.delete("k:" + key);
      await api(env, "sendMessage", { chat_id: chatId, text: `✅ Deleted <code>${key}</code>`, parse_mode: "HTML" });
    } else {
      await api(env, "sendMessage", { chat_id: chatId, text: `❌ Key not found: <code>${key}</code>`, parse_mode: "HTML" });
    }
    return;
  }

  if (cmd === "/export") {
    const keys = await listAllKeys(env);
    const output = JSON.stringify(keys);
    await api(env, "sendMessage", { chat_id: chatId, text: `<code>${escapeHtml(output.slice(0, 4000))}</code>`, parse_mode: "HTML" });
    if (output.length > 4000) {
      await api(env, "sendMessage", { chat_id: chatId, text: "(Nội dung bị cắt - xem trên /listkeys)" });
    }
    return;
  }
}

async function handleCallback(update, env) {
  const q = update.callback_query;
  if (!q || !q.data || !q.data.startsWith("g_")) return;
  const userId = q.from.id;
  try { await api(env, "answerCallbackQuery", { callback_query_id: q.id }); } catch (e) {}

  if (!(await isAdmin(env, userId))) {
    try {
      await api(env, "editMessageText", {
        chat_id: q.message.chat.id,
        message_id: q.message.message_id,
        text: "❌ Bạn không phải Admin."
      });
    } catch (e) {}
    return;
  }

  const keyType = q.data.slice(2);
  const key = await genUniqueKey(env);
  await env.KEYS.put("k:" + key, TYPE_CODE[keyType]);
  const keys = await listAllKeys(env);
  try {
    await api(env, "editMessageText", {
      chat_id: q.message.chat.id,
      message_id: q.message.message_id,
      text: `✅ <b>Key Created</b>\n<code>${key}</code>\nLoại: ${TYPE_NAMES[keyType]}\nTổng: ${Object.keys(keys).length} key`,
      parse_mode: "HTML"
    });
  } catch (e) {}
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;

    if (method === "OPTIONS") {
      return new Response("OK", { headers: CORS_HEADERS });
    }

    if (method === "POST" && path === "/webhook") {
      const update = await request.json();
      try {
        if (update.message) await handleMessage(update, env);
        else if (update.callback_query) await handleCallback(update, env);
      } catch (e) {
        console.error("Handler error:", e);
      }
      return new Response("OK", { status: 200 });
    }

    if (method === "GET" && path === "/keys") {
      const keys = await listAllKeys(env);
      return new Response(JSON.stringify(keys), { headers: CORS_HEADERS });
    }

    if (method === "GET" && path === "/count") {
      const keys = await listAllKeys(env);
      return new Response(JSON.stringify({ count: Object.keys(keys).length }), { headers: CORS_HEADERS });
    }

    if (method === "POST" && path === "/import") {
      const body = await request.json();
      if (!body || body.token !== IMPORT_TOKEN || typeof body.keys !== "object") {
        return new Response(JSON.stringify({ ok: false, error: "invalid" }), { headers: CORS_HEADERS, status: 400 });
      }
      let n = 0;
      for (const [key, type] of Object.entries(body.keys)) {
        await env.KEYS.put("k:" + key.toUpperCase(), String(type));
        n++;
      }
      return new Response(JSON.stringify({ ok: true, imported: n }), { headers: CORS_HEADERS });
    }

    if (method === "POST" && path === "/reserve") {
      const body = await request.json();
      const key = String(body && body.key || "").toUpperCase();
      const exists = await keyExists(env, key);
      if (!exists && key.startsWith("DAT-")) await env.KEYS.put("k:" + key, "v");
      return new Response(JSON.stringify({ ok: !exists }), { headers: CORS_HEADERS });
    }

    return new Response("OK", { status: 200 });
  }
};
