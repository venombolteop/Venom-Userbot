import re

from VenomX import app, call, cdz, eor
from VenomX import add_to_queue
from VenomX import download_media_file
from VenomX import get_media_info, get_media_stream
from pyrogram import filters
from pytgcalls.exceptions import AlreadyJoinedError, GroupCallNotFound
from pytgcalls.exceptions import NoActiveGroupCall


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
    if audiostream:
        media = await client.download_media(replied)
        type = "Audio"
    elif videostream:
        media = await client.download_media(replied)
        type = "Video"
    else:
        if len(message.command) < 2:
            return await aux.edit(
                "**🥀 Give Me Some Query To\nStream Audio Or Video❗...**"
            )
        query = message.text.split(None, 1)[1]
        if "https://" in query:
            base = r"(?:https?:)?(?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube(?:\-nocookie)?\.(?:[A-Za-z]{2,4}|[A-Za-z]{2,3}\.[A-Za-z]{2})\/)?(?:shorts\/|live\/)?(?:watch|embed\/|vi?\/)*(?:\?[\w=&]*vi?=)?([^#&\?\/]{11}).*$"
            resu = re.findall(base, query)
            vidid = resu[0] if resu[0] else None
        else:
            vidid = None
        results = await get_media_info(vidid, query)
        link = str(results[1])
        if command == "v":
            type = "Video"
        else:
            type = "Audio"
        media = await download_media_file(link, type)
    try:
        a = await call.get_call(chat_id)
        if a.status == "not_playing":
            stream = await get_media_stream(media, type)
            await call.change_stream(chat_id, stream)
            await add_to_queue(chat_id, media=media, type=type)
            return await aux.edit("**Streaming Started ....**")
        elif (a.status == "playing" or a.status == "paused"):
            position = await add_to_queue(chat_id, media=media, type=type)
            return await aux.edit(f"**Added to Queue At {position}**")
    except GroupCallNotFound:
        try:
            stream = await get_media_stream(media, type)
            await call.join_group_call(chat_id, stream, auto_start=False)
            await add_to_queue(chat_id, media=media, type=type)
            return await aux.edit("**Streaming Started ....**")
        except NoActiveGroupCall:
            return await aux.edit("**No Active VC !**")
        except AlreadyJoinedError:
            return await aux.edit("**Assistant Already in VC !**")
        except Exception as e:
            print(f"Error: {e}")
            return await aux.edit("**Please Try Again !**")
        except:
            return
