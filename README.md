# URL Shortener

A URL shortener implementation from scratch in Python — no external libraries used.

Built as part of a series of open-source system design projects.

## How It Works

1. User submits a long URL
2. Server checks if URL already exists (duplicate prevention)
3. If new — inserts into SQLite, gets auto-increment ID
4. ID encoded to Base62 → short code
5. Short code stored back in database
6. On redirect — short code decoded → ID → long URL fetched → 302 redirect

## Algorithms & Concepts

### Base62 Encoding
Converts auto-increment integer IDs to short alphanumeric codes.
- Characters: `0-9` + `a-z` + `A-Z` = 62 total
- 6 characters → 56 billion unique URLs
- Offset applied to ensure minimum 6 character length

### Database Indexing
- `long_url` column is indexed for O(log n) duplicate lookup
- Without index — full table scan on 300TB+ data

## Data Structures (built from scratch)
- **Base62** — encode/decode with O(log₆₂ n) time, O(1) reverse lookup via hash map

## System Design

### Capacity Estimation
- 100M URLs shortened per day
- 10:1 read/write ratio → 1B redirects per day
- ~11,500 requests/second peak
- ~365TB storage over 5 years

### Architecture (Production)
```
User → Load Balancer → App Servers → Cache (Redis)
                                    ↓ (cache miss)
                              Sharded Database
```

- **Load Balancer** — distributes traffic, handles server failures
- **Redis Cache** — 80% redirects hit cache (Pareto principle), database not touched
- **Sharding** — 365TB doesn't fit one machine, consistent hashing distributes data
- **302 redirect** — not 301, so analytics work and links can be updated/deleted

### SQL vs NoSQL
Both work. At scale — NoSQL or sharded SQL preferred for horizontal scaling.

## Usage

```python
from src.url_shortener import URLShortener

s = URLShortener()
code = s.shorten("https://youtube.com/watch?v=abc123")
print(code)                # e.g. "4c93"
print(s.redirect(code))    # https://youtube.com/watch?v=abc123
```

## Run Tests

```bash
python3 -m unittest tests.test -v
```

## Demo Server

```bash
python3 demo.py
```

Shorten a URL:
```bash
curl -X POST http://localhost:8080/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com"}'
```

Redirect — open in browser:
```
http://localhost:8080/<short_code>
```

## Redis Integration (Mini Redis)

This project uses [mini-redis](https://github.com/NiHaLOO7/mini-redis) — a Redis implementation built from scratch as part of the same project series.

### Features Added
- **Redis Caching** — frequently accessed URLs cached in Redis for fast redirect (no DB hit)
- **Distributed ID Generation (Redis INCR)** — shared atomic counter across multiple servers
- **Snowflake ID Generator** — Twitter-style 64-bit unique IDs using timestamp + machine_id + sequence (no central dependency)

### How to Run (with Redis)

1. Start mini-redis (Docker):
```bash
cd ~/Desktop/Codes/GIT_PROJ/mini-redis
docker compose up --build
```

2. Run URL Shortener:
```bash
cd ~/Desktop/Codes/GIT_PROJ/url-shortener
python3 demo.py
```

3. Mini-redis runs on port `6380`, URL shortener connects automatically.

### Without Redis
If mini-redis is not running, `RedisClient` will throw `ConnectionRefusedError` on startup. To run without Redis, comment out the Redis lines in `url_shortener.py`.

## Project Structure

```
url-shortener/
├── src/
│   ├── base62.py          # Base62 encode/decode
│   ├── bloom_filter.py    # Bloom filter for duplicate check
│   ├── database.py        # SQLite operations
│   ├── redis_client.py    # TCP client for mini-redis
│   ├── snowflake.py       # Snowflake ID generator
│   └── url_shortener.py   # Core shorten/redirect logic
├── tests/
│   └── test.py            # Unit tests
├── demo.py                # HTTP server demo
└── requirements.txt
```

## Future Improvements
- Connection pooling
- TTL (link expiry)
- Click analytics
- Graceful fallback when Redis is down
