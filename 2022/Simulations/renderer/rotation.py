import pygame
import math

class rotation():
    def __init__(self):
        self.thetax = 0
        self.thetay = 0
        self.thetaz = 0

    def move(self):
        dist = 2
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.thetax = (self.thetax - math.radians(dist) + math.radians(360)) % math.radians(360)
        elif keys[pygame.K_DOWN]:
            self.thetax = (self.thetax + math.radians(dist)) % math.radians(360)
        if keys[pygame.K_a]:
            self.thetay = (self.thetay - math.radians(dist) + math.radians(360)) % math.radians(360)
        elif keys[pygame.K_d]:
            self.thetay = (self.thetay + math.radians(dist)) % math.radians(360)
        if keys[pygame.K_LEFT]:
            self.thetaz = (self.thetaz - math.radians(dist) + math.radians(360)) % math.radians(360)
        elif keys[pygame.K_RIGHT]:
            self.thetaz = (self.thetaz + math.radians(dist)) % math.radians(360)

    def calc(self, table):
        new_table = []
        for point in table:
            temp = [0, 0, 0]
            temp[0] = (math.cos(self.thetax) * math.cos(self.thetay) * point[0]) + (math.cos(self.thetax) * math.sin(self.thetay) * math.sin(self.thetaz) - math.sin(self.thetax) * math.cos(self.thetaz)) * point[1] + (math.cos(self.thetax) * math.sin(self.thetay) * math.cos(self.thetaz) + math.sin(self.thetax) * math.sin(self.thetaz)) * point[2]
            temp[1] = (math.sin(self.thetax) * math.cos(self.thetay) * point[0]) + (math.sin(self.thetax) * math.sin(self.thetay) * math.sin(self.thetaz) + math.cos(self.thetax) * math.cos(self.thetaz)) * point[1] + (math.sin(self.thetax) * math.sin(self.thetay) * math.cos(self.thetaz) - math.cos(self.thetax) * math.sin(self.thetaz)) * point[2]
            temp[2] = (-math.sin(self.thetay) * point[0]) + (math.cos(self.thetay) * math.sin(self.thetaz) * point[1]) + (math.cos(self.thetay) * math.cos(self.thetaz) * point[2])
            new_table.append(temp)
        return new_table