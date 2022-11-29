class Maze():
    def __init__(self, rows, cols, all_cells):
        self.rows = rows
        self.cols = cols
        self.board = [[0] * (2 * cols + 1) for i in range(2 * rows + 1)]
        self.all_cells = all_cells

    def InitBoard(self):
        for i in range(2 * self.rows + 1):
            for j in range(2 * self.cols + 1):
                if i % 2 == 0:
                    self.board[i][j] = '█'
                else:
                    if j % 2 == 1:
                        self.board[i][j] = '_'
                    else:
                        self.board[i][j] = '█'
        self.board[2 * self.rows][2 * self.cols - 1] = '_'
        self.board[1][0] = '_'

    def CellNeighbors(self, cell, next, divided=False):
        neighb = []
        bottom = self.Check(cell.x, cell.y + 1)
        top = self.Check(cell.x, cell.y - 1)
        left = self.Check(cell.x - 1, cell.y)
        right = self.Check(cell.x + 1, cell.y)
        if next:
            if top and not top.visited:
                neighb.append(top)
            if right and not right.visited:
                neighb.append(right)
            if left and not left.visited:
                neighb.append(left)
            if bottom and not bottom.visited:
                neighb.append(bottom)
        elif divided:
            if bottom and not self.Divided(bottom, cell) and bottom.visited:
                neighb.append(bottom)
            if top and not self.Divided(top, cell) and top.visited:
                neighb.append(top)
            if left and not self.Divided(left, cell) and left.visited:
                neighb.append(left)
            if right and not self.Divided(right, cell) and right.visited:
                neighb.append(right)
        else:
            if top and top.visited:
                neighb.append(top)
            if right and right.visited:
                neighb.append(right)
            if left and left.visited:
                neighb.append(left)
            if bottom and bottom.visited:
                neighb.append(bottom)
        if neighb:
            return neighb
        return False

    def Check(self, x, y):
        if x < 0 or x >= self.cols or y < 0 or y >= self.rows:
            return False
        return self.all_cells[x + y * self.cols]

    def DestroyWall(self, cur, next):
        self.board[cur.y + next.y + 1][cur.x + next.x + 1] = '_'

    def Divided(self, cur, next):
        if self.board[cur.y + next.y + 1][cur.x + next.x + 1] == '_':
            return False
        return True

    def CheckSet(self, cell):
        neighb = []
        bottom = self.Check(cell.x, cell.y + 1)
        top = self.Check(cell.x, cell.y - 1)
        left = self.Check(cell.x - 1, cell.y)
        right = self.Check(cell.x + 1, cell.y)
        if top and top.set != cell.set and top.set > 0:
            neighb.append(top)
        if bottom and bottom.set != cell.set and bottom.set > 0:
            neighb.append(bottom)
        if left and left.set != cell.set and left.set > 0:
            neighb.append(left)
        if right and right.set != cell.set and right.set > 0:
            neighb.append(right)
        if neighb:
            return neighb
        return False

class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.set = 0
