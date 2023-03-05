import time

class dis_info():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class tps():
    def __init__(self, tps):
        self.length = 1 / tps
        self.start_time = 0
        self.slowmo = False

    def slow(self):
        if self.slowmo:
            self.slowmo = False
            self.length = self.length / 5
        else:
            self.slowmo = True
            self.length = self.length * 5
        return self.slowmo

    def start(self):
        self.start_time = time.perf_counter()

    def buffer(self):
        end_time = time.perf_counter()
        log = end_time
        while end_time < self.start_time + self.length:
            end_time = time.perf_counter()
        return log - self.start_time