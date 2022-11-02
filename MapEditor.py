import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import sys
import time
import math
from Utils import show
from pygame.locals import *
from copy import deepcopy


class MapEditor:
    def __init__(self, y=None, x=None, map=[], B=None, R=None, EH=None, delay=250, debug=True, cubeSize=50, env_style=1,
                 agent_style=1):

        pg.init()

        self.cubeSize = cubeSize
        self.celltype = ['stone', 'hole', 'empty', 'box']
        self.active_buttons = [False, False, False]
        self.colors = [(255, 255, 255), (60, 60, 60), (0, 0, 64), (255, 201, 14), (255, 127, 39), (0, 128, 64),
                       (180, 230, 30), (128, 0, 0), (237, 38, 36)]
        self.font = pg.font.Font(None, int(0.45 * self.cubeSize))
        self.delay = delay
        self.debug = debug
        self.last_mouse_click = [None, None]
        self.Done = False
        self.save = False
        self.saved_path = None
        self.message = None
        self.to_change = []
        self.back_to_gui = False

        box_img = pg.image.load('images\\env\\' + str(env_style) + '\\box.jpg')
        self.box_img = pg.transform.scale(box_img, (self.cubeSize, self.cubeSize))
        self.small_box = pg.transform.scale(box_img, (int(0.52 * self.cubeSize), int(0.52 * self.cubeSize)))

        hole_img = pg.image.load('images\\env\\' + str(env_style) + '\\hole.jpg')
        self.hole_img = pg.transform.scale(hole_img, (self.cubeSize, self.cubeSize))
        self.small_hole = pg.transform.scale(hole_img, (int(0.52 * self.cubeSize), int(0.52 * self.cubeSize)))

        floor_img = pg.image.load('images\\env\\' + str(env_style) + '\\floor.jpg')
        self.floor_img = pg.transform.scale(floor_img, (self.cubeSize, self.cubeSize))

        stone_img = pg.image.load('images\\env\\' + str(env_style) + '\\stone.jpg')
        self.stone_img = pg.transform.scale(stone_img, (self.cubeSize, self.cubeSize))
        self.small_stone = pg.transform.scale(stone_img, (int(0.52 * self.cubeSize), int(0.52 * self.cubeSize)))

        left_img = pg.image.load('images\\agent\\' + str(agent_style) + '\\left.png')
        self.left_img = pg.transform.scale(left_img, (2 * self.cubeSize, 2 * self.cubeSize))
        right_img = pg.image.load('images\\agent\\' + str(agent_style) + '\\right.png')
        self.right_img = pg.transform.scale(right_img, (2 * self.cubeSize, 2 * self.cubeSize))
        up_img = pg.image.load('images\\agent\\' + str(agent_style) + '\\up.png')
        self.up_img = pg.transform.scale(up_img, (2 * self.cubeSize, 2 * self.cubeSize))
        down_img = pg.image.load('images\\agent\\' + str(agent_style) + '\\down.png')
        self.down_img = pg.transform.scale(down_img, (2 * self.cubeSize, 2 * self.cubeSize))

        self.back = pg.image.load('images\\back.png')
        self.back = pg.transform.scale(self.back, (int(0.66 * self.cubeSize), int(0.66 * self.cubeSize)))
        # self.reset = pg.image.load('images\\reset.png')
        # self.reset = pg.transform.scale(self.reset, (int(0.66 * self.cubeSize), int(0.66 * self.cubeSize)))

        if map == []:
            self.x = x + 2
            self.y = y + 2
            self.N = x * y

            self.initial_map = self.make_initial_map()
            self.map = deepcopy(self.initial_map)

            if B != None and (type(B) == int or B.isdecimal() == True):
                self.B = int(B)
            else:
                self.B = math.floor(0.5 * self.N)

            if R != None and (type(R) == int or R.isdecimal() == True):
                self.R = int(R)
            else:
                self.R = math.floor(0.1 * self.N)

            if EH != None and (type(EH) == int or EH.isdecimal() == True):
                self.EH = int(EH)
            else:
                self.EH = 0

            self.to_fill = ['hole', 'stone', 'box']
            self.remained = [self.EH, self.R, self.B]

        else:

            self.x = len(map[0])
            self.y = len(map)
            self.N = self.x * self.y

            if self.check_legal_map(map):
                pass
            else:
                print('Illegal Map!!!!!!')

            self.initial_map = self.make_initial_map()
            self.map = map

            self.B = 0
            self.R = 0
            self.EH = 0

            for i in range(len(map)):
                for j in range(len(map[0])):
                    if map[i][j] == 1:
                        self.B += 1
                    elif map[i][j] == -2:
                        self.R += 1
                    elif map[i][j] == -1 and (i != 0 and i != len(map) - 1 and j != 0 and j != len(map[0]) - 1):
                        self.EH += 1

            self.to_fill = ['hole', 'stone', 'box']
            self.remained = [0, 0, 0]

            if B != None and (type(B) == int or B.isdecimal() == True):
                self.B = self.B + int(B)
                self.remained[2] = self.B

            if R != None and (type(R) == int or R.isdecimal() == True):
                self.R = self.R + int(R)
                self.remained[1] = self.R

            if EH != None and (type(EH) == int or EH.isdecimal() == True):
                self.EH = self.EH + int(EH)
                self.remained[0] = self.EH

        self.pixelWidth, self.pixelHeight = self.x * self.cubeSize + self.x - 1, self.y * self.cubeSize + self.y - 1
        self.page = pg.display.set_mode((self.pixelWidth, self.pixelHeight + 3 * self.cubeSize))

        self.redrawPage()

    def check_legal_map(self, map):
        legal = True
        for i in range(len(map)):
            for j in range(len(map[0])):
                if (i == 0 or i == len(map) - 1 or j == 0 or j == len(map[0]) - 1) and (
                        map[i][j] == 1 or map[i][j] == 0):
                    legal = False

        return legal

    def make_initial_map(self):
        initial_map = []
        for i in range(self.y):
            row = []
            for j in range(self.x):
                if j == 0 or j == self.x - 1 or i == 0 or i == self.y - 1:
                    row.append(-1)
                else:
                    row.append(0)
            initial_map.append(row)

        return initial_map

    def redrawPage(self):
        self.page.fill(self.colors[1])
        self.drawLines()
        self.drawTile(self.map)
        self.drawButtons()
        self.drawMessage()
        pg.display.update()

    def drawButtons(self):
        pg.draw.rect(self.page, self.colors[2], (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 0.2 * self.cubeSize, self.pixelHeight + 0.7 * self.cubeSize,
            2 * self.cubeSize, 0.66 * self.cubeSize))
        pg.draw.rect(self.page, self.colors[3 + self.active_buttons[0]], (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 0.2 * self.cubeSize, self.pixelHeight + 0.7 * self.cubeSize,
            2 * self.cubeSize, 0.66 * self.cubeSize), 3)
        self.page.blit(self.small_hole, (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 0.3 * self.cubeSize, self.pixelHeight + 0.77 * self.cubeSize))
        message = str(self.remained[0])
        text = self.font.render(message, True, self.colors[0])
        self.page.blit(text, (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 1.35 * self.cubeSize, self.pixelHeight + .91 * self.cubeSize))

        pg.draw.rect(self.page, self.colors[2], (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 0.2 * self.cubeSize, self.pixelHeight + 1.46 * self.cubeSize,
            2 * self.cubeSize, 0.66 * self.cubeSize))
        pg.draw.rect(self.page, self.colors[3 + self.active_buttons[1]], (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 0.2 * self.cubeSize, self.pixelHeight + 1.46 * self.cubeSize,
            2 * self.cubeSize, 0.66 * self.cubeSize), 3)
        self.page.blit(self.small_stone, (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 0.3 * self.cubeSize, self.pixelHeight + 1.53 * self.cubeSize))
        message = str(self.remained[1])
        text = self.font.render(message, True, self.colors[0])
        self.page.blit(text, (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 1.35 * self.cubeSize, self.pixelHeight + 1.67 * self.cubeSize))

        pg.draw.rect(self.page, self.colors[2], (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 0.2 * self.cubeSize, self.pixelHeight + 2.22 * self.cubeSize,
            2 * self.cubeSize, 0.66 * self.cubeSize))
        pg.draw.rect(self.page, self.colors[3 + self.active_buttons[2]], (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 0.2 * self.cubeSize, self.pixelHeight + 2.22 * self.cubeSize,
            2 * self.cubeSize, 0.66 * self.cubeSize), 3)
        self.page.blit(self.small_box, (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 0.3 * self.cubeSize, self.pixelHeight + 2.29 * self.cubeSize))
        message = str(self.remained[2])
        text = self.font.render(message, True, self.colors[0])
        self.page.blit(text, (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 1.35 * self.cubeSize, self.pixelHeight + 2.43 * self.cubeSize))

        pg.draw.rect(self.page, self.colors[5], (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 2.5 * self.cubeSize, self.pixelHeight + 0.7 * self.cubeSize,
            1.4 * self.cubeSize, 0.66 * self.cubeSize))
        pg.draw.rect(self.page, self.colors[6], (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 2.5 * self.cubeSize, self.pixelHeight + 0.7 * self.cubeSize,
            1.4 * self.cubeSize, 0.66 * self.cubeSize), 3)
        message = 'OK'
        text = self.font.render(message, True, self.colors[0])
        self.page.blit(text, (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 2.91 * self.cubeSize, self.pixelHeight + 0.9 * self.cubeSize))

        pg.draw.rect(self.page, self.colors[7], (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 2.5 * self.cubeSize, self.pixelHeight + 1.46 * self.cubeSize,
            1.4 * self.cubeSize, 0.66 * self.cubeSize))
        pg.draw.rect(self.page, self.colors[8], (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 2.5 * self.cubeSize, self.pixelHeight + 1.46 * self.cubeSize,
            1.4 * self.cubeSize, 0.66 * self.cubeSize), 3)
        message = 'Save'
        text = self.font.render(message, True, self.colors[0])
        self.page.blit(text, (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 2.79 * self.cubeSize, self.pixelHeight + 1.66 * self.cubeSize))

        self.page.blit(self.back, (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 3.23 * self.cubeSize, self.pixelHeight + 2.22 * self.cubeSize))
        # self.page.blit(self.reset, (
        #     0.5 * self.pixelWidth - 2 * self.cubeSize + 2.51 * self.cubeSize, self.pixelHeight + 2.22 * self.cubeSize))

    def drawLines(self):
        for i in range(self.x - 1):
            pg.draw.line(self.page, self.colors[0], (self.pixelPos(i + 1), 0), (self.pixelPos(i + 1), self.pixelHeight))

        for i in range(self.y - 1):
            pg.draw.line(self.page, self.colors[0], (0, self.pixelPos(i + 1)), (self.pixelWidth, self.pixelPos(i + 1)))

    def drawTile(self, array):
        for i, a in enumerate(array):
            for j, tile in enumerate(a):
                self.colorCube(j, i, self.celltype[tile + 2])

    def drawMessage(self):
        if self.message != None and type(self.message) == str:
            pg.font.init()
            font = pg.font.SysFont('arial', self.cubeSize)
            color = self.colors[0]
            text = self.font.render(self.message, True, self.colors[0])
            self.page.blit(text, (
                0.5 * self.pixelWidth - 2 * self.cubeSize + 0.6 * self.cubeSize,
                self.pixelHeight + 0.2 * self.cubeSize))
            pg.display.update()
            time.sleep(0.5)
            self.message = None

    def colorCube(self, i, j, celltype):
        if celltype == 'stone':
            self.page.blit(self.stone_img, (self.pixelPos(i), self.pixelPos(j)))
        elif celltype == 'hole':
            self.page.blit(self.hole_img, (self.pixelPos(i), self.pixelPos(j)))
        elif celltype == 'empty':
            self.page.blit(self.floor_img, (self.pixelPos(i), self.pixelPos(j)))
        elif celltype == 'box':
            self.page.blit(self.box_img, (self.pixelPos(i), self.pixelPos(j)))

    def user_click(self):
        # get coordinates of mouse click 
        x, y = pg.mouse.get_pos()

        row = self.whichTile(y)
        column = self.whichTile(x)

        if row >= self.y:
            row = None

        if column >= self.x:
            column = None

        self.last_mouse_click = [row, column]

        if len(self.to_fill) != 0 and row != None and column != None:
            self.update_map(row, column)
        else:
            self.update_buttons(x, y)

    def update_buttons(self, x, y):
        self.active_buttons = [False, False, False]

        if 0.5 * self.pixelWidth - 2 * self.cubeSize + 0.2 * self.cubeSize <= x <= 0.5 * self.pixelWidth - 2 * self.cubeSize + 0.2 * self.cubeSize + 2 * self.cubeSize:
            if self.pixelHeight + 0.7 * self.cubeSize <= y <= self.pixelHeight + 0.7 * self.cubeSize + 0.66 * self.cubeSize:
                self.active_buttons[0] = True

            elif self.pixelHeight + 1.46 * self.cubeSize <= y <= self.pixelHeight + 1.46 * self.cubeSize + 0.66 * self.cubeSize:
                self.active_buttons[1] = True

            elif self.pixelHeight + 2.22 * self.cubeSize <= y <= self.pixelHeight + 2.22 * self.cubeSize + 0.66 * self.cubeSize:
                self.active_buttons[2] = True


        elif 0.5 * self.pixelWidth - 2 * self.cubeSize + 2.5 * self.cubeSize <= x <= 0.5 * self.pixelWidth - 2 * self.cubeSize + 2.5 * self.cubeSize + 1.4 * self.cubeSize:
            if self.pixelHeight + 0.7 * self.cubeSize <= y <= self.pixelHeight + 0.7 * self.cubeSize + 0.66 * self.cubeSize:
                if sum(self.remained) == 0:
                    self.Done = True
                else:
                    self.message = 'Tiles Remained !!!'

            elif self.pixelHeight + 1.46 * self.cubeSize <= y <= self.pixelHeight + 1.46 * self.cubeSize + 0.66 * self.cubeSize:
                self.save = True


            elif self.pixelHeight + 2.22 * self.cubeSize <= y <= self.pixelHeight + 2.22 * self.cubeSize + int(
                    0.66 * self.cubeSize):
                # if 0.5 * self.pixelWidth - 2 * self.cubeSize + 2.51 * self.cubeSize <= x <= 0.5 * self.pixelWidth - 2 * self.cubeSize + 2.51 * self.cubeSize + int(
                #         0.66 * self.cubeSize):
                #     print('Restart')

                if 0.5 * self.pixelWidth - 2 * self.cubeSize + 3.23 * self.cubeSize <= x <= 0.5 * self.pixelWidth - 2 * self.cubeSize + 3.23 * self.cubeSize + int(
                        0.66 * self.cubeSize):
                    self.back_to_gui = True

    def update_map(self, row, column):
        if sum(self.active_buttons) >= 1:
            filling = self.to_fill[self.active_buttons.index(True)]
            remained = self.remained[self.active_buttons.index(True)]
        else:
            filling = None
            remained = -1

        value = self.map[row][column]
        is_changed = bool(self.initial_map[row][column] - value != 0)
        show(self.map)
        show(self.initial_map)

        if filling == None and is_changed == False:
            self.message = 'Choose tile type !!!'

        elif remained > 0 and is_changed == False:
            if filling == 'hole' and value == 0:
                self.to_change = [row, column, -1]
                self.remained[self.active_buttons.index(True)] -= 1

            elif filling == 'box' and value == 0:
                self.to_change = [row, column, 1]
                self.remained[self.active_buttons.index(True)] -= 1

            elif filling == 'stone' and (value == 0 or value == -1):
                self.to_change = [row, column, -2]
                self.remained[self.active_buttons.index(True)] -= 1

            else:
                self.message = 'Action Failed !!!'


        elif is_changed == True:
            if self.map[row][column] == -1:
                self.remained[0] += 1
            elif self.map[row][column] == -2:
                self.remained[1] += 1
            elif self.map[row][column] == 1:
                self.remained[2] += 1

            self.to_change = [row, column, self.initial_map[row][column]]

        else:
            self.message = 'Action Failed !!!'

    def pixelPos(self, i):
        return i * self.cubeSize + i

    def whichTile(self, pixel):
        return pixel // (self.cubeSize + 1)
