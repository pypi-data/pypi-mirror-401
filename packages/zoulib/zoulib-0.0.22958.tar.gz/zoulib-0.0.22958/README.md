# zoulib
 
Текущая версия: **0.0.22958**
Скачивание видео из YouTube/TikTok

## Требования

- Python 3.10+
- ffmpeg для объединения аудио и видео: https://ffmpeg.org/
- Node.js для YouTube: https://nodejs.org/

## Использование

```python
from zoulib.yttik import getlink

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
video = getlink(url)

info = video.get_info()
print(f"Название: {info['title']}")
print(f"Автор: {info['author']}")
print(f"Длительность: {info['duration']} сек")
print(f"Доступные качества: {info['resolutions']}")

video.getdownload()
```


## Функции

- getlink(url) — создаёт объект видео по URL.

- get_info() — возвращает словарь с информацией о видео:

- title — название видео

- author — автор

- duration — длительность в секундах

- resolutions — доступные разрешения

- getdownload() — скачивает видео с выбранным качеством в папку ~/Downloads/yttik.
Видео скачивается с аудио и видео.