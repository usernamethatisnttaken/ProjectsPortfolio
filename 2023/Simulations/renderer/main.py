import pygame
import time

from board import board as board_cls
from place import place as place_cls
from mouse import mouse as mouse_cls

#Basic execution file for the module

TPS = 30
dis_dims = 800
pygame.init()
dis = pygame.display.set_mode((dis_dims, dis_dims))
pygame.display.set_caption('Renderer')

def quit1():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def time_itr(start_time, tps):
    end_time = time.perf_counter()
    while end_time < start_time + (1 / tps):
        end_time = time.perf_counter()

def run():
    mouse = mouse_cls()
    board = board_cls(dis)
    place = place_cls(dis, dis_dims, board, mouse)

    meta_cont = True
    cont = True
    while cont and meta_cont:
        timer = time.perf_counter()
        meta_cont = quit1()
        dis.fill('white')

        mouse.update()
        place.itr()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            cont = False

        pygame.display.update()
        time_itr(timer, TPS)

    cont = True
    while cont and meta_cont:
        timer = time.perf_counter()
        meta_cont = quit1()
        dis.fill('white')

        board.itr()

        pygame.display.update()
        time_itr(timer, TPS)
    pygame.quit()
    quit()

run()