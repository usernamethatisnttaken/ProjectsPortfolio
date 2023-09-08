##DESC
#A little simulation that generates a board of 'walls' out of random noise, then uses
#one of three different search algorithms to find the shortest path as soon as possible

#Breadth-First[modded] - searches close tiles first
#Greedy Best-First[modded] - searches tile that are close to the optimal path first
#Rivulet[custom] (similar to a wacky A* search) - searches tiles that are close to the
    #optimal path AND close to the target point first, but has a small working frontier

#Currently needs some of refactoring as there are a lot of variables that do the same
#thing, move() has entirely too many returns and main() handles a lot of what should be
#handled by lower functions


##SETTINGS
NOISE_PER = 25     #percent of the board that is wall
SEEDED = False     #is the random generator seeded?
TIMED = True     #are the algorithms timed
COLLECT_DATA = False     #if it has a 'data.csv' file, it will write the length and time taken to search

import pygame
import random
import time
import math

decay_time = 10
START_TIME = 0
ALGORITHM = 0
abs_scale = 10
scale = abs_scale
max_cool = 12
dis_dims = 800
pygame.init()
dis = pygame.display.set_mode((dis_dims, dis_dims + 50))
pygame.display.set_caption('Pathfinding Algorithms')


class Display:
    def __init__(self, origin, target):
        self.log = {}
        add = 0
        if dis_dims // scale != dis_dims / scale:
            add = 1
        for i in range(dis_dims // scale + add):
            self.log[i * scale] = {}
        self.origin = origin
        self.target = target
        self.frontier = [origin.coords]
        self.checked  = []
        self.max_state = 0
        self.noise_gen()

    def noise_gen(self): #generates noise on the board
        add = 0
        if dis_dims // scale != dis_dims / scale:
            add = 1
        for i in range(dis_dims // scale + add):
            for j in range(dis_dims // scale + add):
                if [i * scale, j * scale] != self.origin.coords and [i * scale, j * scale] != self.target.coords:
                    self.log[i * scale][j * scale] = [random.choices([0, 1], [100 - NOISE_PER, NOISE_PER])[0], None]

    def state_map(self, type = 0): #sets up the search priority for all searchable blocks (used in greedy and rivulet searches)
        type = 'rivulet'
        if type == 1:
            type = 'deviation'
        state_list = []
        if type in ['deviation', 'rivulet']: #goes off of deviation from optimal path
            for i in self.log:
                for j in self.log[i]:
                    p = self.origin.coords[0] / scale
                    q = self.origin.coords[1] / scale
                    m = self.target.coords[0] / scale
                    n = self.target.coords[1] / scale
                    m1 = (p - n) / (q - m)
                    m2 = (q - m) / (p - n)
                    c = (((j / scale) + m1 * (i / scale)) - (q - m2 * p))/(m1 + m2)
                    d = m2 * c + (q - m2 * p)
                    deviation = math.sqrt(((i / scale) - c)**2 + ((j / scale) - d)**2)
                    self.log[i][j][1] = round(deviation)

                    if round(deviation) not in state_list:
                        state_list.append(round(deviation))

        if type == 'rivulet': #goes off of deviation from optimal path + distance from target
            add = []
            for i in self.log:
                for j in self.log[i]:
                    dist = math.sqrt((self.target.coords[0] / scale - i / scale)**2 + (self.target.coords[1] / scale - j / scale)**2)
                    self.log[i][j][1] = self.log[i][j][1] + round(dist)
                    if round(dist) not in add:
                        add.append(round(dist))
            base = state_list[:]
            state_list = []
            for i in range(len(base)):
                for j in range(len(add)):
                    state_list.append(i + j)
            if self.max_state < round(deviation):
                self.max_state = round(deviation)
        return state_list

    def itr(self, found, state_list, first): #top function for all of the searches
        if ALGORITHM == 0:
            return self.itr_breadth(found, first)
        elif ALGORITHM == 1:
            return self.itr_greedy(found, state_list)
        else:
            return self.itr_rivulet(found, state_list)

    def itr_breadth(self, found, first = False, i = 0): #breadth-first search
        if len(self.frontier) > 0 and found == False:
            for j in [-1, 1]:
                comp = False
                flip = True
                new_x = self.frontier[i][0] + j * scale
                new_y = self.frontier[i][1]
                if [new_x, new_y] == self.target.coords:
                    comp = True
                if dis_dims > new_x >= 0 and dis_dims > new_y >= 0 and [new_x, new_y] != self.origin.coords:
                    for block in self.frontier:
                        if block[0:2] == [new_x, new_y]:
                            flip = False
                    if flip and not comp:
                        if self.log[new_x][new_y][0] > 0:
                            flip = False
                    if flip:
                        if not first:
                            self.frontier.append([new_x, new_y, self.frontier[i]])
                        else:
                            self.frontier.append([new_x, new_y])
                    if comp:
                        self.frontier = self.frontier[-1]
                        return self.frontier[-1]
                if [new_x, new_y] == self.target.coords:
                    return self.frontier[-1]
            for j in [-1, 1]:
                comp = False
                flip = True
                new_x = self.frontier[i][0]
                new_y = self.frontier[i][1] + j * scale
                if [new_x, new_y] == self.target.coords:
                    comp = True
                if dis_dims > new_x >= 0 and dis_dims > new_y >= 0 and [new_x, new_y] != self.origin.coords:
                    for block in self.frontier:
                        if block[0:2] == [new_x, new_y]:
                            flip = False
                    if flip and not comp:
                        if self.log[new_x][new_y][0] > 0:
                           flip = False
                    if flip:
                        if not first:
                            self.frontier.append([new_x, new_y, self.frontier[i]])
                        else:
                            self.frontier.append([new_x, new_y])
                    if comp:
                        self.frontier = self.frontier[-1]
                        return self.frontier[-1]
            check = self.frontier.pop(i)
            if check != self.origin.coords:
                self.log[check[0]][check[1]][0] = 2
        self.draw(found)

    def itr_greedy(self, found, state_list, first = False): #greedy best-first search
        if len(self.frontier) > 0 and not found:
            ind = 0
            cont = True
            while ind < len(state_list) and cont:
                for i in range(len(self.frontier)):
                    i = len(self.frontier) - 1 - i
                    trigger = False
                    for offset in [-1, 1]:
                        new_x = self.frontier[i][0] + offset * scale
                        new_y = self.frontier[i][1]
                        if [new_x, new_y] == self.target.coords:
                            self.frontier.append([new_x, new_y, self.frontier[i]])
                            self.frontier = self.frontier[-1]
                            return self.frontier[-1]
                        flip = True
                        if dis_dims > new_x >= 0 and dis_dims > new_y >= 0 and [new_x, new_y] != self.origin.coords:
                            for block in self.frontier:
                                if block[0:2] == [new_x, new_y]:
                                    flip = False
                            for block in self.checked:
                                if block[0:2] == [new_x, new_y]:
                                    flip = False
                            if self.log[new_x][new_y] == [0, state_list[ind]] and flip:
                                back = self.frontier[i]
                                if [new_x, new_y] != self.origin.coords:
                                    self.frontier.append([new_x, new_y, back])
                                else:
                                    self.frontier.append([new_x, new_y])
                                cont = False
                                trigger = True
                                break
                    if trigger:
                        break
                    for offset in [-1, 1]:
                        new_x = self.frontier[i][0]
                        new_y = self.frontier[i][1] + offset * scale
                        if [new_x, new_y] == self.target.coords:
                            self.frontier.append([new_x, new_y, self.frontier[i]])
                            self.frontier = self.frontier[-1]
                            return self.frontier[-1]
                        flip = True
                        if dis_dims > new_x >= 0 and dis_dims > new_y >= 0 and [new_x, new_y] != self.origin.coords:
                            for block in self.frontier:
                                if block[0:2] == [new_x, new_y]:
                                    flip = False
                            for block in self.checked:
                                if block[0:2] == [new_x, new_y]:
                                    flip = False
                            if self.log[new_x][new_y] == [0, state_list[ind]] and flip:
                                back = self.frontier[i]
                                if [new_x, new_y] != self.origin.coords:
                                    self.frontier.append([new_x, new_y, back])
                                else:
                                    self.frontier.append([new_x, new_y])
                                cont = False
                                break
                ind += 1
                
            cut_list = [] #if a block has no moves_left it is removed from the frontier
            for i in range(len(self.frontier)):
                if self.cutoff(self.frontier[i]):
                    cut_list.append(i - len(cut_list))
            for i in cut_list:
                self.checked.append(self.frontier.pop(i))
                if self.checked[-1] != self.origin.coords:
                    self.log[self.checked[-1][0]][self.checked[-1][1]][0] = 2
        self.draw(found)

    def itr_rivulet(self, found, state_list): #my custom search (sort of like an A* search)
        if len(self.frontier) > 0 and found == False:
            ind = 0
            cont = True
            while ind < len(state_list) and cont:
                for i in range(len(self.frontier)):
                    i = len(self.frontier) - 1 - i
                    trigger = False
                    for offset in [-1, 1]:
                        new_x = self.frontier[i][0] + offset * scale
                        new_y = self.frontier[i][1]
                        if [new_x, new_y] == self.target.coords:
                            self.frontier = self.frontier[i]
                            return self.frontier
                        flip = True
                        if dis_dims > new_x >= 0 and dis_dims > new_y >= 0 and [new_x, new_y] != self.origin.coords:
                            for block in self.frontier:
                                if block[0:2] == [new_x, new_y]:
                                    flip = False
                            for block in self.checked:
                                if block[0:2] == [new_x, new_y]:
                                    flip = False
                            if self.log[new_x][new_y] == [0, state_list[ind]] and flip:
                                back = self.frontier[i]
                                if [new_x, new_y] != self.origin.coords:
                                    self.frontier.append([new_x, new_y, back])
                                else:
                                    self.frontier.append([new_x, new_y])
                                cont = False
                                trigger = True
                                break
                    if trigger:
                        break
                    for offset in [-1, 1]:
                        new_x = self.frontier[i][0]
                        new_y = self.frontier[i][1] + offset * scale
                        if [new_x, new_y] == self.target.coords:
                            self.frontier = self.frontier[i]
                            return self.frontier
                        flip = True
                        if dis_dims > new_x >= 0 and dis_dims > new_y >= 0 and [new_x, new_y] != self.origin.coords:
                            for block in self.frontier:
                                if block[0:2] == [new_x, new_y]:
                                    flip = False
                            for block in self.checked:
                                if block[0:2] == [new_x, new_y]:
                                    flip = False
                            if self.log[new_x][new_y] == [0, state_list[ind]] and flip:
                                back = self.frontier[i]
                                if [new_x, new_y] != self.origin.coords:
                                    self.frontier.append([new_x, new_y, back])
                                else:
                                    self.frontier.append([new_x, new_y])
                                cont = False
                                break
                ind += 1
            while len(self.frontier) > decay_time: #removes old frontier from the working list
                self.checked.append(self.frontier.pop(0))
                if self.checked[-1] != self.origin.coords:
                    self.log[self.checked[-1][0]][self.checked[-1][1]][0] = 2
        self.draw(found)
    
    def cutoff(self, coords): #checks to see if a frontier block has any possible moves left
        x = coords[0]
        y = coords[1]
        for offset in [-1, 1]:
            flip = True
            new_x = x + offset * scale
            new_y = y
            if dis_dims > new_x >= 0 and dis_dims > new_y >= 0 and [new_x, new_y] != self.origin.coords and [new_x, new_y] != self.target.coords:
                for block in self.frontier:
                    if block[0:2] == [new_x, new_y]:
                        flip = False
                for block in self.checked:
                    if block[0:2] == [new_x, new_y]:
                        flip = False
                if self.log[new_x][new_y][0] == 0 and flip:
                    return False
            if [new_x, new_y] == self.target.coords:
                return False
        for offset in [-1, 1]:
            flip = True
            new_x = x
            new_y = y + offset * scale
            if dis_dims > new_x >= 0 and dis_dims > new_y >= 0 and [new_x, new_y] != self.origin.coords and [new_x, new_y] != self.target.coords:
                for block in self.frontier:
                    if block[0:2] == [new_x, new_y]:
                        flip = False
                for block in self.checked:
                    if block[0:2] == [new_x, new_y]:
                        flip = False
                if self.log[new_x][new_y][0] == 0 and flip:
                    return False
            if [new_x, new_y] == self.target.coords:
                return False
        return True

    def add(self): # adds/removes a wall to the world
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            pos = pygame.mouse.get_pos()
            if pos[0] // scale * scale in self.log:
                if pos[1] // scale * scale in self.log[pos[0] // scale * scale]:
                    self.log[pos[0] // scale * scale][pos[1] // scale * scale][0] = 1
        if mouse[2]:
            pos = pygame.mouse.get_pos()
            if pos[0] // scale * scale in self.log:
                if pos[1] // scale * scale in self.log[pos[0] // scale * scale]:
                    self.log[pos[0] // scale * scale][pos[1] // scale * scale][0] = 0

    def draw(self, found = False): #draws the current world set-up
        for x in self.log:
            for y in self.log[x]:
                color = 'white'
                if self.log[x][y][0] == 1:
                    color = 'gray'
                elif self.log[x][y][0] == 2:
                    color = '#80f2ee'
                block = [x, y]
                pygame.draw.polygon(dis, color, [[block[0], block[1]], [block[0], block[1] + scale], [block[0] + scale, block[1] + scale], [block[0] + scale, block[1]]])
        if not found:
            for block in self.frontier:
                color = 'blue'
                pygame.draw.polygon(dis, color, [[block[0], block[1]], [block[0], block[1] + scale], [block[0] + scale, block[1] + scale], [block[0] + scale, block[1]]])
        block = self.origin.coords
        color = 'green'
        pygame.draw.polygon(dis, color, [[block[0], block[1]], [block[0], block[1] + scale], [block[0] + scale, block[1] + scale], [block[0] + scale, block[1]]])
        block = self.target.coords
        color = 'red'
        pygame.draw.polygon(dis, color, [[block[0], block[1]], [block[0], block[1] + scale], [block[0] + scale, block[1] + scale], [block[0] + scale, block[1]]])

    def fin(self): #wrapps the class up at the end
        for i in self.log:
            for j in self.log[i]:
                if self.log[i][j][0] == 2:
                    self.log[i][j][0] = 0

class Origin:
    def __init__(self):
        self.coords = [3 * scale, 3 * scale]

class Target:
    def __init__(self):
        self.coords = [dis_dims - 3 * scale, dis_dims - 3 * scale]

def quit1(): #closes the simulation
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def move(display, origin, target, found, first, result, start, scale_pre, cooldown, state_list, flip): #user input controller
    scale_2pre = scale_pre
    reset = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s] and not start:
        start = True
        state_list = display.state_map(ALGORITHM)
        global START_TIME
        START_TIME = time.perf_counter()
        flip = True
    if keys[pygame.K_p] and cooldown == 0:
        if start:
            start = False
        else:
            start = True
        cooldown = max_cool * 2
    if keys[pygame.K_r]:
        found = False
        first = True
        result = None
        start = False
        display.fin()
        display.frontier = [origin.coords]
        display.checked = []
    if keys[pygame.K_LEFT] and cooldown == 0:
        reset = True
        scale_pre -= 1
        cooldown = max_cool
    if keys[pygame.K_RIGHT] and cooldown == 0:
        reset = True
        scale_pre += 1
        cooldown = max_cool
    global scale
    scale = scale_pre
    if cooldown > 0:
        cooldown -= 1
    if keys[pygame.K_SPACE] or reset:
        time_itr(0.1)
        origin.coords = mod([origin.coords[0] / scale_2pre * scale, origin.coords[1] / scale_2pre * scale])
        target.coords = mod([dis_dims - ((dis_dims - target.coords[0]) / scale_2pre * scale) + scale/2, dis_dims - ((dis_dims - target.coords[1]) / scale_2pre * scale) + scale/2])
        return Display(origin, target), False, True, None, False, cooldown, [], True
    return display, found, first, result, start, cooldown, state_list, flip

def algorithm_choice(display, state_list, choice): #controls the search choice
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        choice = 0
    elif keys[pygame.K_2]:
        choice = 1
        state_list = display.state_map(choice)
    elif keys[pygame.K_3]:
        choice = 2
        state_list = display.state_map(choice)
    global ALGORITHM
    ALGORITHM = choice
    return state_list

def mod(x): #modularization function
    for i in range(len(x)):
        x[i] = x[i] // scale * scale
    return x

def draw(block, origin, tick = 0): #draws the final path
    if block != origin.coords:
        pygame.draw.polygon(dis, 'purple', [[block[0], block[1]], [block[0], block[1] + scale], [block[0] + scale, block[1] + scale], [block[0] + scale, block[1]]])
    if len(block) == 3:
        return draw(block[2], origin, tick + 1)
    return tick

def record(time, length): #records data for further processing
    data = ''
    tick = 0
    with open('data.csv', 'r') as file:
        for line in file:
            if tick != ALGORITHM:
                data += line
            else:
                if tick != 3:
                    newline = '\n'
                else:
                    newline = ''
                if line.strip() != '':
                    comma = ','
                else:
                    comma = ''
                divisor = dis_dims / (scale * math.sqrt(2)) / 100
                data += line.strip() + comma + '(' + str(round(time / divisor * 10, 3)) + ';' + str(round(length / divisor, 3)) + ')' + newline
            tick += 1
    with open('data.csv', 'w') as file:
        file.write(data)

def ui(): #writes the ui/directions form my little knowledge about text in pygame
    pt = 20
    font = pygame.font.SysFont('Comic Sans MS', pt)

    text1 = font.render('<-/+>   S-Start   P-Pause   R-Reset   Space-Reroll Board', False, 'black')
    text2 = font.render('1-Breadth-First   2-Greedy Best-First   3-Rivulet', False, 'black')

    dis.blit(text1, (0, dis_dims))
    dis.blit(text2, (0, dis_dims + 1 * pt))

def time_itr(x): #standard spacer
    start_time = time.time()
    time1 = 1
    while time1 == 1:
        if time.time() - start_time > x:
            time1 = 0

def run():
    if SEEDED:
        random.seed(0)
    origin = Origin()
    target = Target()
    display = Display(origin, target)

    cont = True
    length = len(display.frontier)
    tick = 0
    found = False
    result = None
    first = True
    start = False
    flip = True
    cooldown = 0
    state_list = []
    while cont == True:
        cont = quit1()
        dis.fill('white')

        display, found, first, result, start, cooldown, state_list, flip = move(display, origin, target, found, first, result, start, scale, cooldown, state_list, flip)
        state_list = algorithm_choice(display, state_list, ALGORITHM)
        if start:
            if found:
                display.itr(found, state_list, first)
            else:
                result = display.itr(found, state_list, first)
            if result != None and not found:
                total_time = time.perf_counter() - START_TIME
                print('Timer: ' + str(total_time) + 's')
            if result != None:
                path_len = draw(result, display.origin)
                if flip:
                    print('Len: ' + str(path_len))
                    if COLLECT_DATA:
                        record(total_time, path_len)
                    flip = False
                found = True
                display.fin()

            if tick < length - 1:
                tick += 1
            else:
                tick = 0
                length = len(display.frontier)
            first = False
        else:
            display.add()
            display.draw()
        ui()

        pygame.display.update()
    pygame.quit()
    quit()

run()