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

def spiral_number(x, y):
    m = max(x, y)
    return (m+1)*(m+1)//2

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
        self.MAX_LIMIT = len(self.box_list) * spiral_number(self.x, self.y)
        self.IDS()
    

    # https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search
    def IDS(self):
        for i in range(len(self.box_list),self.MAX_LIMIT):
            found, remaining = self.DLS(self.root_node, i)
            if found != None:
                self.action_list = found.action_seq
                break
            elif not remaining:
                print("go deeper")

    def DLS(self, node, depth):
        if depth == 0:
            if len(node.box_list) == 0:
               return (node, True) 
            else:
                return (None, True)

        elif depth > 0:
            any_remaining = False
            childs = get_childs(node)
            while not childs.empty():
                next_node = childs.get()[1]
                found, remaining = self.DLS(next_node, depth-1)
                if found != None:
                    self.action_list = found.action_seq
                    return (found, True)
                elif remaining:
                    any_remaining = True
            return (None, any_remaining)


    def act(self):
        self.list_iter += 1 
        return self.action_list[self.list_iter]


class Node:
    def __init__(self, gamemap=None, cost=0, action_seq=None):
        self.gamemap = gamemap
        self.x = len(self.gamemap[0]) - 2
        self.y = len(self.gamemap) - 2
        self.box_list = sorted(get_box_loc(self.gamemap, self.x, self.y, 1))
        self.stone_list = get_box_loc(self.gamemap, self.x, self.y, -2)
        self.cost = cost
        self.action_seq = action_seq

    def __lt__(self, other):
        return False

class Action:
    def __init__(self,i,j,direction):
        self.x = i
        self.y = j
        self.direction = direction

    def return_action(self): 
        return (self.x, self.y, self.direction)

def get_childs(node):
    actions = []
    priority = pq() 
    direc = ["up", "down", "right", "left"]
    for i in range(len(node.box_list)):
        for j in range(4):
            new_act = Action(node.box_list[i][0], node.box_list[i][1], direc[j])
            newmap_gamemap, result = do_action(node, new_act)
            if result > 0:
                newaction_seq = deepcopy(node.action_seq)
                new_act.y = node.box_list[i][0]
                new_act.x = node.box_list[i][1]
                newaction_seq.append(new_act)
                priority.put((-1*result, Node(newmap_gamemap, action_seq=newaction_seq)))

    return priority

def do_action(node, action):
    new_gamemap = deepcopy(node.gamemap)
    j, i = action.y, action.x
    dj, di = dir_dic[action.direction]
    n = 1
    while new_gamemap[n*dj+j][n*di+i] == 1:
        n += 1
    
    result = -1
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
 
    return new_gamemap, result
