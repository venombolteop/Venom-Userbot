import asyncio
from VenomX import config
from VenomX.modules import queues
from VenomX.modules.clients import app, call
from VenomX.modules.streams import get_media_stream
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.types import AudioQuality, VideoQuality
from pytgcalls.types.stream import MediaStream
from typing import Union, List

def cdx(commands: Union[str, List[str]]):
    return filters.command(commands, config.COMMAND_PREFIXES)

def cdz(commands: Union[str, List[str]]):
    return filters.command(commands, config.COMMAND_HANDLERS)

async def eor(message: Message, *args, **kwargs) -> Message:
    try:
        msg = (
            message.edit_text
            if bool(message.from_user and message.from_user.is_self or message.outgoing)
            else (message.reply_to_message or message).reply_text
        )
    except Exception as e:
        print(f"Error editing or replying to message: {e}")
        msg = (
            message.edit_text
            if bool(message.from_user and message.outgoing)
            else (message.reply_to_message or message).reply_text
        )
    
    return await msg(*args, **kwargs)

async def call_decorators():
    async def handle_call_events():
        while True:
            try:
                # Check if the bot is in a group call and handle events
                chat_ids = await call.get_active_chats()
                for chat_id in chat_ids:
                    call_info = await call.get_call(chat_id)
                    if call_info.status in ["kicked", "closed", "left"]:
                        queue_empty = await queues.is_queue_empty(chat_id)
                        if not queue_empty:
                            await queues.clear_queue(chat_id)
                        try:
                            await call.leave_group_call(chat_id)
                        except Exception as e:
                            print(f"Error leaving group call: {e}")
                    
                    if call_info.status == "stream_ended":
                        # Handle the end of the stream
                        queue_empty = await queues.is_queue_empty(chat_id)
                        if queue_empty:
                            try:
                                await call.leave_group_call(chat_id)
                            except Exception as e:
                                print(f"Error leaving group call: {e}")
                            return
                        
                        check = await queues.get_from_queue(chat_id)
                        media = check["media"]
                        media_type = check["type"]
                        stream = await get_media_stream(media, media_type)
                        await call.change_stream(chat_id, stream)
                        await app.send_message(chat_id, "Streaming ...")
                
                # Sleep before checking again
                await asyncio.sleep(10)
            except Exception as e:
                print(f"Error in call decorators: {e}")

    # Run the event handler
    asyncio.create_task(handle_call_events())
