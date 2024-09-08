from VenomX import app, call, cdz, eor
from pyrogram import filters
from pytgcalls.exceptions import GroupCallNotFound
from pytgcalls.types import AudioQuality, VideoQuality
from pytgcalls.types.stream import MediaStream
from VenomX import get_media_stream, add_to_queue, get_from_queue, clear_queue, is_queue_empty, task_done

@app.on_message(cdz(["pse", "pause", "vpse", "vpause"]) & ~filters.private)
async def pause_stream(client, message):
    if message.sender_chat:
        return
    chat_id = message.chat.id
    try:
        call_info = await call.get_call(chat_id)
        if call_info.status == "playing":
            await call.pause_stream(chat_id)
            return await eor(message, "**Stream Paused!**")
        elif call_info.status == "paused":
            return await eor(message, "**Already Paused!**")
        else:
            return await eor(message, "**Nothing Streaming!**")
    except GroupCallNotFound:
        return await eor(message, "**I am Not in VC!**")

@app.on_message(cdz(["rsm", "resume", "vrsm", "vresume"]) & ~filters.private)
async def resume_stream(client, message):
    if message.sender_chat:
        return
    chat_id = message.chat.id
    try:
        call_info = await call.get_call(chat_id)
        if call_info.status == "paused":
            await call.resume_stream(chat_id)
            return await eor(message, "**Stream Resumed!**")
        elif call_info.status == "playing":
            return await eor(message, "**Already Playing!**")
        else:
            return await eor(message, "**Nothing Streaming!**")
    except GroupCallNotFound:
        return await eor(message, "**I am Not in VC!**")

@app.on_message(cdz(["skp", "skip", "vskp", "vskip"]) & ~filters.private)
async def skip_stream(client, message):
    if message.sender_chat:
        return
    chat_id = message.chat.id
    try:
        call_info = await call.get_call(chat_id)
        if call_info.status in ["playing", "paused"]:
            await task_done(chat_id)
            queue_empty = await is_queue_empty(chat_id)
            if queue_empty:
                await call.leave_group_call(chat_id)
                return await eor(message, "**🚫 Hey, Queue is Empty,\nSo Leaving VC❗...**")
            next_in_queue = await get_from_queue(chat_id)
            media = next_in_queue["media"]
            media_type = next_in_queue["type"]
            stream = await get_media_stream(media, media_type)
            await call.change_stream(chat_id, stream)
            return await eor(message, "Now Streaming ...")
        else:
            return await eor(message, "**Nothing Playing!**")
    except GroupCallNotFound:
        return await eor(message, "**I am Not in VC!**")

@app.on_message(cdz(["stp", "stop", "end", "vend"]) & ~filters.private)
async def cease_stream(client, message):
    if message.sender_chat:
        return
    chat_id = message.chat.id
    try:
        call_info = await call.get_call(chat_id)
        if call_info.status in ["playing", "paused"]:
            await clear_queue(chat_id)
            await call.leave_group_call(chat_id)
            return await eor(message, "**Stream Ended!**")
    except GroupCallNotFound:
        return await eor(message, "**I am Not in VC!**")

# Handle events manually
@app.on_message(filters.chat(lambda chat: chat.is_group) & filters.group)
async def handle_group_events(client, message):
    if message.text.startswith("/some_command"):
        chat_id = message.chat.id
        call_info = await call.get_call(chat_id)
        if call_info.status == "kicked":
            await call.leave_group_call(chat_id)
        elif call_info.status == "closed":
            # Handle closed call scenario
            pass
        elif call_info.status == "left":
            # Handle left call scenario
            pass
