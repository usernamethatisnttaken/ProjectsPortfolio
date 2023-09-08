from model3D import run         as model
from cubes   import seed_return as seeds
#from clear_texture import main  as clean
import pygame
import math
import time

scale = 20
dis_dims = 600
pygame.init()
dis = pygame.display.set_mode((dis_dims, dis_dims))
a = seeds(dis, dis_dims)
if a == False:
    pygame.quit()
    quit()
else:
    seed = a
white = (255, 255, 255)

def quit1():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def move(theta, tag):
    offset = 2
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and tag == 'x':
        theta += offset
    elif keys[pygame.K_RIGHT] and tag == 'x':
        theta -= offset
    if keys[pygame.K_UP] and tag == 'y':
        theta += offset
    elif keys[pygame.K_DOWN] and tag == 'y':
        theta -= offset
    if keys[pygame.K_q] and tag == 'z':
        theta += offset
    elif keys[pygame.K_e] and tag == 'z':
        theta -= offset
    
    if theta >= 360:
        theta = 0
    elif theta < 0:
        theta += 360
    return theta

def move2(theta, tag):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        a = 1
    elif keys[pygame.K_RIGHT]:
        a = 1
    elif keys[pygame.K_UP]:
        a = 1
    elif keys[pygame.K_DOWN]:
        a = 1
    elif keys[pygame.K_q]:
        a = 1
    elif keys[pygame.K_e]:
        a = 1
    if theta >= 360:
        theta = 0
    elif theta < 0:
        theta += 360
    return theta

def controls(itr2, select, rot):
    if itr2 > 0:
        itr2 -= 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RSHIFT] and itr2 == 0:
        itr2 = 8
        if select == True:
            select = False
        else:
            select = True
    if keys[pygame.K_r] and itr2 == 0:
        rot = [0, 0, 0]
    return [itr2, select, rot]

def aggr(seed, y, invert):
    seed_fix = []
    cut = True
    y -= 1
    posib = [1, 0, -1]
    if invert == True:
        for i in range(len(posib)):
            posib[i] = posib[i] * -1
    for i in range(len(seed)):
        if seed[i][y] == posib[0]:
            seed_fix.append(seed[i])
    for i in range(len(seed)):
        if seed[i][y] == posib[1]:
            seed_fix.append(seed[i])
    for i in range(len(seed)):
        if seed[i][y] == posib[2]:
            seed_fix.append(seed[i])
    return seed_fix

def adj(seed):
    adjacent = []
    for i in range(len(seed)):
        for j in range(len(seed) - 1):
            if j >= i:
                j += 1
            for k in range(len(seed[i])):
                if abs(seed[i][k] - seed[j][k]) <= 1:
                    if seed[i][k] - seed[j][k] != 0:
                        adjacent.append([i, k, seed[i][k] - seed[j][k]])
    return adjacent

def stack(seed, rot):
    if rot[0] > 180:
        seed = aggr(seed, 1, False)
    else:
        seed = aggr(seed, 1, True)
    if rot[0] < 270 and rot[0] > 0:
        seed = aggr(seed, 1, False)
    else:
        seed = aggr(seed, 1, True)
    if rot[1] < 90 or rot[1] > 270:
        seed = aggr(seed, 3, False)
    else:
        seed = aggr(seed, 3, True)
    return seed

def time_itr(x):
    start_time = time.time()
    time1 = 1
    while time1 == 1:
        if time.time() - start_time > x:
            time1 = 0

def main(seed, select):
    itr = 0
    itr2 = 0
    rot = [0, 0, 0]
    all_points = []
    cont = True
    while cont == True:
        cont = quit1()
        a = controls(itr2, select, rot)
        itr2 = a[0]
        select = a[1]
        rot = a[2]
        dis.fill(white)
        if select == False:
            rot = [move(rot[0], 'x'), move(rot[1], 'y'), move(rot[2], 'z')]
        if select == True:
            move2()
            
        #all_points = []
        #cleanup = adj(seed)
        for i in range(len(seed)):
            #all_points.append(model(scale, dis, dis_dims, seed[i], rot, False))
            model(scale, dis, dis_dims, seed[i], rot, False)#, cleanup[i])
        #clean(all_points, dis)

        pygame.display.update()
        time_itr(0.03)
        itr += 1

    pygame.quit()
    quit()

main(seed, False)