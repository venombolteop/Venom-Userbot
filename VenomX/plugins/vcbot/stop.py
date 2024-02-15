from asyncio.queues import QueueEmpty
from pyrogram import filters
from pytgcalls.exceptions import GroupCallNotFound

from ... import *
from ...modules.mongo.streams import *
from ...modules.utilities import queues


@app.on_message(cdx(["stp"]) & ~filters.private)
@sudo_users_only
async def stop_stream(client, message):
    chat_id = message.chat.id
    try:
        a = await call.get_call(chat_id)
        if (a.status == "playing"
            or a.status == "paused"
        ):
            try:
                queues.clear(chat_id)
            except QueueEmpty:
                pass
            await call.change_stream(chat_id)
            await eor(message, "**sᴛʀᴇᴀᴍ sᴛᴏᴘᴘᴇᴅ!**")
        elif a.status == "not_playing":
            await eor(message, "**ɴᴏᴛʜɪɴɢ ᴘʟᴀʏɪɴɢ!**")
    except GroupCallNotFound:
        await eor(message, "**ɪ ᴀᴍ ɴᴏᴛ ɪɴ ᴠᴄ!**")
    except Exception as e:
        print(f"ᴇʀʀᴏʀ: {e}")
        
        
@app.on_message(cdz(["cstp"]))
@sudo_users_only
async def stop_stream_chat(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message,
            "**➻ ɴᴏ sᴛʀᴇᴀᴍ ᴄʜᴀᴛ sᴇᴛ❗**"
    )
    try:
        a = await call.get_call(chat_id)
        if (a.status == "playing"
            or a.status == "paused"
        ):
            try:
                queues.clear(chat_id)
            except QueueEmpty:
                pass
            await call.change_stream(chat_id)
            await eor(message, "**sᴛʀᴇᴀᴍ sᴛᴏᴘᴘᴇᴅ!**")
        elif a.status == "not_playing":
            await eor(message, "**ɴᴏᴛʜɪɴɢ ᴘʟᴀʏɪɴɢ!**")
    except GroupCallNotFound:
        await eor(message, "**ɪ ᴀᴍ ɴᴏᴛ ɪɴ ᴠᴄ!**")
    except Exception as e:
        print(f"ᴇʀʀᴏʀ: {e}")
        


@app.on_message(cdz(["end"]) & ~filters.private)
@sudo_users_only
async def close_stream_(client, message):
    chat_id = message.chat.id
    try:
        a = await call.get_call(chat_id)
        if (a.status == "not_playing"
            or a.status == "playing"
            or a.status == "paused"
        ):
            try:
                queues.clear(chat_id)
            except QueueEmpty:
                pass
            await call.leave_group_call(chat_id)
            await eor(message, "**sᴛʀᴇᴀᴍ ᴇɴᴅᴇᴅ!**")
    except GroupCallNotFound:
        await eor(message, "**ɪ ᴀᴍ ɴᴏᴛ ɪɴ ᴠᴄ!**")
    except Exception as e:
        print(f"ᴇʀʀᴏʀ: {e}")
        


@app.on_message(cdz(["cend"]))
@sudo_users_only
async def close_stream_chat(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message,
            "**➻ ɴᴏ sᴛʀᴇᴀᴍ ᴄʜᴀᴛ sᴇᴛ❗**"
    )
    try:
        a = await call.get_call(chat_id)
        if (a.status == "not_playing"
            or a.status == "playing"
            or a.status == "paused"
        ):
            try:
                queues.clear(chat_id)
            except QueueEmpty:
                pass
            await call.leave_group_call(chat_id)
            await eor(message, "**sᴛʀᴇᴀᴍ ᴇɴᴅᴇᴅ!**")
    except GroupCallNotFound:
        await eor(message, "**ɪ ᴀᴍ ɴᴏᴛ ɪɴ ᴠᴄ!**")
    except Exception as e:
        print(f"ᴇʀʀᴏʀ: {e}")
        
