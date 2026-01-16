from zoulib.yttik.core import resolve_engine

class YTTik:
    def __init__(self, url: str):
        self._engine = resolve_engine(url)

    def getdownload(self):
        self._engine.download()

    def get_info(self):
        return self._engine.get_info()

def getlink(url: str):
    return YTTik(url)
