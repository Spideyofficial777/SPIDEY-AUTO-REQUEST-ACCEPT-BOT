import secrets
import time

from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Spidey.bot import SpideyBot as app
from database.database import db
from .helpers import is_admin, media_payload, send_payload
from .group_selector import resolve_groups
from .locks import TYPES

_PENDING = {}
_PENDING_TTL = 600

SUPPORTED = [
    "save", "get", "clear", "notes",
    "stop", "filters",
    "lock", "unlock", "locks",
    "blacklist", "unblacklist", "blacklists",
    "welcome", "goodbye", "antiflood",
    "setwelcome", "setgoodbye",
    "cleanwelcome", "cleangoodbye", "greetingsettings",
]

ON = {"on", "yes", "true", "1"}
OFF = {"off", "no", "false", "0"}


async def manageable_groups(client, user_id):
    return await resolve_groups(client, user_id)


def pending_put(user_id, command, args, payload=None):
    token = secrets.token_urlsafe(6)
    _PENDING[token] = {
        "user_id": user_id,
        "command": command,
        "args": args,
        "payload": payload,
        "expires": time.monotonic() + _PENDING_TTL,
    }
    return token


def pending_get(token, user_id):
    item = _PENDING.get(token)
    if not item:
        return None
    if item["user_id"] != user_id or item["expires"] < time.monotonic():
        _PENDING.pop(token, None)
        return None
    return item


async def execute(client, source_message, chat_id, command, args, payload=None, actor_id=None):
    actor_id = actor_id or (source_message.from_user.id if source_message.from_user else None)
    if not await is_admin(client, chat_id, actor_id):
        return "ʏᴏᴜ ᴀʀᴇ ɴᴏ ʟᴏɴɢᴇʀ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ."

    if command == "save":
        if not args or not payload:
            return "ᴜsᴀɢᴇ: ʀᴇᴘʟʏ ᴡɪᴛʜ /save note_name"
        await db.group_db.set_note(chat_id, args[0].lower(), payload)
        return "ɴᴏᴛᴇ sᴀᴠᴇᴅ."

    if command == "get":
        if not args:
            return "ᴜsᴀɢᴇ: /get note_name"
        data = await db.group_db.get_note(chat_id, args[0].lower())
        if not data:
            return "ɴᴏᴛᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ."
        await send_payload(source_message, data)
        return None

    if command == "clear":
        if not args:
            return "ᴜsᴀɢᴇ: /clear note_name"
        deleted = await db.group_db.delete_note(chat_id, args[0].lower())
        return "ɴᴏᴛᴇ ᴅᴇʟᴇᴛᴇᴅ." if deleted else "ɴᴏᴛᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ."

    if command == "notes":
        names = await db.group_db.list_notes(chat_id)
        return "ɴᴏᴛᴇs:\n• " + "\n• ".join(names) if names else "ɴᴏ ɴᴏᴛᴇs sᴀᴠᴇᴅ."

    if command == "stop":
        if not args:
            return "ᴜsᴀɢᴇ: /stop filter name"
        key = " ".join(args).strip().lower()
        deleted = await db.group_db.delete_filter(chat_id, key)
        return "ꜰɪʟᴛᴇʀ ᴅᴇʟᴇᴛᴇᴅ." if deleted else "ꜰɪʟᴛᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ."

    if command == "filters":
        names = await db.group_db.list_filters(chat_id)
        return "ꜰɪʟᴛᴇʀs:\n• " + "\n• ".join(names) if names else "ɴᴏ ꜰɪʟᴛᴇʀs sᴀᴠᴇᴅ."

    if command in ("lock", "unlock"):
        if not args or args[0].lower() not in TYPES:
            return "ᴛʏᴘᴇs: " + ", ".join(sorted(TYPES))
        key = args[0].lower()
        await db.group_db.set_lock(chat_id, key, command == "lock")
        return f"{key} sᴇᴛᴛɪɴɢ ᴜᴘᴅᴀᴛᴇᴅ."

    if command == "locks":
        locks = await db.group_db.get_locks(chat_id)
        lines = [f'• {key}: {"ʟᴏᴄᴋᴇᴅ" if locks.get(key) else "ᴜɴʟᴏᴄᴋᴇᴅ"}' for key in sorted(TYPES)]
        return "ʟᴏᴄᴋ sᴛᴀᴛᴜs\n" + "\n".join(lines)

    if command in ("blacklist", "unblacklist"):
        if not args:
            return "ᴜsᴀɢᴇ: /blacklist word or phrase"
        word = " ".join(args).strip().lower()
        await db.group_db.blacklist_word(chat_id, word, command == "blacklist")
        return "ʙʟᴀᴄᴋʟɪsᴛ ᴜᴘᴅᴀᴛᴇᴅ."

    if command == "blacklists":
        words = await db.group_db.get_blacklist(chat_id)
        return "ʙʟᴀᴄᴋʟɪsᴛ:\n• " + "\n• ".join(sorted(words)) if words else "ʙʟᴀᴄᴋʟɪsᴛ ɪs ᴇᴍᴘᴛʏ."

    if command in ("welcome", "goodbye"):
        if not args or args[0].lower() not in ON | OFF:
            return f"ᴜsᴀɢᴇ: /{command} on|off"
        await db.update_settings(chat_id, {command: args[0].lower() in ON})
        return "sᴇᴛᴛɪɴɢ ᴜᴘᴅᴀᴛᴇᴅ."

    if command == "antiflood":
        if not args:
            return "ᴜsᴀɢᴇ: /antiflood 0 ᴏʀ 3-20"
        try:
            number = int(args[0])
            if number != 0 and not 3 <= number <= 20:
                raise ValueError
        except ValueError:
            return "ᴜsᴀɢᴇ: /antiflood 0 ᴏʀ 3-20"
        await db.update_settings(chat_id, {"flood_limit": number})
        return "sᴇᴛᴛɪɴɢ ᴜᴘᴅᴀᴛᴇᴅ."

    if command in ("setwelcome", "setgoodbye"):
        kind = "welcome" if command == "setwelcome" else "goodbye"
        values = {}
        if payload:
            if payload.get("text"):
                values[f"{kind}_text"] = payload["text"]
            if payload.get("file_id") and payload.get("media_type") in ("photo", "video", "animation"):
                values[f"{kind}_media"] = payload["file_id"]
                values[f"{kind}_media_type"] = payload["media_type"]
        elif args:
            values[f"{kind}_text"] = " ".join(args)
        else:
            return f"ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ/ᴘʜᴏᴛᴏ/ᴠɪᴅᴇᴏ ᴏʀ ᴜsᴇ /set{kind} text"
        await db.update_settings(chat_id, values)
        return f"{kind} sᴀᴠᴇᴅ."

    if command in ("cleanwelcome", "cleangoodbye"):
        kind = "welcome" if command == "cleanwelcome" else "goodbye"
        await db.col.update_one({"_id": chat_id}, {"$unset": {
            f"{kind}_text": "", f"{kind}_media": "", f"{kind}_media_type": ""
        }})
        return f"{kind} ʀᴇsᴇᴛ ᴛᴏ ᴅᴇꜰᴀᴜʟᴛ."

    if command == "greetingsettings":
        settings = await db.get_settings(chat_id)
        return (
            "ɢʀᴇᴇᴛɪɴɢ sᴇᴛᴛɪɴɢs\n"
            f'• ᴡᴇʟᴄᴏᴍᴇ: {"ᴏɴ" if settings.get("welcome", True) else "ᴏꜰꜰ"}\n'
            f'• ɢᴏᴏᴅʙʏᴇ: {"ᴏɴ" if settings.get("goodbye", True) else "ᴏꜰꜰ"}\n'
            f'• ᴀɴᴛɪꜰʟᴏᴏᴅ: {settings.get("flood_limit", 0)}\n'
            f'• ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ: {"ᴏɴ" if settings.get("auto_delete", True) else "ᴏꜰꜰ"}'
        )

    return "ᴜɴsᴜᴘᴘᴏʀᴛᴇᴅ ᴄᴏᴍᴍᴀɴᴅ."


