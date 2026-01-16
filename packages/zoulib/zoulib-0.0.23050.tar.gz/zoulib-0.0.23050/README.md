# zoulib
 
Текущая версия: **0.0.23050**
Скачивание видео из YouTube/TikTok

## Требования

- Python 3.10+
- Node.js для YouTube: https://nodejs.org/

## Функции

# yttik

- getlink(url) — создаёт объект видео по URL.

- get_info() — возвращает словарь с информацией о видео:

- title — название видео

- author — автор

- duration — длительность в секундах

- resolutions — доступные разрешения

- getdownload() — скачивает видео с выбранным качеством в папку ~/Downloads/yttik.
Видео скачивается с аудио и видео.

# web_checker

- goto(url) — переход на страницу

- get_html() — возвращает текущий HTML страницы (Selenium)

- get_title() — заголовок страницы

- click(selector) — клик по элементу через CSS-селектор

- type(selector, text) — ввод текста в поле

- get_info() — базовая инфа о сайте: URL, домен, поддомен, путь, статус, заголовок

- is_online() — проверка доступности сайта

- get_html_content() — HTML через requests

- send_request(method, data, headers) — отправка HTTP-запроса (GET/POST и т.д.)

- quit() — закрытие браузера