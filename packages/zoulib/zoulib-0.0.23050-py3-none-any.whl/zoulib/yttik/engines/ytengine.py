import os
import imageio_ffmpeg as ffmpeg
import yt_dlp
from zoulib.yttik.engines.base import BaseEngine
from zoulib.yttik.exceptions import DownloadFailedError

class YTDLPEngine(BaseEngine):
    def __init__(self, url: str):
        self.url = url
        self.info = None
        self.download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "yttik")
        os.makedirs(self.download_dir, exist_ok=True)
        self.ffmpeg_path = ffmpeg.get_ffmpeg_exe()
        self.selected_resolution = None

    def get_info(self):
        with yt_dlp.YoutubeDL({"quiet": True, "skip_download": True}) as ydl:
            self.info = ydl.extract_info(self.url, download=False)
        formats = self.info.get("formats", [])
        resolutions = sorted(
            set(
                f.get("format_note") if f.get("format_note") else (str(f.get("height")) + "p" if f.get("height") else None)
                for f in formats
                if f.get("ext") == "mp4"
            ),
            key=lambda x: int(x.replace("p","")) if x else 0
        )
        return {
            "title": self.info.get("title"),
            "author": self.info.get("uploader"),
            "duration": self.info.get("duration"),
            "resolutions": resolutions
        }

    def select_quality(self):
        info = self.get_info()
        resolutions = info["resolutions"]
        if not resolutions:
            print("Доступные качества не найдены, будет выбрано лучшее качество.")
            self.selected_resolution = None
            return
        print("Доступные качества:")
        for i, res in enumerate(resolutions, 1):
            print(f"{i}. {res}")
        choice = input(f"Выберите качество (1-{len(resolutions)}), Enter для лучшего: ")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(resolutions):
                self.selected_resolution = resolutions[idx]
            else:
                self.selected_resolution = None
        except:
            self.selected_resolution = None

    def download(self):
        if not self.info:
            self.get_info()
        self.select_quality()
        if self.selected_resolution:
            fmt = f"bestvideo[height<={self.selected_resolution.replace('p','')}]+bestaudio[ext=m4a]/best"
        else:
            fmt = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best"
        options = {
            "outtmpl": os.path.join(self.download_dir, "%(title)s.%(ext)s"),
            "format": fmt,
            "merge_output_format": "mp4",
            "ffmpeg_location": self.ffmpeg_path,
            "noplaylist": True,
            "quiet": False
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                ydl.download([self.url])
            except yt_dlp.utils.DownloadError as e:
                raise DownloadFailedError("Видео недоступно или ошибка при скачивании.") from e
            except Exception as e:
                raise DownloadFailedError(f"Неизвестная ошибка: {e}") from e
