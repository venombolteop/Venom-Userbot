import asyncio, os, yt_dlp


async def download_media_file(link: str, type: str):
    loop = asyncio.get_running_loop()
    if type == "Audio":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "no_warnings": True,
            "cookiefile": "cookies.txt",
        }

    elif type == "Video":
        ydl_opts = {
            "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "no_warnings": True,
            "cookiefile": "cookies.txt",
        }
        
    x = yt_dlp.YoutubeDL(ydl_opts)
    info = x.extract_info(link, False)
    file = os.path.join(
        "downloads", f"{info['id']}.{info['ext']}"
    )
    if os.path.exists(file):
        return file
    await loop.run_in_executor(None, x.download, [link])
    return file
