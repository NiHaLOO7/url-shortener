class Base62:
    CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    CHAR_MAP = {c: i for i, c in enumerate(CHARS)}
    OFFSET = 1000000
    def encode(num):
        num = num + Base62.OFFSET
        encoded = ''
        while num >= 62:
            rem = num % 62
            num = num // 62
            encoded = Base62.CHARS[rem] + encoded
        encoded = Base62.CHARS[num] + encoded
        return encoded
    
    def decode(code):
        num = 0
        for i in code:
            num = num * 62 + Base62.CHAR_MAP[i]
        return num - Base62.OFFSET
            
