from copy import deepcopy


def show(array):
    for i in range(len(array)):
        to_print = ''
        for j in range(len(array[i])):
            to_print += str(array[i][j]).zfill(2)
            to_print += ' , '
        to_print = to_print[:-2]
        print(to_print)


class State:
    def __init__(self, map):
        self.previous_map = map
        self.map_array = map
        self.cost = 0
        self.no_initial_cost_move = -1, -1, 'left'
        self.last_state = None
        self.ahead = None
        self.v = None
        self.h = None
        self.number_of_boxes = None
        self.prev_num_box=0

    def update(self, i, j, direction):
        self.previous_map = deepcopy(self.map_array)

        self.update_score(i, j, direction)
        self.update_map(i, j, direction)

    def update_score(self, i, j, direction):
        initI, initJ = i, j
        p_cost_conf = 4
        if (i, j, direction) == self.no_initial_cost_move:
            self.prev_num_box *= 2
            penalty_cost = 0
        else:
            penalty_cost = p_cost_conf

        self.number_of_boxes = 0
        self.last_state = 'not_assigned'
        di, dj = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}[direction]
        self.v, self.h = di, dj
        print(i,j)
        if self.map_array[i][j] != 1: self.last_state = 'no box'
        else:
            while True:
                if self.map_array[i][j] != 1: break
                self.number_of_boxes += 1
                i, j = i + di, j + dj
            self.last_state = {-1: 'fire', -2: 'stone', 0: 'empty'}[self.map_array[i][j]]
            if self.number_of_boxes > self.prev_num_box: penalty_cost = p_cost_conf

        if self.last_state == 'no box':
            self.no_initial_cost_move = -1, -1, 'left'

        elif self.last_state == 'stone':
            self.no_initial_cost_move = initI, initJ, direction

        elif self.last_state == 'empty':
            self.no_initial_cost_move = initI + di, initJ + dj, direction

        elif self.last_state == 'fire':
            self.no_initial_cost_move = initI + di, initJ + dj, direction

        # print('&&&&&&&&&&&&&&&&&&&&&&&')
        # print('i , j = ',i,' , ',j)
        # print('state = ',state)
        # print('no_initial_cost_move = ',self.no_initial_cost_move)
        # print('initial_cost = ',initial_cost)
        # print('number_of_boxes = ',number_of_boxes)
        # print('cost = ',initial_cost + number_of_boxes)
        # print('&&&&&&&&&&&&&&&&&&&&&&&')

        self.prev_num_box = self.number_of_boxes
        self.cost += penalty_cost + self.number_of_boxes

    def update_map(self, i, j, direction):
        v = 0
        h = 0

        if direction == 'up':
            ahead = [l[j] for l in self.map_array][i::-1]
            v = -1

        elif direction == 'down':
            ahead = [l[j] for l in self.map_array][i:]
            v = 1

        elif direction == 'left':
            ahead = self.map_array[i][j::-1]
            h = -1

        elif direction == 'right':
            ahead = self.map_array[i][j:]
            h = 1

        print(ahead)

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

                    # print('==================================')
        # print('state = ',state)                    
        # print('number_of_boxes = ',number_of_boxes)  
        # print('i = ',i + v*number_of_boxes)       
        # print('j = ',j + h*number_of_boxes)       
        # # print('cost = ', 1+number_of_boxes)           
        # print('==================================')

        if state == 'no box':
            # self.no_initial_cost_move = -1 , -1 , 'left'
            pass

        elif state == 'stone':
            # self.no_initial_cost_move = i , j , direction
            pass

        elif state == 'empty':
            self.map_array[i][j] = 0
            self.map_array[i + v * number_of_boxes][j + h * number_of_boxes] = 1
            # self.no_initial_cost_move = i+v , j+h , direction

        elif state == 'fire':
            self.map_array[i][j] = 0
            # self.no_initial_cost_move = i+v , j+h , direction

        # print('no cost = ',self.no_initial_cost_move)

        # print('+++++++++++++++++++++++')
        # show(self.map_array)
        # print('+++++++++++++++++++++++')

    def validate_action(self, action):
        i, j, direction = action[0], action[1], action[2]
        # Checks if the direction is valid
        if direction not in ["up", "down", "right", "left"]:
            print("invalid, action name is wrong")
            return False

        # Makes sure if the coordinates are within range
        if 1 > i or i > len(self.map_array) - 2 or \
                1 > j or j > len(self.map_array[0]) - 2:
            print("invalid, chosen coordinate out of border")
            return False

        # Makes sure if it's chosen a box
        # if self.map_array[x][y] != 1:
        #     print("invalid, no box in this slot")
        #     return False

        return True


class Env:
    def __init__(self, map):
        self.state = State(map)

    def __eq__(self, obj):
        return isinstance(obj, Env) and \
               obj.state.ex_dir == self.state.ex_dir and \
               obj.state.ex_move == self.state.ex_move and \
               obj.state.map_array == self.state.map_array

    def take_action(self, action):
        self.state.update(*action)

    def send_map(self):
        from copy import deepcopy
        return deepcopy(self.state.map_array)

    def send_cost(self):
        return self.state.cost

    def copy_env(self):
        from copy import deepcopy
        a = Env(deepcopy(self.state.map_array))
        a.state = deepcopy(self.state)
        return a

    def goal_test(self):
        if any(1 in sublist for sublist in self.state.map_array):
            return False
        print("Total cost = " + str(self.state.cost))
        return True

    def __deepcopy__(self, memo):
        from copy import deepcopy
        id_self = id(self)  # memoization avoids unnecesary recursion
        _copy = memo.get(id_self)
        if _copy is None:
            _copy = type(self)( deepcopy(self.state.map_array, memo) )
            _copy.state.cost = deepcopy(self.state.cost, memo)
            _copy.state.ex_dir = deepcopy(self.state.ex_dir, memo)
            _copy.state.ex_move = deepcopy(self.state.ex_move, memo)
            _copy.state.prev_num_box = deepcopy(self.state.prev_num_box, memo)
            memo[id_self] = _copy
        return _copy
