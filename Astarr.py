## 1  box
## 0  empty
## -1 fall
## -2 stone

from copy import deepcopy
from queue import PriorityQueue as pq

dir_dic = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}

def get_box_loc(gamemap, x, y, value):
    box_list = []
    for j in range(1, y+1):
        for i in range(1, x+1):
            if gamemap[j][i] == value:
                box_list.append((i,j))
    return box_list


class Agent:
    def __init__(self, env_perception):
        self.perceive = env_perception()
        ## due to lack of time checking that map is actually solvable is not written, so sorry for that.
        self.x = len(self.perceive[0]) - 2
        self.y = len(self.perceive) - 2
        self.box_list = get_box_loc(self.perceive, self.x, self.y, 1)
        self.stone_list = get_box_loc(self.perceive, self.x, self.y, -2)
        self.root_node = Node(gamemap=deepcopy(self.perceive), cost=0, action_seq = [])
        self.action_list = []
        self.list_iter = -1
        self.A_asterisk()
    

    # Based on pseudocode available at aima book v4. 
    # Sorry for not implementing Problem structure
    def A_asterisk(self):
        root_node = self.root_node
        frontier = pq() 
        frontier.put((root_node.path_cost, 0, root_node))
        reached = {}
        reached[root_node.box_list] = root_node 
        while not frontier.empty():
            node = frontier.get()[2]
            if len(node.box_list) == 0:
                self.action_list = node.action_seq
                return node
            for child in expand(node):
                if child not in reached or reached[child.box_list].path_cost > child.path_cost:
                    reached[child.box_list] = child
                    frontier.put((child.path_cost, child.last_act_value, child))
                    #frontier.put((child.path_cost, 0, child))
        return None            
            

    def act(self):
        self.list_iter += 1 
        return self.action_list[self.list_iter]


class Node:
    def __init__(self, gamemap=None, cost=0, h=None, action_seq=None, box_n=None, act_priority=None):
        self.gamemap = gamemap
        self.x = len(self.gamemap[0]) - 2
        self.y = len(self.gamemap) - 2
        self.box_list = tuple(sorted(get_box_loc(self.gamemap, self.x, self.y, 1)))
        self.stone_list = get_box_loc(self.gamemap, self.x, self.y, -2)
        self.cost = cost
        self.boxs_moved = box_n
        self.h = heuristic(self)
        self.path_cost = cost + self.h
        self.action_seq = action_seq
        self.last_act_value = act_priority

    def __lt__(self, other):
        return False

class Action:
    def __init__(self,i,j,direction):
        self.x = i
        self.y = j
        self.direction = direction

    def return_action(self): 
        return (self.x, self.y, self.direction)

def expand(node):   
    direc = ["up", "down", "right", "left"]
    for i in range(len(node.box_list)):
        for j in range(4):
            new_act = Action(node.box_list[i][0], node.box_list[i][1], direc[j])
            newmap_gamemap, result, n, cost = do_action(node, new_act)
            if result > 0:
                newaction_seq = deepcopy(node.action_seq)
                new_act.y = node.box_list[i][0]
                new_act.x = node.box_list[i][1]
                newaction_seq.append(new_act)
                newcost = node.cost + cost 
                #print(newcost, len(get_box_loc(newmap_gamemap, node.x, node.y, 1)))
                yield Node(newmap_gamemap, action_seq=newaction_seq, cost=newcost, box_n=n, act_priority=(-1)*result)

def heuristic(node):
    result = 0
    for i in range(len(node.box_list)):
        result += min(node.box_list[i][0], node.box_list[i][1], node.x - node.box_list[i][0], node.y - node.box_list[i][1])
    return result*4

def do_action(node, action):
    new_gamemap = deepcopy(node.gamemap)
    j, i = action.y, action.x
    dj, di = dir_dic[action.direction]
    n = 1
    while new_gamemap[n*dj+j][n*di+i] == 1:
        n += 1
    result = -1
    action_cost = n+4
    x = new_gamemap[n*dj+j][n*di+i]
    if x == -1 or x == 0:
        new_gamemap[j][i] = 0
        new_gamemap[n*dj+j][n*di+i] = x+x+1
        result = n*(-x)+1
        if node.action_seq:
            ex_j, ex_i, dirc = node.action_seq[-1].x, node.action_seq[-1].y, node.action_seq[-1].direction
            exdj, exdi = dir_dic[dirc]
            if i == ex_i + exdi and j == ex_j + exdj and dirc == action.direction:
                result += node.x * node.y
                action_cost -= 4
                if node.boxs_moved != None:
                    if n > 2*node.boxs_moved:
                        action_cost += 4
    return new_gamemap, result, n, action_cost
