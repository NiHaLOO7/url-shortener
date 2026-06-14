from src.base62 import Base62
from src.database import Database
from src.bloom_filter import BloomFilter

class URLShortener:
    def __init__(self, db_path="urls.db"):
        self.db = Database(db_path)
        self.bloom = BloomFilter(100000, 3)
        self._load_existing_urls()

    def _load_existing_urls(self):
        urls = self.db.get_all_urls()
        for url in urls:
            self.bloom.add(url[0])

    def shorten(self, url):
        if self.bloom.contains(url):
            short_code = self.db.get_short_code(url)
            if short_code is not None:
                return short_code
        id = self.db.save_url(url)
        short_code = Base62.encode(id)
        self.db.update_short_code(id, short_code)
        self.bloom.add(url)
        return short_code


    def redirect(self, short_code):
        id = Base62.decode(short_code)
        return self.db.get_long_url(id)
        