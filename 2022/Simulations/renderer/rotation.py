import pygame
import math

class rotation():
    def __init__(self):
        self.__thetax = 0
        self.__thetay = 0
        self.__thetaz = 0
        self.__speed  = 2

    def __mod_up(self, n):
        return (n + math.radians(self.__speed)) % math.radians(360)
    
    def __mod_down(self, n):
        return (n - math.radians(self.__speed) + math.radians(360)) % math.radians(360)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.__thetax = self.__mod_down(self.__thetax)
        elif keys[pygame.K_DOWN]:
            self.__thetax = self.__mod_up(self.__thetax)
        if keys[pygame.K_a]:
            self.__thetay = self.__mod_down(self.__thetay)
        elif keys[pygame.K_d]:
            self.__thetay = self.__mod_up(self.__thetay)
        if keys[pygame.K_LEFT]:
            self.__thetaz = self.__mod_down(self.__thetaz)
        elif keys[pygame.K_RIGHT]:
            self.__thetaz = self.__mod_up(self.__thetaz)

    def calc(self, table):
        new_tbl = []
        x = self.__thetax
        y = self.__thetay
        z = self.__thetaz
        for point in table:
            temp = []
            temp.append((math.cos(x) * math.cos(y) * point[0]) + (math.cos(x) * math.sin(y) * math.sin(z) - math.sin(x) * math.cos(z)) * point[1] + (math.cos(x) * math.sin(y) * math.cos(z) + math.sin(x) * math.sin(z)) * point[2])
            temp.append((math.sin(x) * math.cos(y) * point[0]) + (math.sin(x) * math.sin(y) * math.sin(z) + math.cos(x) * math.cos(z)) * point[1] + (math.sin(x) * math.sin(y) * math.cos(z) - math.cos(x) * math.sin(z)) * point[2])
            temp.append((-math.sin(y) * point[0]) + (math.cos(y) * math.sin(z) * point[1]) + (math.cos(y) * math.cos(z) * point[2]))
            new_tbl.append(temp)
        return new_tbl