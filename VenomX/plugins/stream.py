import re

from VenomX import app, call, cdz, eor
from VenomX import add_to_queue
from VenomX import download_media_file
from VenomX import get_media_info, get_media_stream
from pyrogram import filters
from pytgcalls.exceptions import AlreadyJoinedError, GroupCallNotFound, NoActiveGroupCall
from pytgcalls.types import Update

# Event handler for playing or streaming media (audio or video)
@app.on_message(cdz(["ply", "play", "vply", "vplay"]) & ~filters.private)
async def start_stream(client, message):
    if message.sender_chat:
        return
    
    aux = await eor(message, "**🔄 Processing ...**")
    chat_id = message.chat.id
    user_id = message.from_user.id
    mention = message.from_user.mention
    replied = message.reply_to_message
    audiostream = ((replied.audio or replied.voice) if replied else None)
    videostream = ((replied.video or replied.document) if replied else None)
    command = str(message.command[0][0])
    
    # Handle audio and video streams
    if audiostream:
        media = await client.download_media(replied)
        stream_type = "Audio"
    elif videostream:
        media = await client.download_media(replied)
        stream_type = "Video"
    else:
        if len(message.command) < 2:
            return await aux.edit("**🥀 Give Me Some Query To\nStream Audio Or Video❗...**")
        
        query = message.text.split(None, 1)[1]
        
        if "https://" in query:
            base = r"(?:https?:)?(?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube(?:\-nocookie)?\.(?:[A-Za-z]{2,4}|[A-Za-z]{2,3}\.[A-Za-z]{2})\/)?(?:shorts\/|live\/)?(?:watch|embed\/|vi?\/)*(?:\?[\w=&]*vi?=)?([^#&\?\/]{11}).*$"
            resu = re.findall(base, query)
            vidid = resu[0] if resu else None
        else:
            vidid = None
        
        # Fetch media info
        results = await get_media_info(vidid, query)
        link = str(results[1])
        stream_type = "Video" if command == "v" else "Audio"
        
        # Download media
        media = await download_media_file(link, stream_type)
    
    try:
        # Get current call status
        a = await call.get_call(chat_id)
        
        # If the call is not playing, start the stream
        if a.status == Update.STREAM_STOPPED:
            stream = await get_media_stream(media, stream_type)
            await call.change_stream(chat_id, stream)
            await add_to_queue(chat_id, media=media, type=stream_type)
            return await aux.edit("**Streaming Started ....**")
        
        # If the call is playing or paused, add to queue
        elif a.status in [Update.STREAM_PLAYING, Update.STREAM_PAUSED]:
            position = await add_to_queue(chat_id, media=media, type=stream_type)
            return await aux.edit(f"**Added to Queue At {position}**")
    
    # Handle cases where group call is not found
    except GroupCallNotFound:
        try:
            stream = await get_media_stream(media, stream_type)
            await call.join_group_call(chat_id, stream, auto_start=False)
            await add_to_queue(chat_id, media=media, type=stream_type)
            return await aux.edit("**Streaming Started ....**")
        
        # No active voice chat
        except NoActiveGroupCall:
            return await aux.edit("**No Active VC !**")
        
        # Assistant is already in the voice chat
        except AlreadyJoinedError:
            return await aux.edit("**Assistant Already in VC !**")
        
        # General exception handler
        except Exception as e:
            print(f"Error: {e}")
            return await aux.edit("**An error occurred. Please try again!**")
