from zoulib.yttik.engines.ytengine import YTDLPEngine
from zoulib.yttik.exceptions import UnsupportedPlatformError

def resolve_engine(url: str):
    lower_url = url.lower()
    if "youtube.com" in lower_url or "youtu.be" in lower_url:
        return YTDLPEngine(url)
    if "tiktok.com" in lower_url:
        return YTDLPEngine(url)
    raise UnsupportedPlatformError("Platform not supported")
