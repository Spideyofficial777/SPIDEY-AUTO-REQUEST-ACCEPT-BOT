from pyrogram import filters
from Spidey.bot import SpideyBot as app


GROUP_ONLY_COMMANDS = [
    "kick", "ban", "tban", "unban", "mute", "tmute", "unmute",
    "warn", "unwarn", "resetwarns", "warnings",
    "purge", "del", "report",
]


@app.on_message(filters.command(GROUP_ONLY_COMMANDS) & filters.private)
async def group_command_private_notice(client, message):
    await message.reply(
        "ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɴᴇᴇᴅs ᴀ ᴛᴀʀɢᴇᴛ ᴜsᴇʀ ᴏʀ ɢʀᴏᴜᴘ ᴍᴇssᴀɢᴇ ᴄᴏɴᴛᴇxᴛ, "
        "sᴏ ᴜsᴇ ɪᴛ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ."
    )
