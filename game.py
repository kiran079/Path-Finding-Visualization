import pygame
import heapq
from colors import *
from box import Box

SCREEN = (800, 500)
START = 0
END = 1
BARRIER = 2
EMPTY = 3 

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode(SCREEN)
        self.size = 25
        self.grid = []
        self.clicked = -1
        self.initGrid()
        self.initStartEnd()

    def initGrid(self):
        self.num_y = SCREEN[1] // self.size
        self.num_x = SCREEN[0] // self.size
        for i in range(self.num_y):
            self.grid.append([])
            for j in range(self.num_x):
                self.grid[i].append(Box(self.window, j * self.size, i * self.size, self.size))

    def initStartEnd(self):
        self.start = self.grid[9][5]
        self.start.setType(START)
        self.end = self.grid[9][-5]
        self.end.setType(END)

    def drawGrid(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.grid[i][j].draw()

    def pos_to_index(self, pos):
        return pos[0] // self.size, pos[1] // self.size

    def isValidPos(self, pos):
        return (0 <= pos[1] <= self.num_x - 1 and 0 <= pos[0] <= self.num_y - 1)

    def getNeighbors(self, pos):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbor = (pos[0] + i, pos[1] + j)
                if ((i != 0 or j != 0) and self.isValidPos(neighbor)):
                    neighbors.append(neighbor)
        return neighbors


    def eventListener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                index = self.pos_to_index(mouse_pos)
                self.clicked = self.grid[index[1]][index[0]].type
            elif event.type == pygame.MOUSEBUTTONUP:
                self.clicked = -1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return self.aStar()
        return True

    def changeBlock(self):
        mouse_pos = pygame.mouse.get_pos()
        if (self.clicked > -1 and not self.start.getCollision(mouse_pos) and not self.end.getCollision(mouse_pos)):
            new_index = self.pos_to_index(mouse_pos)
            if (self.clicked == START):
                self.start.setType(EMPTY)
                self.start = self.grid[new_index[1]][new_index[0]]
                self.start.setType(START)
            elif (self.clicked == END):
                self.end.setType(EMPTY)
                self.end = self.grid[new_index[1]][new_index[0]]
                self.end.setType(END) 
            elif (self.clicked == BARRIER):
                self.grid[new_index[1]][new_index[0]].setType(EMPTY)
            elif (self.clicked == EMPTY):
                self.grid[new_index[1]][new_index[0]].setType(BARRIER)

    def getFcost(self, index):
        return self.getGcost(index) + self.getHcost(index)

    def getGcost(self, index):
        return self.getDist(index, self.start_index)

    def getHcost(self, index):
        return self.getDist(index, self.end_index)

    def getDist(self, ind1, ind2):
        x = abs(ind1[0] - ind2[0])
        y = abs(ind1[1] - ind2[1])
        if (x < y):
            x , y = y, x
        return (10 * (x-y)) + (y * 14)

    def greenify(self, index):
        for neighbor in self.getNeighbors(index):
            if self.grid[neighbor[0]][neighbor[1]].type == 3:
                self.grid[neighbor[0]][neighbor[1]].setType(5)

    def aStar(self):
        self.start_index = self.pos_to_index((self.start.rect.centery, self.start.rect.centerx))
        self.end_index = self.pos_to_index((self.end.rect.centery, self.end.rect.centerx))
        opened = []
        prev = {}
        heapq.heappush(opened, (0, self.start_index, self.start))
        opened_hash = {self.start_index}

        g_score = {self.pos_to_index((temp.rect.centery, temp.rect.centerx)): float("inf") for row in self.grid for temp in row}
        g_score[self.start_index] = 0
        f_score = {self.pos_to_index((temp.rect.centery, temp.rect.centerx)): float("inf") for row in self.grid for temp in row}
        f_score[self.start_index] = self.getHcost(self.start_index)
        while opened:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            pygame.time.wait(15)
            popped = heapq.heappop(opened)
            opened_hash.remove(popped[1])

            if (popped[2] == self.end):
                temp = prev[popped[1]]
                while (temp != self.start_index):
                    pygame.time.wait(25)
                    self.grid[temp[0]][temp[1]].setType(6)
                    self.drawGrid()
                    pygame.display.update()
                    temp = prev[temp]
                return True

            for neighbor in self.getNeighbors(popped[1]):
                if self.grid[neighbor[0]][neighbor[1]].type == 2 or self.grid[neighbor[0]][neighbor[1]].type == 0:
                    continue
                self.greenify(popped[1])
                temp_g_score = g_score[popped[1]]+ self.getDist(popped[1], neighbor)
                if temp_g_score < g_score[neighbor]:
                    prev[neighbor] = popped[1]
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.getHcost(neighbor)
                    if neighbor not in opened_hash:
                        heapq.heappush(opened, (f_score[neighbor], neighbor, self.grid[neighbor[0]][neighbor[1]]))
                        opened_hash.add(neighbor)
                        if popped[2] != self.start:
                            popped[2].setType(4)
            self.drawGrid()
            pygame.display.update()

        return True



    def run(self):
        running = True
        clock = pygame.time.Clock()
        while(running):
            clock.tick(30)
            running = self.eventListener()
            self.window.fill(WHITE_SMOKE)
            self.drawGrid()
            self.changeBlock()
            pygame.display.update()