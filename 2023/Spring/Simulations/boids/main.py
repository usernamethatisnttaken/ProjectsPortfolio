#Base visuals for the project

import pygame

from mech import dis_info
from mech import tps as tps_cls

import model

TPS = tps_cls(tps = 20)
dis_dims = dis_info(x = 1500, y = 900)
pygame.init()
dis = pygame.display.set_mode((dis_dims.x, dis_dims.y))
pygame.display.set_caption('Boids')

COOLDOWN = 0

def quit1(cooldown):
    deltacool = 0
    if cooldown:
        deltacool = -1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_F11] and not cooldown:
        pygame.display.toggle_fullscreen()
        deltacool = 8

    if keys[pygame.K_s] and not cooldown:
        if not TPS.slow():
            deltacool = 8
        else:
            deltacool = 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    global COOLDOWN
    COOLDOWN += deltacool
    return True

def disp_ticksp(tickspeed):
    col = "black"
    if tickspeed > TPS.length:
        col = "red"
    tps = pygame.font.SysFont("Times New Roman", 10).render("tps: " + str(tickspeed) + "/" + str(TPS.length), False, col)
    dis.blit(tps, (dis_dims.x - 75, 5))

def run():
    board = model.model(dis, dis_dims)

    tickspeed = 0
    cont = True
    while cont:
        TPS.start()
        cont = quit1(COOLDOWN)
        dis.fill('white')

        board.itr()

        disp_ticksp(tickspeed)
        pygame.display.update()
        tickspeed = round(TPS.buffer(), 3)
    pygame.quit()
    quit()

run()