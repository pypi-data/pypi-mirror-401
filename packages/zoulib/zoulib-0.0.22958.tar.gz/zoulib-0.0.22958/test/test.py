from zoulib.yttik import getlink

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
video = getlink(url)
info = video.get_info()
print(f"Название: {info['title']}\nАвтор: {info['author']}\nДлительность: {info['duration']} сек\nДоступные качества: {info['resolutions']}")
video.getdownload()
