import os
import httpx
from typing import List, Optional
from .models import Video, UploadSession
from .exceptions import AuthError, UploadError
from .utils import download_youtube_video

class RutubeClient:
    BASE_URL = "https://rutube.ru/api"  # Проверить актуальный base url

    def __init__(self, email: str = None, password: str = None, token: str = None):
        self.email = email
        self.password = password
        self.token = token
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; RutubeStudioClient/0.1)",
            "Accept": "application/json"
        }
        self.client = httpx.AsyncClient(timeout=60.0)

    async def login(self):
        """Авторизация по логину/паролю, если нет токена"""
        if self.token:
            return
        
        # ! ВАЖНО: Эндпоинт нужно уточнить через сниффер
        response = await self.client.post(
            f"{self.BASE_URL}/accounts/token_auth/", 
            data={"username": self.email, "password": self.password}
        )
        
        if response.status_code != 200:
            raise AuthError(f"Login failed: {response.text}")
        
        data = response.json()
        self.token = data.get("token")
        self.headers["Authorization"] = f"Token {self.token}"

    async def get_my_videos(self) -> List[Video]:
        """Получение списка видео"""
        await self.login()
        resp = await self.client.get(f"{self.BASE_URL}/video/person/", headers=self.headers)
        resp.raise_for_status()
        # Предполагаем, что API возвращает { results: [...] }
        return [Video(**item) for item in resp.json().get('results', [])]

    async def upload_video(self, file_path: str, title: str, description: str = "") -> Video:
        """
        Загрузка видео. Обычно это 2 этапа: 
        1. Получить URL загрузки 
        2. Отправить файл
        """
        await self.login()

        # Шаг 1: Инициализация загрузки
        init_resp = await self.client.post(
            f"{self.BASE_URL}/video/upload/", 
            headers=self.headers,
            json={"title": title, "description": description}
        )
        init_data = init_resp.json()
        upload_url = init_data.get("upload_url") # Уточнить поле
        file_id = init_data.get("id")

        # Шаг 2: Отправка файла (Streaming)
        # Rutube может использовать PUT или POST multipart
        with open(file_path, "rb") as f:
            files = {'file': (os.path.basename(file_path), f)}
            # Внимание: для больших файлов лучше использовать генератор (read chunk)
            upload_resp = await self.client.post(upload_url, files=files, headers=self.headers)
        
        if upload_resp.status_code not in [200, 201]:
            raise UploadError(f"Upload failed: {upload_resp.text}")

        return Video(id=file_id, title=title, description=description)

    async def sync_from_youtube(self, youtube_url: str, publish: bool = True):
        """
        Киллер-фича: скачать с YT -> загрузить на Rutube
        """
        print(f"📥 Downloading from YouTube: {youtube_url}")
        video_data = await download_youtube_video(youtube_url)
        
        print(f"🚀 Uploading to Rutube: {video_data['title']}")
        try:
            rutube_video = await self.upload_video(
                file_path=video_data['path'],
                title=video_data['title'],
                description=video_data['description']
            )
            print(f"✅ Success! Rutube ID: {rutube_video.id}")
            return rutube_video
        finally:
            # Чистим за собой
            if os.path.exists(video_data['path']):
                os.remove(video_data['path'])

    async def close(self):
        await self.client.aclose()
