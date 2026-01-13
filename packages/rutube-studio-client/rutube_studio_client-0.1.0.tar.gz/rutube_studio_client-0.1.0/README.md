# 📺 Rutube Studio Client

Асинхронная библиотека для управления видео на Rutube. Идеально для автоматизации, кросс-постинга и миграции контента.

## Фичи
- 🚀 **Полностью асинхронный** (на базе `httpx`)
- 📦 **Строгая типизация** (Pydantic v2)
- 📹 **YouTube Sync** — одной строкой кода переносит видео с YouTube на Rutube (включая название и описание).

## Установка

```bash
pip install rutube-studio
Использование
1. Загрузка видео с YouTube (Sync)
Python

import asyncio
from rutube import RutubeClient

async def main():
    client = RutubeClient(email="user@mail.ru", password="secure_pass")
    
    # Скачает с YouTube и зальет на Rutube
    await client.sync_from_youtube("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
2. Получение статистики
Python

videos = await client.get_my_videos()
for v in videos:
    print(f"{v.title}: {v.stats.views} views")