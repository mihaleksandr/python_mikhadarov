import random
def Way(maze):
    cur_cell = maze.all_cells[0]
    way_stack = [cur_cell]
    while cur_cell.x != maze.cols - 1 or cur_cell.y != maze.rows - 1:
        cur_cell.visited = False
        neigh = maze.CellNeighbors(cur_cell, False, True)
        if neigh:
            next_cell = random.choice(neigh)
            way_stack.append(next_cell)
            maze.board[2 * cur_cell.y + 1][2 * cur_cell.x + 1] = '*'
            maze.board[cur_cell.y + next_cell.y + 1][cur_cell.x + next_cell.x + 1] = '*'
            cur_cell = next_cell
        else:
            way_stack.pop()
            next_cell = way_stack[-1]
            maze.board[2 * next_cell.y + 1][2 * next_cell.x + 1] = '_'
            maze.board[cur_cell.y + next_cell.y + 1][cur_cell.x + next_cell.x + 1] = '_'
            cur_cell = next_cell

    maze.board[1][0] = '*'
    maze.board[2 * maze.rows][2 * maze.cols - 1] = '*'
    maze.board[2 * maze.rows - 1][2 * maze.cols - 1] = '*'


def DFS(maze):
    current_cell = maze.all_cells[0]
    stack = [current_cell]
    while stack:
        current_cell.visited = True
        neigh = maze.CellNeighbors(current_cell, True)
        if neigh:
            next_cell = random.choice(neigh)
            stack.append(next_cell)
            maze.DestroyWall(current_cell, next_cell)
            current_cell = next_cell
        else:
            current_cell = stack.pop()


def MinSpanningTree(maze):
    current_cell = maze.all_cells[0]
    front = set(maze.CellNeighbors(current_cell, True))
    current_cell.visited = True
    while front:
        next_cell = random.choice(list(front))
        next_cell.visited = True
        current_cell = random.choice(maze.CellNeighbors(next_cell, False))
        neigh = maze.CellNeighbors(next_cell, True)
        if neigh:
            front = front.union(set(neigh))
        maze.DestroyWall(current_cell, next_cell)
        front.remove(next_cell)


def Kraskal(maze):
    not_visited_cells = maze.all_cells.copy()
    count_set = 0
    while not_visited_cells:
        count_set += 1
        current_cell = random.choice(not_visited_cells)
        current_cell.set = count_set
        current_cell.visited = True
        not_visited_cells.remove(current_cell)
        neigh = maze.CellNeighbors(current_cell, True)
        while neigh:
            next_cell = random.choice(neigh)
            maze.DestroyWall(current_cell, next_cell)
            current_cell = next_cell
            current_cell.set = count_set
            current_cell.visited = True
            not_visited_cells.remove(current_cell)
            neigh = maze.CellNeighbors(current_cell, True)
    current_cell = maze.all_cells[0]
    all_sets = [current_cell.set]
    stack = [current_cell]
    while stack:
        current_cell.visited = False
        neigh = maze.CellNeighbors(current_cell, False)
        if neigh:
            next_cell = random.choice(neigh)
            stack.append(next_cell)
            if next_cell.set != current_cell.set and next_cell.set not in all_sets:
                maze.DestroyWall(current_cell, next_cell)
                all_sets.append(next_cell.set)
            current_cell = next_cell
        else:
            current_cell = stack.pop()
    for i in maze.all_cells:
        i.visited = True

