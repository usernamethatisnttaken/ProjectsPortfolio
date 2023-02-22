import pygame

from plane import plane as plane

debug = True

class polyhedron():
    def __init__(self, dis, type, coords, focal_length, rotation, scale):
        self.__coords = coords
        self.__focal_length  = focal_length
        self.__rotation  = rotation
        self.dis   = dis
        self.__scale = scale
        self.score = (sum(coords) + (len(coords) * 0.5)) / len(coords)
        self.__generate_nodes(type)
        self.__generate_edges(type)
        self.__generate_sides(type)
        self.adjust()

    def __fit(self, n):
        return n * self.__scale[0] + 400

    def __project_vertex(self, vertex, focal_length):
        x, y, z = vertex

        new_x = (focal_length * x) / (z + focal_length)
        new_y = (focal_length * y) / (z + focal_length)

        return [new_x, new_y]

    # def itr(self):
    #     self.adjust()
    #     self.draw()

    def __generate_nodes(self, type):
        if type == "cubular":
            self.__d3_node_table = []
            for x in [self.__coords[0], self.__coords[0] + 1]:
                for y in [self.__coords[1], self.__coords[1] + 1]:
                    for z in [self.__coords[2], self.__coords[2] + 1]:
                        self.__d3_node_table.append([x, y, z])

    def __generate_edges(self, type):
        if type == "cubular":
            self.__edge_table = [
                [0, 1],
                [0, 2],
                [0, 4],
                [1, 5],
                [1, 3],
                [2, 6],
                [2, 3],
                [3, 7],
                [4, 5],
                [4, 6],
                [5, 7],
                [6, 7]
            ]

    def __generate_sides(self, type):
        colors  = ["gray" for i in range(6)]
        if debug:
            colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        if type == "cubular":
            self.__side_table = [
                plane([0, 1, 3, 2], self.__d3_node_table, colors[0]),
                plane([4, 5, 7, 6], self.__d3_node_table, colors[1]),
                plane([0, 1, 5, 4], self.__d3_node_table, colors[2]),
                plane([2, 3, 7, 6], self.__d3_node_table, colors[3]),
                plane([0, 2, 6, 4], self.__d3_node_table, colors[4]),
                plane([1, 3, 7, 5], self.__d3_node_table, colors[5])
            ]

    def adjust(self):
        self.__d2_node_table = []
        temp_tbl = self.__rotation.calc(self.__d3_node_table)
        for node in temp_tbl:
            self.__d2_node_table.append(self.__project_vertex(node, self.__focal_length))

        for plane in self.__side_table:
            plane.update(temp_tbl)

        self.score = 0
        for i in range(len(temp_tbl)):
            self.score += temp_tbl[i][2]
        self.score /= len(temp_tbl)
        
    def draw(self):
        if not debug:
            for line in self.__edge_table:
                p1 = [self.__fit(self.__d2_node_table[line[0]][0]), self.__fit(self.__d2_node_table[line[0]][1])]
                p2 = [self.__fit(self.__d2_node_table[line[1]][0]), self.__fit(self.__d2_node_table[line[1]][1])]
                pygame.draw.line(self.dis, "black", p1, p2, 2)

        working = sorted(self.__side_table[:], key = lambda plane: plane.score)
        for i in range(len(working)):
            i = len(working) - i - 1
            p1 = [self.__fit(self.__d2_node_table[working[i].a][0]), self.__fit(self.__d2_node_table[working[i].a][1])]
            p2 = [self.__fit(self.__d2_node_table[working[i].b][0]), self.__fit(self.__d2_node_table[working[i].b][1])]
            p3 = [self.__fit(self.__d2_node_table[working[i].c][0]), self.__fit(self.__d2_node_table[working[i].c][1])]
            p4 = [self.__fit(self.__d2_node_table[working[i].d][0]), self.__fit(self.__d2_node_table[working[i].d][1])]
            pygame.draw.polygon(self.dis, working[i].color, [p1, p2, p3, p4])

    def __repr__(self):
        return str(self.score)