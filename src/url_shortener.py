from src.base62 import Base62
from src.database import Database
from src.bloom_filter import BloomFilter
from src.redis_client import RedisClient
from src.snowflake import Snowflake
import uuid

HOST = 'localhost'
PORT = 6380
EPOCH = 1700000000000
MACHINE_ID = uuid.getnode() % 1024
class URLShortener:
    def __init__(self, db_path="urls.db"):
        self.db = Database(db_path)
        self.bloom = BloomFilter(100000, 3)
        self.redis = RedisClient(HOST, PORT)
        self.snowflake = Snowflake(MACHINE_ID, EPOCH)
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
        # Id Generation using radis.
        # url_id = int(self.redis.incr("url_counter"))
        url_id = self.snowflake.generate()
        short_code = Base62.encode(url_id)
        self.db.save_url(url, short_code)
        self.redis.set(short_code, url)
        self.bloom.add(url)
        return short_code


    def redirect(self, short_code):
        url = self.redis.get(short_code) 
        if url is None:
            # id = Base62.decode(short_code)
            url = self.db.get_long_url(short_code)
            if url is not None: self.redis.set(short_code, url)
        return url
        