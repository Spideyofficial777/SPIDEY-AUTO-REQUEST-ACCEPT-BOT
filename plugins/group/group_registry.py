from datetime import datetime, timezone

from pyrogram import enums
from pyrogram.errors import FloodWait

from database.database import db

_VALID_MEMBER_STATUSES = {
    enums.ChatMemberStatus.OWNER,
    enums.ChatMemberStatus.ADMINISTRATOR,
    enums.ChatMemberStatus.MEMBER,
    enums.ChatMemberStatus.RESTRICTED,
}


async def register_group(client, chat):
    if chat.type not in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
        return
    status = None
    try:
        me = await client.get_me()
        member = await client.get_chat_member(chat.id, me.id)
        status = member.status
    except Exception:
        pass
    await db.add_chat(
        chat.id,
        chat.title or str(chat.id),
        chat_type=chat.type,
        bot_status=status,
    )


async def validate_registered_groups(client):
    me = await client.get_me()
    groups = await db.list_registered_groups()
    valid = 0
    unavailable = 0
    for item in groups:
        chat_id = item.get("id")
        if not chat_id:
            continue
        try:
            chat = await client.get_chat(chat_id)
            member = await client.get_chat_member(chat_id, me.id)
            status = member.status
            await db.update_chat_validation(
                chat_id,
                bot_status=status,
                title=chat.title or item.get("title") or str(chat_id),
                error=None,
            )
            if status in _VALID_MEMBER_STATUSES:
                valid += 1
            else:
                unavailable += 1
        except FloodWait:
            unavailable += 1
        except Exception as exc:
            unavailable += 1
            await db.update_chat_validation(
                chat_id,
                error=type(exc).__name__,
            )
    return {"total": len(groups), "valid": valid, "unavailable": unavailable}


async def manageable_groups(client, user_id):
    result = []
    seen = set()
    groups = await db.list_registered_groups()
    me = await client.get_me()

    for item in groups:
        chat_id = item.get("id")
        if not chat_id or chat_id in seen:
            continue

        try:
            bot_member = await client.get_chat_member(chat_id, me.id)
            if bot_member.status not in _VALID_MEMBER_STATUSES:
                continue

            user_member = await client.get_chat_member(chat_id, user_id)
            if user_member.status not in (
                enums.ChatMemberStatus.ADMINISTRATOR,
                enums.ChatMemberStatus.OWNER,
            ):
                continue

            chat = await client.get_chat(chat_id)
            result.append(
                (chat_id, chat.title or item.get("title") or str(chat_id))
            )
            seen.add(chat_id)
        except Exception:
            continue

    result.sort(key=lambda item: item[1].casefold())
    return result
