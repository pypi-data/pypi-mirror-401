import os
import asyncio
import yt_dlp

async def download_youtube_video(url: str, output_dir: str = "temp") -> dict:
    """
    Скачивает видео с YouTube и возвращает путь к файлу и метаданные.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{output_dir}/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    # yt-dlp - синхронная библиотека, запускаем в треде, чтобы не блокировать asyncio
    loop = asyncio.get_event_loop()
    
    def _download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return {
                "path": filename,
                "title": info.get('title', 'No title'),
                "description": info.get('description', ''),
            }

    return await loop.run_in_executor(None, _download)
