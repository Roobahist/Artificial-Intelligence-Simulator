from copy import deepcopy
import time

from Utils import show


class Agent:
    def __init__(self, env_perception):
        # YOU CAN CHOOSE AGENT TYPE HERE, LOOK AT AGENT_TYPE_DICT TO FIND OUT OTHER CHOICES
        self.agent_type = "random"

        # A DICTIONARY OF AVAILABLE AGENT ALGORITHMS. YOU CAN ADD UP MORE TO THIS LIST IF YOU WISH.
        self.agent_type_dict = {

            "A_Star": self.A_Star_agent,
            "IDS": self.IDS_agent,
            "random": self.random_agent,

        }

        self.perceive = env_perception
        self.box_locs   = self.find_loc(self.perceive(), 1)
        self.stone_locs = self.find_loc(self.perceive(),-2)
        self.dropped_boxes = 0
        self.sequence=[]
        self.seen = []
        self.done = False

    # Algorithms which return an *action sequence* or a *single action*

    def find_loc(self,gamemap,value):
        locs = []
        for i in range(len(gamemap)):
            for j in range(len(gamemap[0])):
                if gamemap[i][j] == value:
                    locs.append([i,j])
        return locs

    def A_Star_agent(self):
        map_array = self.perceive()
        action_sequence = []
        ######### EDITABLE SECTION #########


        ######### END OF EDITABLE SECTION #########
        return action_sequence

    def IDS_agent(self):
        answer = None
        map_array = self.perceive()
        action_sequence = []
        ######### EDITABLE SECTION #########
        depth = -1
        while not self.done:
            depth += 1
            print('Depth = ',depth)

            answer = self.DLS(map_array,depth)
            if answer != 'Deeper':
                pass

        if answer not in  ['Failure']:
            while answer.parent != None:
                action_sequence.append(Action(*answer.action))
                answer = answer.parent
        else:
            print('!!! Failure !!!')

        action_sequence = list(reversed(action_sequence))

        ######### END OF EDITABLE SECTION #########
        return action_sequence

    def DLS(self,gamemap,depth):

        root = Node(deepcopy(gamemap),0)
        frontier = [root]
        result = 'Failure'

        while len(frontier) != 0:

            to_expand = frontier[0]
            frontier.remove(frontier[0])

            if len(self.find_loc(to_expand.gamemap, 1)) == 0:
                self.done = True
                return to_expand

            if to_expand.depth >= depth:
                result = 'Deeper'
            else:
                for child in self.expand(to_expand):
                    if child not in self.seen :
                        frontier.append(child)

        if result == 'Failure':
            self.done = True

        return result


    def update_map(self,gamemap, i, j, direction):
        v = 0
        h = 0

        if direction == 'up':
            ahead = [l[j] for l in gamemap][i::-1]
            v = -1

        elif direction == 'down':
            ahead = [l[j] for l in gamemap][i:]
            v = 1

        elif direction == 'left':
            ahead = gamemap[i][j::-1]
            h = -1

        elif direction == 'right':
            ahead = gamemap[i][j:]
            h = 1


        number_of_boxes = 0
        state = 'not_assigned'

        if number_of_boxes == 0 and ahead[0] != 1:
            state = 'no box'

        else:
            for z in range(len(ahead)):

                if ahead[z] == 1:
                    number_of_boxes += 1
                    continue

                if ahead[z] == -1:
                    state = 'fire'
                    break

                if ahead[z] == -2:
                    state = 'stone'
                    break

                if ahead[z] == 0:
                    state = 'empty'
                    break


        if state == 'no box':
            pass

        elif state == 'stone':
            pass

        elif state == 'empty':
            gamemap[i][j] = 0
            gamemap[i + v * number_of_boxes][j + h * number_of_boxes] = 1

        elif state == 'fire':
            gamemap[i][j] = 0

        return gamemap

    def expand(self,parent):
        gamemap = parent.gamemap
        children = []

        directions = ['up','down','left','right']
        box_locs = self.find_loc(gamemap, 1)
        for box_loc in box_locs:
            for direction in directions :
                child_map = self.update_map(deepcopy(gamemap),box_loc[0],box_loc[1],direction)
                children.append(Node(child_map,
                                    parent.depth+1,
                                    parent,
                                    [box_loc[0],box_loc[1],direction]))

        return children


    def random_agent(self):
        import random

        map_array = self.perceive()

        w, h = len(map_array[0]), len(map_array)
        for _ in range(100):
            (i, j) = (random.randint(1, h - 2), random.randint(1, w - 2))
            if map_array[i][j] == 1: break
        h_edge_dist = min(i, h - 1 - i)
        v_edge_dist = min(j, w - 1 - j)
        if h_edge_dist < v_edge_dist:
            if 2 * i < h:
                dir = 'up'
            else:
                dir = 'down'
        else:
            if 2 * j < w:
                dir = 'left'
            else:
                dir = 'right'

        return Action(i, j, dir)


    def act(self):

        # If sequence not empty, pops another action
        if len(self.sequence)!=0: return self.sequence.pop(0)

        # Result is whether a sequence or a single action object
        result = self.agent_type_dict[self.agent_type]()

        # check if the result was a sequence
        if isinstance(result, list) and not(False in [isinstance(ar, Action) for ar in result]):
            self.sequence = result
            return self.sequence.pop(0)

        # As it was not a sequence, this line assures the result was a valid single action
        if not isinstance(result, Action):

            raise TypeError("Agent did not return an instance of the class Action")

        return result

class State:
    pass

class Node:
    def __init__(self, gamemap, depth, parent=None, action=None):
        self.action = action
        self.gamemap = gamemap
        self.depth = depth
        self.parent = parent
    pass

class Action:
    def __init__(self,i,j,direction):
        self.update(i,j,direction)

    def update(self, i, j, direction):
        # Validates the action format as (int, int, string)
        if not (isinstance(i, int) and isinstance(j, int) and isinstance(direction, str)):
            raise TypeError("x, y or direction has wrong type")

        self.x = i
        self.y = j
        self.direction = direction

    def return_action(self): return (self.x, self.y, self.direction)
