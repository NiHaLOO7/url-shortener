import time
class Snowflake:
    def __init__(self, machine_id, epoch):
        self.machine_id = machine_id
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = 0

    def generate(self):
        timestamp = int(time.time() * 1000) - self.epoch
        if timestamp == self.last_timestamp:
            self.sequence += 1
            if self.sequence > 4095:
                while timestamp == self.last_timestamp:
                    timestamp = int(time.time() * 1000) - self.epoch
                self.sequence = 0
        else:
            self.sequence = 0

        self.last_timestamp = timestamp
        id = (timestamp << 22) | (self.machine_id << 12) | self.sequence
        return id