from ai import Action
import random
from math import exp


class AgentInspiration:
    def __init__(self, env_percption):
        # YOU CAN CHOOSE AGENT TYPE HERE, LOOK AT LINE 20 FOR MORE CHOICES
        self.agent_type = "NErSimAnealAgent"

        self.agent_type_dict = {

            "BruteRandomAgent": self.BruteRandomAgent,
            "WiseRandomAgent": self.WiseRandomAgent,
            "EdgeOrientedAgent": self.EdgeOrientedAgent,
            "NearestEdgeAgent": self.NearestEdgeAgent,
            "NErandAgent": self.NErandAgent,
            "NErSimAnealAgent": self.NErSimAnealAgent,
            "NE1memAgent": self.NE1memAgent,

        }

        self.push_on, self.push_dir, self.last_push_on = None, None, None
        self.perceive = env_percption
        self.sequence = []

        self.t=0

    def act(self):
        if len(self.sequence)!=0: return self.sequence.pop(0)

        result = self.agent_type_dict[self.agent_type]()

        # check if a sequence was returned
        if isinstance(result, list) and \
           not(False in [isinstance(ar, Action) for ar in result]):
            self.sequence = result
            return self.sequence.pop(0)

        if not isinstance(result, Action):
            raise TypeError("Agent did not return an instance of the Action class")

        *self.push_on, self.push_dir = result.return_action()

        return result


    def BruteRandomAgent(self):
        map_array=self.perceive()
        if not self.push_dir or map_array[self.push_on[0]][self.push_on[1]] != 1 or random.random() > 0.75:
            w, h = len(map_array[0]), len(map_array)
            return Action(
                random.randint(1, h - 2), random.randint(1, w - 2), random.choice(["right", "left", "up", "down"]))
        else:
            return Action(*self.push_on, self.push_dir)

    def WiseRandomAgent(self):
        map_array=self.perceive()
        if not self.push_dir or map_array[self.push_on[0]][self.push_on[1]] != 1 or random.random() > 0.75:
            w, h = len(map_array[0]), len(map_array)
            for _ in range(100):
                (i, j) = (random.randint(1, h - 2), random.randint(1, w - 2))
                if map_array[i][j] == 1: break
            return Action(i, j, random.choice(["right", "left", "up", "down"]))
        else:
            return Action(*self.push_on, self.push_dir)

    def EdgeOrientedAgent(self):
        map_array=self.perceive()
        if not self.push_dir or map_array[self.push_on[0]][self.push_on[1]] != 1 or random.random() > 0.75:
            w, h = len(map_array[0]), len(map_array)
            for _ in range(100):
                (i, j) = (random.randint(1, h - 2), random.randint(1, w - 2))
                if map_array[i][j] == 1: break
            if random.random() < 0.5:
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
        else:
            return Action(*self.push_on, self.push_dir)

    def NearestEdgeAgent(self):
        map_array=self.perceive()
        if not self.push_dir or map_array[self.push_on[0]][self.push_on[1]] != 1 or random.random() > 0.75:
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
        else:
            return Action(*self.push_on, self.push_dir)

    def NErandAgent(self):
        map_array=self.perceive()
        if not self.push_dir or map_array[self.push_on[0]][self.push_on[1]] != 1 or random.random() > 0.75:
            w, h = len(map_array[0]), len(map_array)
            for _ in range(100):
                (i, j) = (random.randint(1, h - 2), random.randint(1, w - 2))
                if map_array[i][j] == 1: break
            h_edge_dist = min(i, h - 1 - i)
            v_edge_dist = min(j, w - 1 - j)
            if random.random() < 0.2:
                dir = random.choice(["right", "left", "up", "down"])
            elif h_edge_dist < v_edge_dist:
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
        else:
            return Action(*self.push_on, self.push_dir)

    def NErSimAnealAgent(self):
        map_array=self.perceive()
        if not self.push_dir or map_array[self.push_on[0]][self.push_on[1]] != 1 or random.random() > 0.75:
            w, h = len(map_array[0]), len(map_array)
            for _ in range(100):
                (i, j) = (random.randint(1, h - 2), random.randint(1, w - 2))
                if map_array[i][j] == 1: break
            h_edge_dist = min(i, h - 1 - i)
            v_edge_dist = min(j, w - 1 - j)
            if random.random() < 1 - exp(-self.t / 10):
                dir = random.choice(["right", "left", "up", "down"])
            elif h_edge_dist < v_edge_dist:
                if 2 * i < h:
                    dir = 'up'
                else:
                    dir = 'down'
            else:
                if 2 * j < w:
                    dir = 'left'
                else:
                    dir = 'right'
            self.t = self.t + 1
            return Action(i, j, dir)
        else:
            self.t = self.t + 1
            return Action(*self.push_on, self.push_dir)

    def NE1memAgent(self):
        map_array=self.perceive()
        if not self.push_dir or self.push_on == self.last_push_on and map_array[self.push_on[0]][self.push_on[1]] != 1:
            w, h = len(map_array[0]), len(map_array)
            for _ in range(100):
                (i, j) = (random.randint(1, h - 2), random.randint(1, w - 2))
                if map_array[i][j] == 1: break
            h_edge_dist = min(i, h - 1 - i)
            v_edge_dist = min(j, w - 1 - j)
            if random.random() < 0.2:
                dir = random.choice(["right", "left", "up", "down"])
            elif h_edge_dist < v_edge_dist:
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
            self.last_push_on = (i, j)
        elif self.push_on == self.last_push_on:
            return Action(*self.push_on, random.choice(["right", "left", "up", "down"]))
        else:
            self.last_push_on = self.push_on
            return Action(*self.push_on, self.push_dir)
