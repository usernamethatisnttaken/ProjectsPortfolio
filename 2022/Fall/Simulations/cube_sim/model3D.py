from dis import dis
from re import A
import pygame
import math
import time

black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

def safe_div(x, y):
    if y == 0:
        return 0
    else:
        return x / y

def safe_div2(x, y):
    if y == 0:
        return 1
    else:
        return x / y

def max(y):
    x = []
    for i in y:
        x.append(i)
    max = x.pop(0)
    total = 0
    for i in range(len(x)):
        if x[i] > max:
            max = x[i]
            total = i + 1
    return total

def polygon(x, y, col):
    if col == black:
        size = 1
    else:
        size = 2
    for i in y:
        if i == 0:
            pygame.draw.line(dis, col, x[0], x[1], size)
    for i in y:
        if i == 1:
            pygame.draw.line(dis, col, x[1], x[2], size)
    for i in y:
        if i == 2:
            pygame.draw.line(dis, col, x[2], x[3], size)
    for i in y:
        if i == 3:
            pygame.draw.line(dis, col, x[3], x[0], size)

def rotate(x, z, b, origin, color):#, adj):
    offset = x[0][2]
    a = dis_dims/2
    x1 = (x[0][0] + x[2][0] + x[7][0] + x[5][0]) / 4
    y1 = (x[0][1] + x[2][1] + x[7][1] + x[5][1]) / 4
    z1 = (x[0][2] + x[2][2] + x[7][2] + x[5][2]) / 4
    r2 = math.sqrt(abs(x1 - x[0][0])**2 + abs(y1 - x[0][1]**2))
    x2 = math.sin(math.radians(z + 45)) * r2
    y2 = math.cos(math.radians(z + 45)) * r2

    p1 = [x2 + a, math.cos(math.radians(b)) * y2 + a + (offset * math.sin(math.radians(b)))]
    p2 = [-y2 + a, math.cos(math.radians(b)) * x2 + a + (offset * math.sin(math.radians(b)))]
    p3 = [-x2 + a, math.cos(math.radians(b)) * -y2 + a + (offset * math.sin(math.radians(b)))]
    p4 = [y2 + a, math.cos(math.radians(b)) * -x2 + a + (offset * math.sin(math.radians(b)))]
    p5 = [x2 + a, math.cos(math.radians(b)) * y2 + a + -(offset * math.sin(math.radians(b)))]
    p6 = [-y2 + a, math.cos(math.radians(b)) * x2 + a + -(offset * math.sin(math.radians(b)))]
    p7 = [-x2 + a, math.cos(math.radians(b)) * -y2 + a + -(offset * math.sin(math.radians(b)))]
    p8 = [y2 + a, math.cos(math.radians(b)) * -x2 + a + -(offset * math.sin(math.radians(b)))]
    points = [p1, p2, p3, p4, p5, p6, p7, p8]
    p = points

    ##add difference between originalL and originalR and add to originalL to get offset and rotation -- DONE
    for k in range(abs(origin[0])):
        k = origin[0]
        l = safe_div(abs(origin[0]), origin[0])
        for i in [0, 1]:
            for j in range(2):
                j = j * 4
                a = (p[j][i] - p[j + 1][i]) * l
                p[j][i] = p[j][i] + (a)
                p[j + 1][i] = p[j + 1][i] + (a)
                a = (p[j + 3][i] - p[j + 2][i]) * l
                p[j + 2][i] = p[j + 2][i] + (a)
                p[j + 3][i] = p[j + 3][i] + (a)
    for k in range(abs(origin[1])):
        k = origin[1]
        l = safe_div(abs(origin[1]), origin[1])
        for i in [0, 1]:
            for j in range(2):
                j = j * 4
                a = (p[j][i] - p[j + 3][i]) * l
                p[j][i] = p[j][i] + (a)
                p[j + 3][i] = p[j + 3][i] + (a)
                a = (p[j + 1][i] - p[j + 2][i]) * l
                p[j + 1][i] = p[j + 1][i] + (a)
                p[j + 2][i] = p[j + 2][i] + (a)
    for k in range(abs(origin[2])):
        k = origin[2]
        l = safe_div(abs(origin[2]), origin[2])
        for i in [0, 1]:
            for j in range(4):
                a = (p[j][i] - p[j + 4][i]) * l
                p[j][i] = p[j][i] + (a)
                p[j + 4][i] = p[j + 4][i] + (a)

    if color == False: #just make colliding square width 0
        test = False
        if test == True:
            col = black
            polygon([p[0], p[1], p[2], p[3]], [0, 1, 2, 3], col)
            polygon([p[4], p[5], p[6], p[7]], [0, 1, 2, 3], col)
            polygon([p[0], p[3], p[7], p[4]], [0, 1, 2, 3], col)
            polygon([p[1], p[2], p[6], p[5]], [0, 1, 2, 3], col)
            polygon([p[0], p[1], p[5], p[4]], [0, 1, 2, 3], col)
            polygon([p[2], p[3], p[7], p[6]], [0, 1, 2, 3], col)

            l = safe_div2(abs(origin[0]), origin[0])
            #l = -1
            if adj[1] == 2 and adj[2] == -l:
                polygon([p[0], p[1], p[2], p[3]], [0, 1, 2, 3], 'white')
            if adj[1] == 2 and adj[2] == l:
                polygon([p[4], p[5], p[6], p[7]], [0, 1, 2, 3], 'white')
            l = safe_div2(abs(origin[1]), origin[1])
            if adj[1] == 0 and adj[2] == -l:
                polygon([p[0], p[3], p[7], p[4]], [0, 1, 2, 3], 'white')
            if adj[1] == 0 and adj[2] == l:
                polygon([p[1], p[2], p[6], p[5]], [0, 1, 2, 3], 'white')
            l = safe_div2(abs(origin[2]), origin[2])
            if adj[1] == 1 and adj[2] == l:
                polygon([p[0], p[1], p[5], p[4]], [0, 1, 2, 3], 'white')
            if adj[1] == 1 and adj[2] == -l:
                polygon([p[2], p[3], p[7], p[6]], [0, 1, 2, 3], 'white')

        else:
            pygame.draw.polygon(dis, black, [p[0], p[1], p[2], p[3]], 1)
            pygame.draw.polygon(dis, black, [p[4], p[5], p[6], p[7]], 1)
            pygame.draw.polygon(dis, black, [p[0], p[3], p[7], p[4]], 1)
            pygame.draw.polygon(dis, black, [p[1], p[2], p[6], p[5]], 1)
            pygame.draw.polygon(dis, black, [p[0], p[1], p[5], p[4]], 1)
            pygame.draw.polygon(dis, black, [p[2], p[3], p[7], p[6]], 1)

    else:
        #c = ['red', 'green', 'blue']
        c = ['red', 'red', 'red']
        pack = [[c[0], [p1, p2, p3, p4]], [c[0], [p5, p6, p7, p8]], [c[1], [p1, p4, p8, p5]], [c[1], [p2, p3, p7, p6]], [c[2], [p1, p2, p6, p5]], [c[2], [p3, p4, p8, p7]]]
        stack(pack, b, z)
        for i in pack:
            pygame.draw.polygon(dis, i[0], i[1])
    return p

