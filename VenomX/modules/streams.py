import asyncio, re, yt_dlp

from VenomX import config
from pyrogram.types import Audio, Voice
from pyrogram.types import Video, VideoNote
from pytgcalls.types import AudioQuality, VideoQuality
from pytgcalls.types import MediaStream
from pytgcalls.types.raw import AudioParameters
from pytgcalls.types.raw import VideoParameters
from typing import Union
from youtubesearchpython.__future__ import VideosSearch


def get_audio_name(audio: Union[Audio, Voice]):
    try:
        file_name = (
            audio.file_unique_id
            + "."
            + (
                (audio.file_name.split(".")[-1])
                if (not isinstance(audio, Voice))
                else "ogg"
            )
        )
    except:
        file_name = audio.file_unique_id + "." + ".ogg"
        
    return file_name


def get_video_name(video: Union[Video, VideoNote]):
    try:
        file_name = (
            video.file_unique_id
            + "."
            + (video.file_name.split(".")[-1])
        )
    except:
        file_name = video.file_unique_id + "." + "mp4"
    
    return file_name
    

# Get Details Of Youtube Video
async def get_media_info(vidid: str, query: str):
    url = (
        f"https://www.youtube.com/watch?v={vidid}"
        if vidid else None
    )
    search = url if url else query
    results = VideosSearch(search, limit=1)
    for result in (await results.next())["result"]:
        videoid= vidid if vidid else result["id"]
        videourl = url if url else result["link"]

    return [videoid, videourl]



# Direct Link From YouTube
async def get_stream_link(link: str):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "bestvideo+bestaudio/best",
        "--cookies", "cookies.txt",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    links = stdout.decode().split('\n')
    return links[0], links[1]


# Stream Using PyTgCalls
async def get_media_stream(media, type: str):
    if type == "Audio":
        stream = MediaStream(
            media_path=media,
            video_flags=MediaStream.IGNORE,
            audio_parameters=AudioQuality.STUDIO,
        )
    elif type == "Video":
        stream = MediaStream(
            media_path=media,
            audio_parameters=AudioQuality.STUDIO,
            video_parameters=VideoQuality.HD_720p,
        )
            
    return stream
            
