from VenomX import app, call, cdz, eor
from VenomX import add_to_queue, get_from_queue, get_media_stream
from VenomX import clear_queue, is_queue_empty, task_done
from pyrogram import filters
from pytgcalls.exceptions import GroupCallNotFound


@app.on_message(cdz(["pse", "pause", "vpse", "vpause"]) & ~filters.private)
async def pause_stream(client, message):
    if message.sender_chat:
        return
    chat_id = message.chat.id
    try:
        a = await call.get_call(chat_id)
        if a.status == "playing":
            await call.pause_stream(chat_id)
            return await eor(message, "**Stream Paused!**")
        elif a.status == "paused":
            return await eor(message, "**Already Paused!**")
        elif a.status == "not_playing":
            return await eor(message, "**Nothing Streaming!**")
    except GroupCallNotFound:
        return await eor(message, "**I am Not in VC!**")


@app.on_message(cdz(["rsm", "resume", "vrsm", "vresume"]) & ~filters.private)
async def resume_stream(client, message):
    if message.sender_chat:
        return
    chat_id = message.chat.id
    try:
        a = await call.get_call(chat_id)
        if a.status == "paused":
            await call.resume_stream(chat_id)
            return await eor(message, "**Stream Resumed!**")
        elif a.status == "playing":
            return await eor(message, "**Already Playing!**")
        elif a.status == "not_playing":
            return await eor(message, "**Nothing Streaming!**")
    except GroupCallNotFound:
        return await eor(message, "**I am Not in VC!**")


@app.on_message(cdz(["skp", "skip", "vskp", "vskip"]) & ~filters.private)
async def skip_stream(client, message):
    if message.sender_chat:
        return
    chat_id = message.chat.id
    try:
        a = await call.get_call(chat_id)
        if (a.status == "playing"
            or a.status == "paused"
        ):
            await task_done(chat_id)
            queue_empty = await is_queue_empty(chat_id)
            if queue_empty :
                await call.leave_group_call(chat_id)
                return await eor(
                    message,
                    "**🚫 Hey, Queue is Empty,\nSo Leaving VC❗...**"
                )
            check = await get_from_queue(chat_id)
            media = check["media"]
            type = check["type"]
            stream = await get_media_stream(media, type)
            await call.change_stream(chat_id, stream)
            return await eor(
                message,
                "Now Streaming ..."
            )
        elif a.status == "not_playing":
            return await eor(message, "**Nothing Playing!**")
    except GroupCallNotFound:
        return await eor(message, "**I am Not in VC!**")
    

@app.on_message(cdz(["stp", "stop", "end", "vend"]) & ~filters.private)
async def cease_stream(client, message):
    if message.sender_chat:
        return
    chat_id = message.chat.id
    try:
        a = await call.get_call(chat_id)
        if (a.status == "not_playing"
            or a.status == "playing"
            or a.status == "paused"
        ):
            await clear_queue(chat_id)
            await call.leave_group_call(chat_id)
            return await eor(message, "**Stream Ended!**")
    except GroupCallNotFound:
        return await eor(message, "**I am Not in VC!**")
    
