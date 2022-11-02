def possible_locs(location, map):
    x = location[0]
    y = location[1]
    all_moves = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
    possible = []
    for move in all_moves:
        if 0 <= move[0] <= len(map) - 1:
            if 0 <= move[1] <= len(map[0]) - 1:
                if map[move[0]][move[1]] == 0:
                    possible.append(move)
        continue
    return possible


def show(array):
    for i in range(len(array)):
        to_print = ''
        for j in range(len(array[i])):
            to_print += str(array[i][j]).zfill(2)
            to_print += ' , '
        to_print = to_print[:-2]
        print(to_print)


def base_map(height, width):
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
    return map_array
