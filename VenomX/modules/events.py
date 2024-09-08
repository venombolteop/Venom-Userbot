from VenomX import config
from VenomX.modules import queues
from VenomX.modules.clients import app, call
from VenomX.modules.streams import get_media_stream
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.stream import StreamAudioEnded
from typing import Union, List

# Assuming 'call' is an instance of PyTgCalls
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
    except:
        msg = (
            message.edit_text
            if bool(message.from_user and message.outgoing)
            else (message.reply_to_message or message).reply_text
        )
    
    return await msg(*args, **kwargs)

# Define a function to handle streaming updates
async def handle_stream_updates():
    while True:
        updates = await call.get_updates()
        for update in updates:
            if isinstance(update, StreamAudioEnded):
                await on_stream_end_handler(update)
            # Add other event types and handlers as needed

async def on_stream_end_handler(update: Update):
    if not isinstance(update, StreamAudioEnded):
        return
    chat_id = update.chat_id
    await queues.task_done(chat_id)
    queue_empty = await queues.is_queue_empty(chat_id)
    if queue_empty:
        try:
            await call.leave_group_call(chat_id)
        except Exception as e:
            print(f"Error leaving group call: {e}")
            return
    check = await queues.get_from_queue(chat_id)
    media = check["media"]
    type = check["type"]
    stream = await get_media_stream(media, type)
    await call.change_stream(chat_id, stream)
    await app.send_message(chat_id, "Streaming ...")

async def on_kicked_handler(chat_id: int):
    queue_empty = await queues.is_queue_empty(chat_id)
    if not queue_empty:
        await queues.clear_queue(chat_id)
    try:
        await call.leave_group_call(chat_id)
    except Exception as e:
        print(f"Error leaving group call: {e}")

async def on_closed_voice_chat_handler(chat_id: int):
    await on_kicked_handler(chat_id)

async def on_left_handler(chat_id: int):
    await on_kicked_handler(chat_id)

# You need to start the event handler in your main loop or a background task
# Example of starting the handler function
import asyncio
async def main():
    await handle_stream_updates()

# Run your main function (make sure to integrate with your existing application loop)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
