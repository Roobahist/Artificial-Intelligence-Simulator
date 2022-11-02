import random
from Utils import possible_locs, show, base_map
from MapEditor import MapEditor
import pygame as pg
import os
import math


class ChallengeDesigner:

    def __init__(self):
        self.mapArr = None

    def run(self, command, inputs):
        if command == "load_map":
            load_map_inputs = inputs[1]
            self.load_map(*load_map_inputs)

        elif command == "create_random_map":
            create_random_map_inputs = inputs[2]
            self.create_random_map(*create_random_map_inputs)

        elif command == "design_map":
            design_map_inputs = inputs[3]
            self.base_map(height=design_map_inputs[2],
                          width=design_map_inputs[3])

        else:
            raise ValueError("wrong arg sent to map creator")

    def base_map(self, height, width):
        width = width + 2
        height = height + 2
        map_array = []
        for i in range(height):
            row = []
            for j in range(width):
                if j == 0 or j == width - 1 or i == 0 or i == height - 1:
                    row.append(-1)
                else:
                    row.append(0)
            map_array.append(row)

        self.mapArr = map_array

    def update_map(self, row, column, value):
        self.mapArr[row][column] = value

    def create_random_map(self, env_style, agent_style, height, width):
        map_array = []
        stone_locs = []
        empty_locs = []
        hole_locs = []
        box_locs = []

        map_array = base_map(height, width)

        N = height * width
        number_of_boxes = math.floor(0.5 * N)
        number_of_stones = math.floor(0.05 * N)
        number_of_extraholes = 0

        for i in range(len(map_array)):
            for j in range(len(map_array[0])):
                if j == 0 or j == width - 1 or i == 0 or i == height - 1:
                    hole_locs.append([i, j])

        for i in range(number_of_stones):
            placed = False
            while not (placed):
                row = random.randrange(0, len(map_array), 1)
                col = random.randrange(0, len(map_array[0]), 1)
                if map_array[row][col] != -2:
                    map_array[row][col] = -2
                    placed = True
            stone_locs.append([row, col])

        for i in range(number_of_extraholes):
            placed = False
            while not (placed):
                row = random.randrange(1, len(map_array) - 1, 1)
                col = random.randrange(1, len(map_array[0]) - 1, 1)
                if map_array[row][col] != -2:
                    map_array[row][col] = -1
                    placed = True
            hole_locs.append([row, col])

        i = 0
        while i < number_of_boxes:
            i += 1
            current_loc = random.choice(hole_locs)
            steps_num = random.randint(1, int(height * width / 2))

            if len(possible_locs(current_loc, map_array)) == 0:
                i -= 1
                continue

            for j in range(steps_num):
                if len(possible_locs(current_loc, map_array)) != 0:
                    current_loc = random.choice(possible_locs(current_loc, map_array))
                else:
                    break

            map_array[current_loc[0]][current_loc[1]] = 1
            box_locs.append(current_loc)

        self.mapArr = map_array

    def load_map(self, path):
        import pickle
        path = path.replace('\\', '\\')
        map_array = pickle.load(open(path + '.pickle', "rb"))

        self.mapArr = map_array

    def save_map(self, map_array):
        import pickle
        maps = os.listdir('maps')
        name = 'map_' + str(len(maps)) + '.pickle'

        i = 1
        while name in maps:
            name = 'map_' + str(len(maps) + i) + '.pickle'
            i += 1

        path = 'maps\\' + str(name)

        pickle.dump(map_array, open(path, "wb"))

        return path
