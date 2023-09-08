import pygame

class place: #Class that executes the polyhedron placing !Currently only works on a cubed projection!
    MAX_COOL = 5

    def __init__(self, dis, dis_dims, board, mouse):
        self.dis = dis
        self.dis_dims = dis_dims
        self.__board = board
        self.__mouse = mouse
        self.__log = {}
        self.__scale = 25
        self.__cooldown = 0
        self.__z = 0

    def __rescale(self, n): #Helper function to switch between real and symbolic coordinates
        return n // self.__scale

    def itr(self):
        self.__move()
        self.__draw()
        if self.__cooldown:
            self.__cooldown -= 1

    def __move(self): #User input controller
        coords = [self.__rescale(self.__mouse.x) - self.__rescale(self.dis_dims) / 2, self.__rescale(self.__mouse.y) - self.__rescale(self.dis_dims) / 2, self.__z]
        if self.__mouse.rclick:
            if self.__board.get_polyhedron(coords) == None:
                self.__board.add_polyhedron(coords)
                if self.__z not in self.__log:
                    self.__log[self.__z] = []
                self.__log[self.__z].append(coords[0:2])

        if self.__mouse.lclick:
            self.__board.rmv_polyhedron(coords)
            if self.__z in self.__log:
                for i in range(len(self.__log[self.__z])):
                    if self.__log[self.__z][i] == coords[0:2]:
                        self.__log[self.__z].pop(i)
                        break

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and not self.__cooldown:
            self.__z += 1
            self.__cooldown = self.MAX_COOL
        elif (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and not self.__cooldown:
            self.__z -= 1
            self.__cooldown = self.MAX_COOL

    def __draw(self):
        scale = self.__scale
        for x in range(self.__rescale(self.dis_dims)):
            for y in range(self.__rescale(self.dis_dims)):
                width = 1
                col = "black"
                if [x, y] == [self.__rescale(self.__mouse.x), self.__rescale(self.__mouse.y)]:
                    width = 3
                    col = "red"
                pygame.draw.polygon(self.dis, col, [[x * scale, y * scale], [(x + 1) * scale, y * scale], [(x + 1) * scale, (y + 1) * scale], [x * scale, (y + 1) * scale]], width)

        max_shadow = 10
        offset = 1
        for z in self.__log:
            diff = (z - self.__z) * offset
            if diff < 0 and diff > -max_shadow:
                for coords in self.__log[z]:
                    col = (255 / (max_shadow) * -diff, 255 / (max_shadow) * -diff, 255 / (max_shadow) * -diff)
                    pygame.draw.line(self.dis, col, [(coords[0] + self.__rescale(self.dis_dims) / 2) * scale - diff, (coords[1] + self.__rescale(self.dis_dims) / 2) * scale - diff], [(coords[0] + self.__rescale(self.dis_dims) / 2) * scale + scale - 0.005, (coords[1] + self.__rescale(self.dis_dims) / 2) * scale - diff])
                    pygame.draw.line(self.dis, col, [(coords[0] + self.__rescale(self.dis_dims) / 2) * scale - diff, (coords[1] + self.__rescale(self.dis_dims) / 2) * scale - diff], [(coords[0] + self.__rescale(self.dis_dims) / 2) * scale - diff, (coords[1] + self.__rescale(self.dis_dims) / 2) * scale + scale - 0.005])
            if diff == 0:
                for coords in self.__log[z]:
                    px = (coords[0] + self.__rescale(self.dis_dims) / 2) * scale
                    py = (coords[1] + self.__rescale(self.dis_dims) / 2) * scale
                    pygame.draw.polygon(self.dis, col, [[px, py], [px + scale, py], [px + scale, py + scale], [px, py + scale]], 2)
            if diff > 0 and diff < max_shadow:
                for coords in self.__log[z]:
                    col = (255 / (max_shadow) * diff, 255 / (max_shadow) * diff, 255 / (max_shadow) * diff)
                    pygame.draw.line(self.dis, col, [(coords[0] + self.__rescale(self.dis_dims) / 2) * scale - diff, (coords[1] + self.__rescale(self.dis_dims) / 2) * scale - diff], [(coords[0] + self.__rescale(self.dis_dims) / 2) * scale + scale + 0.005 - diff, (coords[1] + self.__rescale(self.dis_dims) / 2) * scale - diff])
                    pygame.draw.line(self.dis, col, [(coords[0] + self.__rescale(self.dis_dims) / 2) * scale - diff, (coords[1] + self.__rescale(self.dis_dims) / 2) * scale - diff], [(coords[0] + self.__rescale(self.dis_dims) / 2) * scale - diff, (coords[1] + self.__rescale(self.dis_dims) / 2) * scale + scale + 0.005 - diff])
        
        z_ind = pygame.font.SysFont("Times New Roman", 10).render("Z:" + str(self.__z), False, (0, 0, 0))
        self.dis.blit(z_ind, (self.dis_dims - scale + 2, self.dis_dims - scale))