def stack(pack, b, z):
    single = True
    if single == True:
        if 90 <= b < 270:
            if 180 <= b < 360:
                if 180 <= z < 360:
                    pack.append(pack.pop(3))
                elif 0 <= z < 180:
                    pack.append(pack.pop(2))
            else:
                if 180 <= z < 360:
                    pack.append(pack.pop(2))
                elif 0 <= z < 180:
                    pack.append(pack.pop(3))
            pack.append(pack.pop(0))
        elif 0 <= b < 90 or 270 <= b < 360:
            if 180 <= b < 360:
                if 180 <= z < 360:
                    pack.append(pack.pop(3))
                elif 0 <= z < 180:
                    pack.append(pack.pop(2))
            else:
                if 180 <= z < 360:
                    pack.append(pack.pop(2))
                elif 0 <= z < 180:
                    pack.append(pack.pop(3))
            pack.append(pack.pop(1))

def time_itr(x):
    start_time = time.time()
    time1 = 1
    while time1 == 1:
        if time.time() - start_time > x:
            time1 = 0

def run(scale_pre, disp, dis_dims_pre, origin, rot, color):#, cleanup): #need to integrate cleanup
    global dis
    dis = disp

    global dis_dims
    dis_dims = dis_dims_pre

    global scale
    scale = scale_pre

    a = scale
    global vertices
    vertices = [[a, a, a], [a, a, -a], [a, -a, a], [a, -a, -a], [-a, a, a], [-a, a, -a], [-a, -a, a], [-a, -a, -a]]
    vertices_pre = []
    for i in range(len(vertices)):
        vertices_pre.append([vertices[i][0], vertices[i][1], vertices[i][2]])
    vertices = []
    for i in vertices_pre:
        vertices.append(i)

    p = rotate(vertices, rot[0], rot[1], origin, color)#, cleanup)
    return p