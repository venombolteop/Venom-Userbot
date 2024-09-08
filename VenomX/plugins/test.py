from VenomX import app, call, cdz
from pyrogram import filters
from pytgcalls.types import AudioQuality, VideoQuality
from pytgcalls.types.stream import MediaStream  # Adjust based on available imports
from VenomX import get_media_stream  # Ensure this function is defined to handle stream extraction

@app.on_message(cdz(["stream"]) & ~filters.private)
async def test_media_stream(client, message):
    if message.sender_chat:
        return
    
    chat_id = message.chat.id
    url = "https://www.youtube.com/watch?v=wjvyh7V39u4"  # Example URL, replace as needed
    
    # Get media stream (audio and/or video) based on URL and quality
    stream = await get_media_stream(url, stream_type="Video", audio_quality=AudioQuality.HIGH, video_quality=VideoQuality.HD_720p)
    
    try:
        # Join the group call and start the stream
        await call.join_group_call(chat_id, stream)
    except Exception as e:
        # If already joined, change the stream
        try:
            await call.change_stream(chat_id, stream)
        except Exception as inner_e:
            # Handle any other exceptions
            print(f"Error changing stream: {inner_e}")
    except Exception as e:
        # Handle any other exceptions
        print(f"Error joining group call: {e}")
