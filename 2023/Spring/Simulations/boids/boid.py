#This code has a lot of bugs : )
#The biggest one is a modular arithmetic problem at theta = 0. However, I am labeling that a feature and moving on
#Main controller class for each boid

import pygame
import random
import math

import t_angle

SPEED = 10
SIGHT = 100
SIGHT_THETA = 135
TWO_PI = math.radians(360)
COLORS = [(255, 0, 0), (255, 63, 0), (255, 127, 0), (255, 190, 0), (255, 255, 0), (127, 225, 0), (0, 255, 0), (0, 127, 127), (0, 0, 255), (63, 0, 255), (127, 0, 255)]

class boid():
    def __init__(self, dis, dis_dims, coords, id, debug):
        self.dis = dis
        self.dis_dims = dis_dims
        self.id = id
        self.__color = [random.randint(0, 255) for i in range(3)]
        self.__x, self.__y = coords
        self.__theta = math.radians(45)
        self.__target_angle = t_angle.t_angle(self.__theta)

        self.__evade_allow = True

    #Safe division function
    def __div(self, n, m):
        if not m:
            return 0
        return n / m

    #Calculates the sign of the input
    def __sign(self, n):
        return self.__div(n, abs(n))
    
    #Calculates the relative angle between two points, given the direction of the root point
    def __rel_theta(self, a, b, phi):
        theta = math.acos(self.__div((b[0] - a[0]), math.sqrt((b[1] - a[1])**2 + (b[0] - a[0])**2)))
        if self.__sign(math.asin(self.__div((b[1] - a[1]), math.sqrt((b[1] - a[1])**2 + (b[0] - a[0])**2)))) < 0:
            theta = TWO_PI - theta
        theta = (theta - phi + TWO_PI) % TWO_PI
        return (TWO_PI - theta) % TWO_PI

    #Modular arithmetic
    def __mod(self, n, mod = TWO_PI):
        return (n + mod) % mod
    
    #Returns the input, limited
    def __max(self, n, max):
        if abs(n) > max:
            return max * self.__sign(n)
        return n

    #Returns the distance between two points
    def __dist(self, a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    #Shell iteration function
    def itr(self, check_chunks):
            self.__check(check_chunks)
            self.__theta = self.__mod(self.__theta)
            self.__move()
            self.__draw()

    #Is fed a list of nearby boids and modifies the movement of this boid to compensate for them
    def __check(self, check_chunks):
        avg_turn = 0
        avg_pos = [0, 0]
        sight_boid_count = 0
        area_boid_count = 1
        for chunk in check_chunks:
            for boid in chunk:
                other_pos = boid.get_pos()
                if [self.__x, self.__y] != other_pos:
                    dist = self.__dist([self.__x, self.__y], other_pos)
                    if dist < SIGHT:
                        theta = self.__rel_theta([self.__x, self.__y], other_pos, self.__theta)
                        if (theta - 2 * self.__theta + math.radians(450)) % TWO_PI >= math.radians(360 - SIGHT_THETA / 2) or (theta - 2 * self.__theta + math.radians(450)) % TWO_PI <= math.radians(SIGHT_THETA / 2):
                            self.__evade(dist, theta)
                            self.__evade_allow = False
                            avg_turn += boid.get_theta()
                            avg_pos = [avg_pos[0] + (other_pos[0] - self.__x), avg_pos[1] + (other_pos[1] - self.__y)]
                            sight_boid_count += 1
                        avg_pos = [avg_pos[0] + (other_pos[0] - self.__x) / 10, avg_pos[1] + (other_pos[1] - self.__y) / 10]
                        area_boid_count += 1
        self.__match(self.__div(avg_turn, sight_boid_count))
        self.__jostle([self.__div(avg_pos[0], area_boid_count) + self.__x, self.__div(avg_pos[1], area_boid_count) + self.__y])
        self.__evade_allow = True
        self.__color = COLORS[len(COLORS) - 1 - (area_boid_count // 4 if area_boid_count < len(COLORS) * 4 else len(COLORS) - 1)]

    #!This code has bugs!  Each boid tries not to crash into other boids
    def __evade(self, dist, theta):
        rate = 1/7.5 #1 / 2
        theta -= self.__theta - math.radians(90)
        if self.__evade_allow:
            self.__theta -= self.__target_angle.deltatheta
            self.__theta -= (self.__target_angle.deltatheta * self.__sign(theta) * rate) % TWO_PI

    #!This code has bugs!  Each boid wants to match the angle of its friends
    def __match(self, avg_turn):
        self.__theta += self.__max(self.__div((self.__mod(avg_turn) - self.__mod(self.__theta)), 9), (SIGHT_THETA / 4) / 32)

    #Each boid wants to be in the center of its group
    def __jostle(self, avg_pos):
        self.__theta += self.__div(self.__rel_theta([self.__x, self.__y], avg_pos, self.__theta), 50)

    #Base movement controller for the boids
    def __move(self):
        self.__theta += self.__target_angle.get()
        self.__x = self.__mod(SPEED * math.sin(self.__theta) + self.__x, self.dis_dims.x)
        self.__y = self.__mod(SPEED * math.cos(self.__theta) + self.__y, self.dis_dims.y)

    #Draws the boid
    def __draw(self):
        scale = 25
        outline = 50
        p1 = [math.sin(self.__theta) / 2 * scale + self.__x, math.cos(self.__theta) / 2 * scale + self.__y]
        p2 = [math.sin(self.__theta + math.radians(225)) / 3 * scale + self.__x, math.cos(self.__theta + math.radians(225)) / 3 * scale + self.__y]
        p3 = [math.sin(self.__theta + math.radians(135)) / 3 * scale + self.__x, math.cos(self.__theta + math.radians(135)) / 3 * scale + self.__y]
        pygame.draw.polygon(self.dis, self.__color, [p1, p2, p3])
        pygame.draw.polygon(self.dis, [i - (outline if i - outline > 0 else i) for i in self.__color], [p1, p2, p3], 1)

    def get_pos(self):
        return [self.__x, self.__y]
    
    def get_theta(self):
        return self.__theta