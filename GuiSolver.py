import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import time
from MainGui import InputBox


class Solver:
    pixelWidth, pixelHeight, page, cubeSize, colors = 0, 0, 0, 0, []

    def __init__(self, cubeSize, delay, state, env_style=1, agent_style=1):

        box_img = pg.image.load('images\\env\\' + str(env_style) + '\\box.jpg')
        self.box_img = pg.transform.scale(box_img, (cubeSize, cubeSize))
        hole_img = pg.image.load('images\\env\\' + str(env_style) + '\\hole.jpg')
        self.hole_img = pg.transform.scale(hole_img, (cubeSize, cubeSize))
        floor_img = pg.image.load('images\\env\\' + str(env_style) + '\\floor.jpg')
        self.floor_img = pg.transform.scale(floor_img, (cubeSize, cubeSize))
        stone_img = pg.image.load('images\\env\\' + str(env_style) + '\\stone.jpg')
        self.stone_img = pg.transform.scale(stone_img, (cubeSize, cubeSize))

        left_img = pg.image.load('images\\agent\\' + str(agent_style) + '\\left.png')
        self.left_img = pg.transform.scale(left_img, (2 * cubeSize, 2 * cubeSize))
        right_img = pg.image.load('images\\agent\\' + str(agent_style) + '\\right.png')
        self.right_img = pg.transform.scale(right_img, (2 * cubeSize, 2 * cubeSize))
        up_img = pg.image.load('images\\agent\\' + str(agent_style) + '\\up.png')
        self.up_img = pg.transform.scale(up_img, (2 * cubeSize, 2 * cubeSize))
        down_img = pg.image.load('images\\agent\\' + str(agent_style) + '\\down.png')
        self.down_img = pg.transform.scale(down_img, (2 * cubeSize, 2 * cubeSize))

        self.back = pg.image.load('images\\back.png')
        self.back = pg.transform.scale(self.back,(int(0.66*cubeSize),int(0.66*cubeSize)))

        self.increase = pg.image.load('images\\increase.png')
        self.increase = pg.transform.scale(self.increase,(int(0.5*cubeSize),int(0.3*cubeSize)))

        self.decrease = pg.image.load('images\\decrease.png')
        self.decrease = pg.transform.scale(self.decrease,(int(0.5*cubeSize),int(0.3*cubeSize)))

        self.back_to_mapeditor = False

        self.delay = delay
        w = len(state.map_array[0])
        h = len(state.map_array)
        # celltype for rocks, hole, empty, box
        self.celltype = ['stone', 'hole', 'empty', 'box']
        self.cubeSize = cubeSize
        self.pixelWidth, self.pixelHeight = w * self.cubeSize + w - 1, h * self.cubeSize + h - 1
        self.page = pg.display.set_mode((self.pixelWidth, self.pixelHeight + 3 * self.cubeSize))

        self.delayinput = InputBox(0.5 * self.pixelWidth - 2 * self.cubeSize + 1.5*self.cubeSize, self.pixelHeight + 1.4*self.cubeSize,0.7*self.cubeSize,0.6*self.cubeSize,text = '1', font_size=int(0.6 * self.cubeSize))

        self.redrawPage(state)

    # def drawinputbox(self):

    def redrawPage(self, game, action=None):
        mapArr = game.previous_map
        self.page.fill((60, 60, 60))
        self.drawTile(mapArr)
        self.drawAction(action)
        self.drawTexts(game)
        self.drawButtons()
        self.animate(game, action)

        self.drawTile(game.map_array)
        self.drawAction(action)

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

    def drawTile(self, array):
        for i, a in enumerate(array):
            for j, tile in enumerate(a):
                self.colorCube(j, i, self.celltype[tile + 2])

    def drawAction(self, action):
        if action == None: return

        if action.direction == 'right':
            self.page.blit(self.right_img,
                           (self.pixelPos(action.y) - self.cubeSize / 2, self.pixelPos(action.x) - self.cubeSize / 2))

        if action.direction == 'left':
            self.page.blit(self.left_img,
                           (self.pixelPos(action.y) - self.cubeSize / 2, self.pixelPos(action.x) - self.cubeSize / 2))

        if action.direction == 'up':
            self.page.blit(self.up_img,
                           (self.pixelPos(action.y) - self.cubeSize / 2, self.pixelPos(action.x) - self.cubeSize / 2))

        if action.direction == 'down':
            self.page.blit(self.down_img,
                           (self.pixelPos(action.y) - self.cubeSize / 2, self.pixelPos(action.x) - self.cubeSize / 2))

    def animate(self, state, action, fps=30, duration=1):

        if state.previous_map != None:
            cells_to_move = []
            if state.last_state in ['empty', 'fire']:
                for k in range(state.number_of_boxes):
                    cells_to_move.append([action.x + k * state.v, action.y + k * state.h])

            if len(cells_to_move) > 0:
                step = self.cubeSize / fps

                for k in range(1, fps + 1):
                    if self.back_to_mapeditor:
                        break

                    for cell in cells_to_move:
                        self.page.blit(self.floor_img, (self.pixelPos(cell[1]), self.pixelPos(cell[0])))

                    for cell in cells_to_move:
                        self.page.blit(self.box_img, (self.pixelPos(cell[1]) + state.h * k * step + state.h,
                                                      self.pixelPos(cell[0]) + state.v * k * step + state.v))

                    self.drawAction(action)

                    self.drawTexts(state)
                    self.drawButtons()
                    # self.drawinputbox()

                    pg.display.update()
                    pg.time.delay(int((duration*200) / fps))

                    for event in pg.event.get():

                        if event.type == pg.QUIT:
                            exit()

                        if event.type == pg.MOUSEBUTTONDOWN:
                            self.user_click(event)

                        if event.type == pg.KEYDOWN:
                            self.user_write(event)

    def drawButtons(self):
        self.page.blit(self.back , (0.5*self.pixelWidth - 2*self.cubeSize + 3.23*self.cubeSize,self.pixelHeight+2.22*self.cubeSize))
        self.page.blit(self.increase , (0.5 * self.pixelWidth - 2 * self.cubeSize + 1.6*self.cubeSize, self.pixelHeight + 1*self.cubeSize))
        self.page.blit(self.decrease , (0.5 * self.pixelWidth - 2 * self.cubeSize + 1.6*self.cubeSize, self.pixelHeight + 2.1*self.cubeSize))
        self.delayinput.draw(self.page)
        # self.page.blit(self.increase,(0.5 * self.pixelWidth - 2 * self.cubeSize + 1.5*self.cubeSize, self.pixelHeight + 0.9*self.cubeSize))
        pg.display.update()

    def drawTexts(self, state):
        pg.font.init()
        pg.draw.rect(self.page,(60,60,60),(0,self.pixelHeight,self.pixelWidth,self.cubeSize*3))
        font = pg.font.SysFont('arial', int(0.45 * self.cubeSize))
        color = (255, 255, 255)
        message = "Deine Pathetik ist : " + str(state.cost)
        text = font.render(message, True, color)
        self.page.blit(text, (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 0.15 * self.cubeSize, self.pixelHeight + 0.2 * self.cubeSize))

        text = font.render('Delay :          (s)', True, color)
        self.page.blit(text, (
            0.5 * self.pixelWidth - 2 * self.cubeSize + 0.2*self.cubeSize, self.pixelHeight + 1.4*self.cubeSize))
        


    def colorCube(self, i, j, celltype):
        if celltype == 'stone':
            self.page.blit(self.stone_img, (self.pixelPos(i), self.pixelPos(j)))
        elif celltype == 'hole':
            self.page.blit(self.hole_img, (self.pixelPos(i), self.pixelPos(j)))
        elif celltype == 'empty':
            self.page.blit(self.floor_img, (self.pixelPos(i), self.pixelPos(j)))
        elif celltype == 'box':
            self.page.blit(self.box_img, (self.pixelPos(i), self.pixelPos(j)))

    def pixelPos(self, i):
        return i * self.cubeSize + i

    def user_click(self,event=None): 
        x, y = pg.mouse.get_pos() 
        # if self.delayinput.rect.collidepoint(event.pos):
        #     self.delayinput.active = not self.delayinput.active
        # else:
        #     self.delayinput.active = False
        # self.delayinput.color = self.delayinput.COLOR_ACTIVE if self.delayinput.active else self.delayinput.COLOR_INACTIVE

        if 0.5 * self.pixelWidth - 2 * self.cubeSize + 1.6*self.cubeSize <= x <= 0.5 * self.pixelWidth - 2 * self.cubeSize + 1.6*self.cubeSize + 0.5*self.cubeSize:
            if self.pixelHeight + 1*self.cubeSize <= y <= self.pixelHeight + 1*self.cubeSize + 0.3*self.cubeSize:
                if float(self.delayinput.text) < 99:
                    self.delayinput.text = str(float(self.delayinput.text) + 0.25)
            elif self.pixelHeight + 2.1*self.cubeSize <= y <= self.pixelHeight + 2.1*self.cubeSize + 0.3*self.cubeSize:
                if float(self.delayinput.text) > 0:
                    self.delayinput.text = str(float(self.delayinput.text) - 0.25)

        elif 0.5*self.pixelWidth - 2*self.cubeSize + 3.23*self.cubeSize <= x <= 0.5*self.pixelWidth - 2*self.cubeSize + 3.23*self.cubeSize + int(0.66*self.cubeSize):
            if self.pixelHeight+2.22*self.cubeSize <= y <= self.pixelHeight+2.22*self.cubeSize + int(0.66*self.cubeSize):
                self.back_to_mapeditor = True
        self.drawButtons()
        pg.display.update()


    # def user_write(self, event=None):
    #     if self.delayinput.active:
    #         if event.key == pg.K_BACKSPACE:
    #             self.delayinput.text = self.delayinput.text[:-1]
    #         else:
    #             if len(self.delayinput.text) + 1 <= self.delayinput.ml:
    #                 if self.delayinput.txt_surface.get_width() + 20 <= self.delayinput.w:
    #                     self.delayinput.text += event.unicode

    #         self.delayinput.changed = True
    #         self.delayinput.txt_surface = self.delayinput.font.render(self.delayinput.text, True, self.delayinput.color)
    #         self.drawButtons()
    #         pg.display.update()

