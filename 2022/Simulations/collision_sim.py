##DESC
#Another little simulation that attempts to attract a number of circles ('spheres') to the center
#but also not let them intersect - it doesn't work, but I like the progress on it and I spent a
#little bit of time on it. One of my many collision simulations

#Currently is finished, I would prefer to write another one than refactor this one, since I have
#a little bit more experience now

##CONFIG
night_mode = False     #inverts colors, for better night viewing
acceleration = 1     #acceleration toward the center point
air_resistance = 0.05     #what percentage of velocity is lost to air resistance every check
sphere_amount = 100

import pygame
import random
import time
import math

scale = 5
dis_dims = 800
pygame.init()
dis = pygame.display.set_mode((dis_dims, dis_dims))
pygame.display.set_caption('Collision Simulation')
dim_accel_at = 50
vel_resp_cutoff = 0.05

if night_mode:
    entity_col = 'white'
    screen_col = 'black'
else:
    entity_col = 'black'
    screen_col = 'white'
keys_dict = {0:pygame.K_0, 1:pygame.K_1, 2:pygame.K_2, 3:pygame.K_3, 4:pygame.K_4, 5:pygame.K_5, 6:pygame.K_6, 7:pygame.K_7, 8:pygame.K_8, 9:pygame.K_9}

class CircleGroup:
    __slots__ = ['__circle_list']

    def __init__(self, gen_number):
        self.__circle_list = []
        for i in range(gen_number):
            self.__circle_list.append(Circle([random.randint(-5, 5), random.randint(195, 205)], [random.randint(5, 20), random.randint(5, 20)]))

    def iterate(self, target_pos): #top function for all spheres
        for entity in self.__circle_list:
            entity.iterate(target_pos)
        self.collision_check()

    def collision_check(self): #checks for collisions between all spheres
        itr_num = len(self.__circle_list)
        for i in range(itr_num):
            working_circle = self.__circle_list.pop(0)
            for entity in range(len(self.__circle_list) - i):
                offset = working_circle.check_cols(self.__circle_list[entity].get_pos(), self.__circle_list[entity].get_vel(), self.__circle_list[entity].get_size())
                self.__circle_list[entity].collision_fix(offset)
            self.__circle_list.append(working_circle)

class Circle:
    __slots__ = ['__pos', '__vel', '__size', '__mass', '__color']

    def __init__(self, pos, vel, size = scale, mass = 1, color = entity_col):
        self.__pos   = pos
        self.__vel   = vel
        self.__size  = size
        self.__mass  = mass
        self.__color = color

    def get_pos(self):
        return self.__pos

    def get_vel(self):
        return self.__vel

    def get_size(self):
        return self.__size

    def iterate(self, target_pos): #top function for the working sphere
        self.air_resist()
        self.accelerate(target_pos)
        self.move()
        self.draw()

    def draw(self): #draws the circle
        if night_mode:
            pygame.draw.circle(dis, self.__color, mod(self.__pos), self.__size)
        else:
            pygame.draw.circle(dis, self.__color, mod(self.__pos), self.__size, width = 2)

    def accelerate(self, target_pos): #accelerates the sphere toward the center
        x_diff = target_pos[0] - self.__pos[0] #uses a component vector system
        y_diff = target_pos[1] - self.__pos[1]
        magnitude = math.sqrt(x_diff**2 + y_diff**2)

        rel_acceleration = math.sqrt(magnitude) / math.sqrt(dim_accel_at)
        if rel_acceleration > acceleration:
            rel_acceleration = acceleration

        factor = div(magnitude, rel_acceleration)
        add_vel = [div(x_diff, factor), div(y_diff, factor)]
        for i in range(len(self.__vel)):
            self.__vel[i] += add_vel[i] * (1 - air_resistance)

    def move(self): #moves the sphere by its velocity
        for i in range(len(self.__pos)):
            self.__pos[i] += self.__vel[i]

    def air_resist(self): #calculates air_resistance
        for i in range(len(self.__vel)):
            self.__vel[i] *= (1 - air_resistance)
            if abs(self.__vel[i]) < vel_resp_cutoff:
                self.__vel[i] = 0

    def check_cols(self, other_pos, other_vel, other_size): #checks collisions between this sphere and all others
        x_diff = self.__pos[0] - other_pos[0]
        y_diff = self.__pos[1] - other_pos[1]
        dist = math.sqrt(x_diff**2 + y_diff**2) - (self.__size + other_size)
        if dist < 0:
            mp = [(self.__pos[0] + other_pos[0]) / 2, (self.__pos[1] + other_pos[1]) / 2]
            delta_mp = math.sqrt((self.__pos[0] - mp[0])**2 + (self.__pos[1] - mp[1])**2)
            result = [(-1 * x_diff * dist / 2) / (delta_mp), (-1 * y_diff * dist / 2) / (delta_mp)]
            self.collision_fix(result)
            return [result[0] * -1, result[1] * -1]

    def collision_fix(self, offset): #acts on the collision detected above and TRYS to fix it
        if offset != None:
            for i in range(len(self.__vel)):
                self.__vel[i] += offset[i] / 2

def div(x, y): #simple no DivisionByZero function
    if y == 0:
        return 0
    return x / y

def mod(x): #modular function
    return [dis_dims / 2 + x[0], dis_dims / 2 + x[1]]

def quit1(): #closes the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def time_itr(x): #simple space function
    start_time = time.time()
    time1 = 1
    while time1 == 1:
        if time.time() - start_time > x:
            time1 = 0

def move(): #controls user inputs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        mov =  [mov[0] - scale, mov[1]]
    for i in keys_dict:
        if keys[keys_dict[i]]:
            global acceleration
            acceleration = i

def run():
    circle = CircleGroup(sphere_amount)

    cont = True
    while cont == True:
        cont = quit1()
        dis.fill(screen_col)

        move()
        circle.iterate([0, 0])

        pygame.display.update()
        time_itr(0.03)
    pygame.quit()
    quit()

run()