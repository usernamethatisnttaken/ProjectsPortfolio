import pygame
import random
import math

import boid

CHUNK_SCALE = 100
SHOW_TILES  = False
FAST_PLACE  = False
DEBUG = False

class model:
    def __init__(self, dis, dis_dims):
        self.dis = dis
        self.dis_dims = dis_dims
        self.__boid_count = 0
        self.__debug = False

        self.__board = {}
        for x in range(dis_dims.x // CHUNK_SCALE):
            self.__board[x] = {}
            for y in range(dis_dims.y // CHUNK_SCALE):
                self.__board[x][y] = []

        if not DEBUG:
            for i in range(10):
                self.__add_boid()
        else:
            self.__add_boid([400, 400])
            self.__add_boid([350, 450])

        self.ctrl_cool = 0

    def __add_boid(self, coords = None):
        if coords == None:
            radius = 50
            place_coords = [CHUNK_SCALE / 2 + random.randint(0, radius), CHUNK_SCALE / 2 + random.randint(0, radius)]
            self.__board[0][0].append(boid.boid(self.dis, self.dis_dims, place_coords, self.__boid_count, self.__debug and self.__boid_count == 1))
        else:
            if DEBUG:
                boid_push = boid.boid(self.dis, self.dis_dims, coords, self.__boid_count, False)
                self.__board[0][0].append(boid_push)
                if self.__boid_count == 1:
                    self.__debug_boid = boid_push
        self.__boid_count += 1

    def itr(self):
        self.__ctrl()

        new = {}
        for x in range(self.dis_dims.x // CHUNK_SCALE):
            new[x] = {}
            for y in range(self.dis_dims.y // CHUNK_SCALE):
                new[x][y] = []
        for x in self.__board:
            for y in self.__board[x]:
                tick = 0
                for boid in self.__board[x][y]:
                    carry = []
                    carry.append(self.__board[x - 1][y - 1]) if (x > 0 and y > 0) else None
                    carry.append(self.__board[x][y - 1]) if (y > 0) else None
                    carry.append(self.__board[x + 1][y - 1]) if (x < 14 and y > 0) else None
                    carry.append(self.__board[x - 1][y]) if (x > 0) else None
                    carry.append(self.__board[x][y])
                    carry.append(self.__board[x + 1][y]) if (x < 14) else None
                    carry.append(self.__board[x - 1][y + 1]) if (x > 0 and y < 8) else None
                    carry.append(self.__board[x][y + 1]) if (y < 8) else None
                    carry.append(self.__board[x + 1][y + 1]) if (x > 14 and y < 8) else None

                    boid.itr(carry)
                    new[boid.get_pos()[0] // CHUNK_SCALE][boid.get_pos()[1] // CHUNK_SCALE].append(self.__board[x][y][tick])
                    tick += 1
        self.__board = new

        self.__draw()

    def __ctrl(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_n]:
            if FAST_PLACE:
                for i in range(int(math.sqrt(self.__boid_count)) - 1):
                    self.__add_boid()
            self.__add_boid()
        if keys[pygame.K_m]:
            if not FAST_PLACE:
                for i in range(10):
                    self.__add_boid()
        if keys[pygame.K_d] and not self.ctrl_cool:
            self.__debug = abs(self.__debug - 1)
            self.ctrl_cool = 8
        if keys[pygame.K_r] and not self.ctrl_cool:
            self.__boid_count = 0
            self.__board = {}
            for x in range(self.dis_dims.x // CHUNK_SCALE):
                self.__board[x] = {}
                for y in range(self.dis_dims.y // CHUNK_SCALE):
                    self.__board[x][y] = []
            if not DEBUG:
                for i in range(10):
                    self.__add_boid()
            else:
                self.__add_boid([400, 400])
                self.__add_boid([350, 450])

        if self.ctrl_cool:
            self.ctrl_cool -= 1
        if DEBUG:
            self.__debug_boid.x, self.__debug_boid.y = pygame.mouse.get_pos()

    def __draw(self):
        if SHOW_TILES and self.__debug:
            for x in self.__board:
                z = x
                for y in self.__board[z]:
                    amount = len(self.__board[z][y])
                    x = z * CHUNK_SCALE
                    y = y * CHUNK_SCALE
                    pygame.draw.polygon(self.dis, "black", [[x, y], [x, y + CHUNK_SCALE], [x + CHUNK_SCALE, y + CHUNK_SCALE], [x + CHUNK_SCALE, y]], 1)
        tps = pygame.font.SysFont("Times New Roman", 10).render("boids: " + str(self.__boid_count), False, "black")
        self.dis.blit(tps, (self.dis_dims.x - 75, 15))