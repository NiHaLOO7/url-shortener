from src.base62 import Base62
from src.database import Database

class URLShortener:
    def __init__(self, db_path="urls.db"):
        self.db = Database(db_path)

    def shorten(self, url):
        short_code = self.db.get_short_code(url)
        if short_code is not None:
            return short_code
        id = self.db.save_url(url)
        short_code = Base62.encode(id)
        self.db.update_short_code(id, short_code)
        return short_code


    def redirect(self, short_code):
        id = Base62.decode(short_code)
        return self.db.get_long_url(id)
        