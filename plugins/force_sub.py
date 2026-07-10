from pyrogram.errors import (
    ChannelPrivate,
    ChatAdminRequired,
    PeerIdInvalid,
    UserNotParticipant,
)

from configs import CHANNEL_IDS


async def validate_force_sub_channels(client):
    results = []
    me = await client.get_me()
    for channel_id in CHANNEL_IDS:
        try:
            chat = await client.get_chat(channel_id)
            member = await client.get_chat_member(channel_id, me.id)
            results.append({
                "channel_id": channel_id,
                "title": chat.title or str(channel_id),
                "ok": True,
                "status": str(member.status),
                "error": None,
            })
        except Exception as exc:
            results.append({
                "channel_id": channel_id,
                "title": str(channel_id),
                "ok": False,
                "status": None,
                "error": type(exc).__name__,
            })
    return results


async def missing_force_sub_channels(client, user_id):
    missing = []
    unavailable = []
    for channel_id in CHANNEL_IDS:
        try:
            member = await client.get_chat_member(channel_id, user_id)
            if str(member.status).lower().endswith("left") or str(member.status).lower().endswith("banned"):
                missing.append(channel_id)
        except UserNotParticipant:
            missing.append(channel_id)
        except (ChannelPrivate, ChatAdminRequired, PeerIdInvalid) as exc:
            unavailable.append((channel_id, type(exc).__name__))
        except Exception as exc:
            unavailable.append((channel_id, type(exc).__name__))
    return missing, unavailable