@app.on_message(filters.command(SUPPORTED) & filters.private)
async def private_group_control(client, message):
    if not message.from_user:
        return

    command = message.command[0].lower()
    args = message.command[1:]
    payload = media_payload(message.reply_to_message) if message.reply_to_message else None

    groups = await manageable_groups(client, message.from_user.id)
    if not groups:
        return await message.reply(
            "ɴᴏ ᴍᴀɴᴀɢᴇᴀʙʟᴇ ɢʀᴏᴜᴘ ꜰᴏᴜɴᴅ. "
            "ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ."
        )

    if len(groups) == 1:
        chat_id, title = groups[0]
        result = await execute(client, message, chat_id, command, args, payload)
        if result:
            await message.reply(f"<b>{title}</b>\n\n{result}", parse_mode=enums.ParseMode.HTML)
        return

    token = pending_put(message.from_user.id, command, args, payload)
    rows = [
        [InlineKeyboardButton(title[:50], callback_data=f"pgc:{token}:{chat_id}")]
        for chat_id, title in groups[:50]
    ]
    await message.reply(
        "sᴇʟᴇᴄᴛ ᴛʜᴇ ɢʀᴏᴜᴘ ꜰᴏʀ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.",
        reply_markup=InlineKeyboardMarkup(rows),
    )


@app.on_callback_query(filters.regex(r"^pgc:"))
async def private_group_control_callback(client, query):
    if not query.from_user:
        return

    parts = query.data.split(":", 2)
    if len(parts) != 3:
        return await query.answer("ɪɴᴠᴀʟɪᴅ ʀᴇǫᴜᴇsᴛ.", show_alert=True)

    token, chat_id_raw = parts[1], parts[2]
    item = pending_get(token, query.from_user.id)
    if not item:
        return await query.answer("ᴛʜɪs ʀᴇǫᴜᴇsᴛ ʜᴀs ᴇxᴘɪʀᴇᴅ.", show_alert=True)

    try:
        chat_id = int(chat_id_raw)
    except ValueError:
        return await query.answer("ɪɴᴠᴀʟɪᴅ ɢʀᴏᴜᴘ.", show_alert=True)

    result = await execute(
        client,
        query.message,
        chat_id,
        item["command"],
        item["args"],
        item["payload"],
        actor_id=query.from_user.id,
    )

    _PENDING.pop(token, None)

    try:
        chat = await client.get_chat(chat_id)
        title = chat.title or str(chat_id)
    except Exception:
        title = str(chat_id)

    await query.answer("ᴅᴏɴᴇ.", show_alert=False)
    if result:
        await query.message.edit_text(
            f"<b>{title}</b>\n\n{result}",
            parse_mode=enums.ParseMode.HTML,
        )
    else:
        await query.message.edit_text(f"<b>{title}</b>\n\nᴅᴏɴᴇ.", parse_mode=enums.ParseMode.HTML)
