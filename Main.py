from Env import Env
from MapLoader import ChallengeDesigner
from GuiSolver import Solver
from ai import Agent
from other_agents import AgentInspiration
from Utils import show
from MainGui import GUI
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from MapEditor import MapEditor
from copy import deepcopy
import time

env_style = 1
agent_style = 1

# mode = 'console'
mode = 'gui'


def ask_user():
    mapLoadType = input("load or create? (l/c/d) ")

    if mapLoadType == "l":
        return "load_map", [[], [input('path = ')], [], []]

    if mapLoadType == "c":
        return "create_random_map", [[], [], [env_style, agent_style, int(input("height? : ")) + 2,
                                              int(input("width? : ")) + 2], []]

    if mapLoadType == "d":
        return "design_map", [[], [], [], [env_style,
                                           agent_style,
                                           int(input("height? : ")),
                                           int(input("width? : ")),
                                           input("Boxes? press enter if default : "),
                                           input("Extra Holes? press enter if default : "),
                                           input("Obstacles? press enter if default : ")]]
    return "create", 7, 7


if __name__ == "__main__":
    cubesize = 50


    if mode == 'console':
        initial_Map = ChallengeDesigner().run(*ask_user())

    elif mode == 'gui':

        gui_create = True
        gui_draw = True
        cd_create = True

        while (True):
            if gui_create:
                gui = GUI()
                gui_create = False
                cd_create = True

            if gui_draw:
                gui.draw()
                for event in pg.event.get():

                    if event.type == pg.QUIT:
                        exit()

                    if event.type == pg.MOUSEBUTTONDOWN:
                        gui.user_click(event)

                    if event.type == pg.KEYDOWN:
                        gui.user_write(event)

            if gui.Done == True:
                gui.Done = False

                gui_create = True
                gui_draw = True

                if cd_create:
                    try:
                        cd =  ChallengeDesigner()
                        cd.run(gui.command,gui.inputs)
                        map_array = cd.mapArr

                    except:
                        gui_create = False
                        if gui.command == 'load_map':
                            gui.message = 'No such file !!!'

                        else:
                            gui.message = 'Invalid inputs !!!'
                        continue

                    if gui.command in ['load_map', 'create_random_map']:
                        me = MapEditor(map=map_array,
                                       env_style=gui.env_style,
                                       agent_style=gui.agent_style,
                                       cubeSize=cubesize)

                    else:
                        me = MapEditor(map=map_array,
                                       env_style=gui.env_style,
                                       agent_style=gui.agent_style,
                                       y=gui.inputs[3][2],
                                       x=gui.inputs[3][3],
                                       B=gui.inputs[3][4],
                                       EH=gui.inputs[3][5],
                                       R=gui.inputs[3][6],
                                       cubeSize=cubesize)

                else:
                    me = MapEditor(map=cd.mapArr,
                                   env_style=gui.env_style,
                                   agent_style=gui.agent_style,
                                   cubeSize=cubesize)

                while me.back_to_gui != True:
                    if me.save == True:
                        me.save = False
                        path = cd.save_map(me.map)
                        me.message = path[5:]

                    me.redrawPage()

                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            exit()

                        elif event.type == pg.MOUSEBUTTONDOWN:
                            me.user_click()

                    if me.to_change != []:
                        cd.update_map(me.to_change[0], me.to_change[1], me.to_change[2])
                        map_array = cd.mapArr
                        me.map = map_array
                        me.to_change = []

                    if me.Done == True:
                        sim = Env(deepcopy(cd.mapArr))
                        agent = Agent(sim.send_map)

                        gui_solver = Solver(cubeSize=cubesize, delay=100, state=sim.state, env_style=gui.env_style,
                                            agent_style=gui.agent_style)

                        while not (sim.goal_test() or gui_solver.back_to_mapeditor):

                            show(sim.state.map_array)

                            action = agent.act()
                            while sim.state.validate_action(action.return_action()) is False:
                                action = agent.act()

                            sim.take_action(action.return_action())

                            gui_solver.redrawPage(sim.state, action)
                            
                            start = time.time()

                            while not (time.time()-start > float(gui_solver.delayinput.text)
                                        or gui_solver.back_to_mapeditor
                                        or sim.goal_test()):

                                for event in pg.event.get():

                                    if event.type == pg.QUIT:
                                        exit()

                                    if event.type == pg.MOUSEBUTTONDOWN:
                                        gui_solver.user_click(event)

                                    # if event.type == pg.KEYDOWN:
                                    #     gui_solver.user_write(event)

                            print("successful action")

                        me.back_to_gui = True
                        gui_create = False
                        gui_draw = False
                        gui.Done = True
                        cd_create = False

                        print("победа!!!")
