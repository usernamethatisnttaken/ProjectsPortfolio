import pygame

import polyhedron
import rotation

#Top modeling class - should be able to be used with different applicaitions (figuativaly)
class board:
    def __init__(self, dis):
        self.dis = dis
        self.__rotation = rotation.rotation()
        self.__focal_length = 10
        self.__polyhedra = {}
        self.__scale = [32]

    def add_polyhedron(self, coords): #Adds a polyhedron to the board
        if coords[0] not in self.__polyhedra:
            self.__polyhedra[coords[0]] = {}
        if coords[1] not in self.__polyhedra[coords[0]]:
            self.__polyhedra[coords[0]][coords[1]] = {}
        
        self.__polyhedra[coords[0]][coords[1]][coords[2]] = polyhedron.polyhedron(self.dis, "cubular", coords, self.__focal_length, self.__rotation, self.__scale)

    def rmv_polyhedron(self, coords): #Removes a polyhedron from the board
        if coords[0] in self.__polyhedra:
            if coords[1] in self.__polyhedra[coords[0]]:
                if coords[2] in self.__polyhedra[coords[0]][coords[1]]:
                    self.__polyhedra[coords[0]][coords[1]].pop(coords[2])

    def get_polyhedron(self, coords): #Returns the polyhedron object at the specified coords
        if coords[0] in self.__polyhedra:
            if coords[1] in self.__polyhedra[coords[0]]:
                if coords[2] in self.__polyhedra[coords[0]][coords[1]]:
                    return self.__polyhedra[coords[0]][coords[1]][coords[2]]
        return None

    def itr(self):
        self.__move()
        self.__rotation.move()

        draw_priority = []
        for x in self.__polyhedra:
            for y in self.__polyhedra[x]:
                for z in self.__polyhedra[x][y]:
                    draw_priority.append(self.__polyhedra[x][y][z])
        for polyhedron in draw_priority:
            polyhedron.adjust()
        draw_priority = sorted(draw_priority, key = lambda polyhedron: polyhedron.score, reverse = True)
        for polyhedron in draw_priority:
            polyhedron.draw()

    def __move(self): #Scaling controller
        dist = 0.5
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] and self.__scale[0] > dist:
            self.__scale[0] -= dist
        elif keys[pygame.K_w]:
            self.__scale[0] += dist