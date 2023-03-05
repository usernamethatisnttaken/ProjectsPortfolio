import random
import math

class t_angle:
    def __init__(self, current):
        self.deltatheta = 0
        self.duration = 0
        self.__update()

    def __min(self, x, y):
        if x <= y:
            return x
        return y

    def __update(self):
        scale = 1 / 40
        choice = [random.randint(-180, 180) for i in range(10)]
        prob = [self.__min(90 - abs(i) / 2, 30 + abs(i) / 2) for i in choice]
        self.deltatheta = math.radians(random.choices(choice, prob)[0] * scale)
        self.duration = random.randint(20, 40)

    def get(self):
        if self.duration:
            self.duration -= 1
        else:
            self.__update()
        return self.deltatheta
    
    def set(self, target):
        self.deltatheta = target
        self.duration = random.randint(20, 40)

    
    def peek(self):
        return self.deltatheta