import pygame

class mouse: #A controller that houses all of the information relevant to the mouse
    def __init__(self):
        self.x = 0
        self.y = 0
        self.rclick = False
        self.lclick = False

    def update(self):
        pos = pygame.mouse.get_pos()
        self.x = pos[0]
        self.y = pos[1]

        down = pygame.mouse.get_pressed()
        self.rclick = down[0]
        self.lclick = down[2]