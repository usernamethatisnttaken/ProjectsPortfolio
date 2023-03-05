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
    def __init__(self, dis, dis_dims, coords, id, debug_carry):
        self.dis = dis
        self.dis_dims = dis_dims
        self.id = id
        self.__color = [random.randint(0, 255) for i in range(3)]
        self.__x, self.__y = coords
        self.__theta = math.radians(45)
        self.__theta_log = math.radians(45)
        self.__target_angle = t_angle.t_angle(self.__theta)

        self.__evade_allow = True

        self.__ctrl_cool = 0
        self.__debug = debug_carry

    def __div(self, n, m):
        if not m:
            return 0
        return n / m

    def __sign(self, n):
        return self.__div(n, abs(n))
    
    def __rel_theta(self, a, b, phi):
        theta = math.acos(self.__div((b[0] - a[0]), math.sqrt((b[1] - a[1])**2 + (b[0] - a[0])**2)))
        if self.__sign(math.asin(self.__div((b[1] - a[1]), math.sqrt((b[1] - a[1])**2 + (b[0] - a[0])**2)))) < 0:
            theta = TWO_PI - theta
        theta = (theta - phi + TWO_PI) % TWO_PI
        return (TWO_PI - theta) % TWO_PI

    def __mod(self, n, mod = TWO_PI):
        return (n + mod) % mod
    
    def __max(self, n, max):
        if abs(n) > max:
            return max * self.__sign(n)
        return n

    def __dist(self, a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def itr(self, check_chunks):
            self.__ctrl()
            self.__check(check_chunks)
            self.__theta = self.__mod(self.__theta)
            self.__move()
            self.__draw()

    def __ctrl(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and not self.__ctrl_cool:
            if not self.__debug and not self.id:
                self.__debug = True
                self.__ctrl_cool = 8
            elif self.__debug:
                self.__debug = False
                self.__ctrl_cool = 8

        if self.__ctrl_cool:
            self.__ctrl_cool -= 1

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
                            # if self.__debug:
                            #     pygame.draw.line(self.dis, "red", [self.__x, self.__y] ,[boid.get_pos()[0], boid.get_pos()[1]], 3)
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

    def __evade(self, dist, theta): #Also jank, but it kind of works and that is good enough for me for now
        rate = 1/7.5 #1 / 2
        theta -= self.__theta - math.radians(90)
        if self.__evade_allow:
            self.__theta -= self.__target_angle.deltatheta
            self.__theta -= (self.__target_angle.deltatheta * self.__sign(theta) * rate) % TWO_PI
        # if self.__debug:
        #     print(math.degrees(theta), math.degrees(self.__theta))
        #     pygame.draw.line(self.dis, "orange", [self.__x, self.__y], [SIGHT * math.sin(self.__theta) + self.__x, SIGHT * math.cos(self.__theta) + self.__x])
        #     pygame.draw.line(self.dis, "purple", [self.__x, self.__y], [SIGHT * math.sin(self.__theta - self.__target_angle.deltatheta * self.__sign(theta) * rate) + self.__x, SIGHT * math.cos(self.__theta - self.__target_angle.deltatheta * self.__sign(theta) * rate) + self.__x])

    def __match(self, avg_turn): #THIS IS ABSOLUTE JANK AND JUST BARELY WORKS
        self.__theta += self.__max(self.__div((self.__mod(avg_turn) - self.__mod(self.__theta)), 9), (SIGHT_THETA / 4) / 32)

    def __jostle(self, avg_pos):
        # if self.__debug:
        #     pygame.draw.line(self.dis, "blue", [self.__x, self.__y], avg_pos, 3)
        self.__theta += self.__div(self.__rel_theta([self.__x, self.__y], avg_pos, self.__theta), 50)

    def __move(self):
        self.__theta += self.__target_angle.get()
        new_x = SIGHT * math.sin(self.__theta) + self.__x
        new_y = SIGHT * math.cos(self.__theta) + self.__y
        if self.__debug:
            pygame.draw.line(self.dis, "yellow", [self.__x, self.__y], [new_x, new_y])
        self.__x, self.__y = self.__bound(new_x, new_y)
        

    def __bound(self, x, y):
        # rate = math.radians(15)
        # self.__theta = self.__mod(self.__theta)
        # x_down = (x < 0 and self.__theta < 270) or (x > self.dis_dims.x and self.__theta < 90)
        # y_down = (y < 0 and self.__theta < 180) or (y > self.dis_dims.y and self.__theta < 360)
        # x_up = (x < 0 and self.__theta > 270) or (x > self.dis_dims.x and self.__theta > 90)
        # y_up = (y < 0 and self.__theta > 180) or (y > self.dis_dims.y and self.__theta > 0)
        # if x_down or y_down:
        #     if self.__debug:
        #         print(True)
        #     self.__theta -= rate
        #     self.__target_angle.set(-rate)
        # if x_up or y_up:
        #     if self.__debug:
        #         print(True)
        #     self.__theta += rate
        #     self.__target_angle.set(rate)

        # max_theta = 10
        # if abs(self.__theta - self.__theta_log) > math.radians(max_theta):
        #     self.__theta = self.__theta_log + (math.radians(max_theta) * -self.__sign(self.__theta - self.__theta_log))
        # self.__theta_log = self.__theta

        new_x = self.__mod(SPEED * math.sin(self.__theta) + self.__x, self.dis_dims.x)
        new_y = self.__mod(SPEED * math.cos(self.__theta) + self.__y, self.dis_dims.y)
        return new_x, new_y

    def __draw(self):
        scale = 25
        outline = 50
        p1 = [math.sin(self.__theta) / 2 * scale + self.__x, math.cos(self.__theta) / 2 * scale + self.__y]
        p2 = [math.sin(self.__theta + math.radians(225)) / 3 * scale + self.__x, math.cos(self.__theta + math.radians(225)) / 3 * scale + self.__y]
        p3 = [math.sin(self.__theta + math.radians(135)) / 3 * scale + self.__x, math.cos(self.__theta + math.radians(135)) / 3 * scale + self.__y]
        pygame.draw.polygon(self.dis, self.__color, [p1, p2, p3])
        pygame.draw.polygon(self.dis, [i - (outline if i - outline > 0 else i) for i in self.__color], [p1, p2, p3], 1)
        # pygame.draw.polygon(self.dis, "black", [p1, p2, p3], 1)

        if self.__debug:
            pygame.draw.line(self.dis, "green", [self.__x, self.__y], [SIGHT * math.sin(math.radians(SIGHT_THETA / 2) + self.__theta) + self.__x, SIGHT * math.cos(math.radians(SIGHT_THETA / 2) + self.__theta) + self.__y], 1)
            pygame.draw.line(self.dis, "green", [self.__x, self.__y], [SIGHT * math.sin(math.radians(-SIGHT_THETA / 2) + self.__theta) + self.__x, SIGHT * math.cos(math.radians(-SIGHT_THETA / 2) + self.__theta) + self.__y], 1)

            sight_rect = pygame.rect.Rect(self.__x - SIGHT, self.__y - SIGHT, 2 * SIGHT, 2 * SIGHT)
            pygame.draw.arc(self.dis, "green", sight_rect, math.radians(-SIGHT_THETA / 2) + self.__theta - math.radians(90), math.radians(SIGHT_THETA / 2) + self.__theta - math.radians(90))
            pygame.draw.arc(self.dis, "red", sight_rect, math.radians(SIGHT_THETA / 2) + self.__theta - math.radians(90), math.radians(-SIGHT_THETA / 2) + self.__theta - math.radians(90))


    def get_pos(self):
        return [self.__x, self.__y]
    
    def get_theta(self):
        return self.__theta
    
    def __repr__(self):
        return "[" + str(self.__x) + ", " + str(self.__y) + "]"