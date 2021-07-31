import pygame

def cut_subsurface(image_link, size_x, size_y):
    image = pygame.image.load(image_link)
    frame_num = int(image.get_width() / size_x)
    frames = []
    for i in range(frame_num):
        frames.append(image.subsurface(i * size_x, 0, size_x, size_y))
    return frames


def readFile(file):
    f = open(file, 'r')
    mes = f.read()
    row_num = mes.split('\n')
    board = []
    for i in row_num:
        row = i.split(' ')
        board.append(row)
    for r in range(len(board)):
        for c in range(len(board[r])):
            board[r][c] = int(board[r][c])
    return board

def print_map(map):
    for r in range(len(map)):
        row = ""
        for c in range(len(map[r])):
            row += ("" + str(map[r][c]))
        print(row)
    print("" * len(map[0]))

def print_best_move_map(shortest_path_tree, map):
    board = [["A" for c in range(len(map[r]))] for r in range(len(map))]
    for tile in shortest_path_tree:
        board[tile[1]][tile[0]] = shortest_path_tree[tile]

    for r in range(len(board)):
        row = ""
        for c in range(len(board[r])):
            length = len(str(board[r][c]))
            row += (5-length) * " " + str(board[r][c])
            row += " "
        print(row)
    print("*" * len(board))