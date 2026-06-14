class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.bits = bytearray(size//8 + 1)
        # Multiple checks -> all will pass for same url, otherwise fail
        self.num_hashes = num_hashes

    def _set_bit(self, position):
        byte_index = position // 8
        bit_index = position % 8
        self.bits[byte_index] = self.bits[byte_index] | (1 << bit_index)

    def _check_bit(self, position):
        byte_index = position // 8
        bit_index = position % 8
        return self.bits[byte_index] & (1 << bit_index) != 0
    
    def _get_hash(self, item, seed):
        h = seed  # start from seed
        PRIME = 31
        for c in item:
            h = (h * PRIME + ord(c)) % self.size
        return h
    
    def add(self, item):
        for i in range(self.num_hashes):
            item_hash = self._get_hash(item, i)
            self._set_bit(item_hash)

    def contains(self, item):
        for i in range(self.num_hashes):
            item_hash = self._get_hash(item, i)
            if not self._check_bit(item_hash):
                return False
        return True
    
