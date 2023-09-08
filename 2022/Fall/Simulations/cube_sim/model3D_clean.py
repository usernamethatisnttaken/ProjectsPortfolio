from dis import dis
from re import A
import pygame
import math
import time

scale = 5
dis_dims = 600
pygame.init()
dis = pygame.display.set_mode((dis_dims, dis_dims))
pygame.display.set_caption('')

class Square:
    def __init__(self, x):
        self.a = [x[0], x[1]]
        self.b = [x[1], x[2]]
        self.c = [x[2], x[3]]
        self.d = [x[3], x[0]]

class Coord:
    def __init__(self, pos, dims):
        self.sqrs = []
        self.sqrs.append(Square([[pos[0] - dims / 2, pos[1] + dims / 2], [pos[0] + dims / 2, pos[1] + dims / 2], [pos[0] + dims / 2, pos[1] - dims / 2], [pos[0] - dims / 2, pos[1] - dims / 2]]))
        self.sqrs.append(Square([[pos[0] + dims / 2, pos[1] + dims / 2], [pos[0] + dims / 2, pos[1] + dims / 2], [pos[0] + dims / 2, pos[1] - dims / 2], [pos[0] + dims / 2, pos[1] + dims / 2]]))
        self.sqrs.append(Square([[pos[0] + dims / 2, pos[1] + dims / 2], [pos[0] - dims / 2, pos[1] + dims / 2], [pos[0] - dims / 2, pos[1] - dims / 2], [pos[0] + dims / 2, pos[1] - dims / 2]]))
        self.sqrs.append(Square([[pos[0] - dims / 2, pos[1] + dims / 2], [pos[0] - dims / 2, pos[1] + dims / 2], [pos[0] - dims / 2, pos[1] - dims / 2], [pos[0] - dims / 2, pos[1] - dims / 2]]))
        self.sqrs.append(Square([[pos[0] + dims / 2, pos[1] + dims / 2], [pos[0] + dims / 2, pos[1] + dims / 2], [pos[0] - dims / 2, pos[1] + dims / 2], [pos[0] - dims / 2, pos[1] + dims / 2]]))
        self.sqrs.append(Square([[pos[0] - dims / 2, pos[1] - dims / 2], [pos[0] - dims / 2, pos[1] - dims / 2], [pos[0] + dims / 2, pos[1] - dims / 2], [pos[0] + dims / 2, pos[1] - dims / 2]]))

class Cube:
    def __init__(self, pos, dims):
        self.pos    = pos
        self.dims   = dims
        self.coords = Coord(pos, dims)
        self.theta  = [0, 0, 0]

    def coord_update(self):
        for i in range(len(self.theta)):
            self.theta[i] = math.radians(self.theta[i])
        self.coords = Coord(self.pos, self.dims)
        self.coords.sqrs[0] = Square([[math.cos(self.theta[2]) * self.coords.sqrs[0].a[0][0], math.sin(self.theta[2]) * self.coords.sqrs[0].a[0][1]], [math.sin(self.theta[2]) * self.coords.sqrs[0].b[0][0], math.cos(self.theta[2]) * self.coords.sqrs[0].b[0][1]], [math.sin(self.theta[2]) * self.coords.sqrs[0].c[0][0], math.cos(self.theta[2]) * self.coords.sqrs[0].c[0][1]], [math.cos(self.theta[2]) * self.coords.sqrs[0].d[0][0], math.sin(self.theta[2]) * self.coords.sqrs[0].d[0][1]]]) #flipped sin and cos for every other one
        self.coords.sqrs[2] = Square([[math.cos(self.theta[2]) * self.coords.sqrs[2].a[0][0], math.sin(self.theta[2]) * self.coords.sqrs[2].a[0][1]], [math.cos(math.radians(180) - self.theta[2]) * self.coords.sqrs[2].b[0][0], math.sin(math.radians(180) - self.theta[2]) * self.coords.sqrs[2].b[0][1]], [math.cos(math.radians(180) - self.theta[2]) * self.coords.sqrs[2].c[0][0], math.sin(math.radians(180) - self.theta[2]) * self.coords.sqrs[2].c[0][1]], [math.cos(self.theta[2]) * self.coords.sqrs[2].d[0][0], math.sin(self.theta[2]) * self.coords.sqrs[2].d[0][1]]])
        for i in range(len(self.theta)):
            self.theta[i] = math.degrees(self.theta[i])

    def rotate(self, theta):
        self.theta = [self.theta[0] + theta[0], self.theta[1] + theta[1]]
        for i in range(len(self.theta)):
            if self.theta[i] >= 360:
                self.theta[i] = 0
            elif self.theta[i] < 0:
                self.theta[i] += 360
        self.coord_update()

def quit1():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def time_itr(x):
    start_time = time.time()
    time1 = 1
    while time1 == 1:
        if time.time() - start_time > x:
            time1 = 0

def mod(x):
    y = [0, 0]
    y[0] = dis_dims / 2 + float(x[0]) * scale
    y[1] = dis_dims / 2 - float(x[1]) * scale
    return y

def draw_cube(cube):
    for i in cube.coords.sqrs:
        pygame.draw.line(dis, 'black', mod(i.a[0]), mod(i.a[1]))
        pygame.draw.line(dis, 'black', mod(i.b[0]), mod(i.b[1]))
        pygame.draw.line(dis, 'black', mod(i.c[0]), mod(i.c[1]))
        pygame.draw.line(dis, 'black', mod(i.d[0]), mod(i.d[1]))

def move(theta):
    offset = 2
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        theta[0] += offset
    elif keys[pygame.K_RIGHT]:
        theta[0] -= offset
    if keys[pygame.K_UP]:
        theta[1] += offset
    elif keys[pygame.K_DOWN]:
        theta[1] -= offset
    return theta

def run():
    cube1 = Cube([0, 0], 10)

    theta = [0, 0]
    cont = True
    while cont == True:
        cont = quit1()
        dis.fill('white')

        #cube1.rotate(move([0, 0]))
        #draw_cube(cube1)
        #Asin(x_theta - offset)*sin(y_theta) + (Acos(y_theta))/sqrt(2)), Acos(x_theta - offset)*sin(y_theta)

        theta = move(theta)
        for i in range(len(theta)):
            theta[i] = math.radians(theta[i])
        dims = 100
        points = []
        for j in [-1, 1]:
            for i in [0, math.pi/2, math.pi, 3*math.pi/2]:
                points.append([dims * math.sin(theta[0] + i) * math.sin(theta[1]) + j * (dims * math.cos(theta[1] / math.sqrt(2))), dims * math.cos(theta[0] + i) * math.sin(theta[1])])
        # for i in range(len(points)):
        #     points[i] = (dis_dims / 2) + points[i][0], (dis_dims / 2) - points[i][1]
        for i in [0, 4]:
            pygame.draw.line(dis, 'black', points[0 + i], points[1 + i])
            pygame.draw.line(dis, 'black', points[1 + i], points[2 + i])
            pygame.draw.line(dis, 'black', points[2 + i], points[3 + i])
            pygame.draw.line(dis, 'black', points[3 + i], points[0 + i])
        for i in range(len(theta)):
            theta[i] = math.degrees(theta[i])

        pygame.display.update()
        time_itr(0.03)
    pygame.quit()
    quit()

run()