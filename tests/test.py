import unittest
import os
from src.url_shortener import URLShortener

class TestURLShortener(unittest.TestCase):

    def setUp(self):
        # fresh database for each test
        self.shortener = URLShortener(db_path="test_urls.db")

    def tearDown(self):
        # cleanup test database after each test
        os.remove("test_urls.db")

    def test_shorten_returns_code(self):
        # shorten karne pe short code milna chahiye
        url = 'www.google.com'
        sh = URLShortener()
        short = sh.shorten(url)
        self.assertTrue(len(short) > 0)

    def test_redirect_returns_correct_url(self):
        # short code se sahi long URL milni chahiye
        url = 'www.google.com'
        sh = URLShortener()
        short = sh.shorten(url)
        self.assertTrue(len(short) > 0)
        long = sh.redirect(short)
        self.assertEqual(long, url)

    def test_duplicate_url_same_code(self):
        # same URL dobara shorten karo — same code aana chahiye
        url1 = 'www.youtube.com'
        url2 = 'www.youtube.com'
        sh = URLShortener()
        short1 = sh.shorten(url1)
        short2 = sh.shorten(url2)
        self.assertEqual(short1,short2)

if __name__ == '__main__':
    unittest.main()
