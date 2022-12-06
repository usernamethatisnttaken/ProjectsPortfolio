import pygame
import time

def quit1():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def move(pos, itr):
    x = pos[0]
    y = pos[1]
    z = pos[2]
    if itr > 0:
        itr -= 1
    if itr == 0:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= 1
            itr = 8
        elif keys[pygame.K_RIGHT]:
            x += 1
            itr = 8
        elif keys[pygame.K_UP]:
            z -= 1
            itr = 8
        elif keys[pygame.K_DOWN]:
            z += 1
            itr = 8
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            y -= 1
            itr = 8
        elif keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            y += 1
            itr = 8
    return [[x, y, z], itr]

def actions(itr2):
    if itr2 > 0:
        itr2 -= 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and itr2 == 0:
        return [True, True, 8]
    if keys[pygame.K_ESCAPE] and itr2 == 0:
        return [False, False, 8]
    return [False, True, itr2]

def draw(log, scale, pos, tag):
    a = scale / 2
    b = dis_dims/2
    if len(log) > 0 and tag == 'past':
        for i in range(len(log)):
            x = log[i][0]
            y = log[i][1]
            z = log[i][2]
            if y == pos[1]:
                pygame.draw.polygon(dis, 'black', [[b + x*scale + a, b + z*scale - a], [b + x*scale - a, b + z*scale - a], [b + x*scale - a, b + z*scale + a], [b + x*scale + a, b + z*scale + a]], 1)
    elif tag == 'current':
        x = log[0]
        z = log[2]
        pygame.draw.polygon(dis, 'red', [[b + x*scale + a, b + z*scale - a], [b + x*scale - a, b + z*scale - a], [b + x*scale - a, b + z*scale + a], [b + x*scale + a, b + z*scale + a]], 2)

def time_itr(x):
    start_time = time.time()
    time1 = 1
    while time1 == 1:
        if time.time() - start_time > x:
            time1 = 0

def main(dis_pre, dis_dims_pre):
    pos = [0, 0, 0]
    scale = 20
    itr = 0
    itr2 = 0
    cont = True
    backlog = []

    global dis
    dis = dis_pre

    global dis_dims
    dis_dims = dis_dims_pre

    while cont == True:
        dis.fill('white')
        if quit1() == False:
            return False

        a = move(pos, itr)
        pos = a[0]
        itr = a[1]
        a = actions(itr2)
        imprint = a[0]
        if cont == True:
            cont = a[1]
        itr2 = a[2]
        if imprint == True:
            add = True
            for i in range(len(backlog)):
                if backlog[i] == pos:
                    a = i
                    add = False
            if add == False:
                backlog.pop(a)
            if add == True:
                backlog.append(pos)

        draw(backlog, scale, pos, 'past')
        draw(pos, scale, pos, 'current')

        pygame.display.update()
        time_itr(0.03)

    return backlog