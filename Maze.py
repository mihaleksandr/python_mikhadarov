import random
import pygame


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


def Interface():
    FONT = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 20)
    dis = pygame.display.set_mode((500, 500))
    input_box1 = InputBox(100, 300, 140, 40, dis)
    input_box2 = InputBox(100, 400, 140, 40, dis)
    input_boxes = [input_box1, input_box2]
    pygame.display.set_caption('Maze')
    mode = ''
    text = FONT.render('', True, (255, 255, 255))
    text_r = small_font.render('нажмите f, если нужно открыть файл', True, (255, 255, 255))
    file = False
    start_render = False
    first = True
    global game_over
    while not game_over:
        keys = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN and not start_render:
                if event.key == pygame.K_LEFT:
                    mode = "DFS"
                if event.key == pygame.K_RIGHT:
                    mode = "Kraskal"
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    mode = "MST"
                if event.key == pygame.K_f:
                    file = True
                if event.key == pygame.K_RETURN:
                    if input_boxes[0].text and input_boxes[1].text and mode or file:
                        start_render = True
                    else:
                        text = FONT.render('Введите все значения', True, (255, 255, 255))

            if event.type == pygame.KEYDOWN and start_render:
                if event.key == pygame.K_LEFT:
                    keys.append(pygame.K_LEFT)
                if event.key == pygame.K_RIGHT:
                    keys.append(pygame.K_RIGHT)
                if event.key == pygame.K_UP:
                    keys.append(pygame.K_UP)
                if event.key == pygame.K_DOWN:
                    keys.append(pygame.K_DOWN)
                if event.key == pygame.K_SPACE:
                    keys.append(pygame.K_SPACE)
            for box in input_boxes:
                box.handle_event(event)

        dis.fill((0, 0, 0))
        if start_render:
            if first:
                if file:
                    with open("maze.txt", "r") as file_maze:
                        board = []
                        while True:
                            line = file_maze.readline()
                            if not line:
                                break
                            board.append(list(line))
                    rows = (len(board) - 1) // 2
                    cols = (len(board[0]) - 2) // 2
                    all_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
                    maze = Maze(rows, cols, all_cells)
                    maze.board = board
                    for i in all_cells:
                        i.visited = True
                else:
                    rows = int(input_boxes[0].text)
                    cols = int(input_boxes[1].text)
                    all_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
                    maze = Maze(rows, cols, all_cells)
                    maze.InitBoard()
                maze.board[1][1] = '+'
                current_cell = maze.all_cells[0]
                rect_side = min(800 // (2 * maze.rows + 1), 800 // (2 * maze.cols + 1))
                dis = pygame.display.set_mode((rect_side * (2 * maze.cols + 1), rect_side * (2 * maze.rows + 1) + 20))
                if mode == "DFS":
                    DFS(maze)
                if mode == "MST":
                    MinSpanningTree(maze)
                if mode == "Kraskal":
                    Kraskal(maze)
                first = False
            current_cell = Render(maze, dis, current_cell, rect_side, keys)

        else:
            for box in input_boxes:
                box.update()
            for box in input_boxes:
                box.draw()
            text1 = FONT.render('Выбранный режим генерации', True, (255, 255, 255))
            dis.blit(text1, (10, 30))
            text1 = small_font.render('Выбирайте стрелочками', True, (255, 255, 255))
            dis.blit(text1, (10, 70))
            text2 = FONT.render(mode, True, (255, 255, 255))
            dis.blit(text2, (70, 100))
            dis.blit(text, (100, 450))
            text_21 = small_font.render('Высота', True, (255, 255, 255))
            dis.blit(text_21, (100, 280))
            text_22 = small_font.render('Ширина', True, (255, 255, 255))
            dis.blit(text_22, (100, 380))
            dis.blit(text_r, (200, 200))
        pygame.display.update()
        clock.tick(30)
    pygame.quit()
    quit()


def Render(maze, dis, current_cell, rect_side, keys):
    small_font = pygame.font.Font(None, 20)
    big_font = pygame.font.Font(None, 80)
    global game_over
    if pygame.K_LEFT in keys:
        next_cell = maze.Check(current_cell.x - 1, current_cell.y)
        if next_cell and not maze.Divided(current_cell, next_cell):
            maze.board[2 * next_cell.y + 1][2 * next_cell.x + 1] = '+'
            maze.board[2 * current_cell.y + 1][2 * current_cell.x + 1] = '_'
            current_cell = next_cell
    if pygame.K_RIGHT in keys:
        next_cell = maze.Check(current_cell.x + 1, current_cell.y)
        if next_cell and not maze.Divided(current_cell, next_cell):
            maze.board[2 * next_cell.y + 1][2 * next_cell.x + 1] = '+'
            maze.board[2 * current_cell.y + 1][2 * current_cell.x + 1] = '_'
            current_cell = next_cell
    if pygame.K_UP in keys:
        next_cell = maze.Check(current_cell.x, current_cell.y - 1)
        if next_cell and not maze.Divided(current_cell, next_cell):
            maze.board[2 * next_cell.y + 1][2 * next_cell.x + 1] = '+'
            maze.board[2 * current_cell.y + 1][2 * current_cell.x + 1] = '_'
            current_cell = next_cell
    if pygame.K_DOWN in keys:
        next_cell = maze.Check(current_cell.x, current_cell.y + 1)
        if next_cell and not maze.Divided(current_cell, next_cell):
            maze.board[2 * next_cell.y + 1][2 * next_cell.x + 1] = '+'
            maze.board[2 * current_cell.y + 1][2 * current_cell.x + 1] = '_'
            current_cell = next_cell
    if pygame.K_SPACE in keys:
        Way(maze)

    for i in range(2 * maze.rows + 1):
        for j in range(2 * maze.cols + 1):
            if maze.board[i][j] == '█':
                pygame.draw.rect(dis, (255, 255, 255),
                                 (j * rect_side + 1, i * rect_side + 1, rect_side - 2, rect_side - 2))
            if maze.board[i][j] == '_':
                pygame.draw.rect(dis, (255, 255, 255), (j * rect_side, i * rect_side, rect_side, rect_side), 1)
            if maze.board[i][j] == '*':
                pygame.draw.rect(dis, (64, 128, 255), (j * rect_side, i * rect_side, rect_side, rect_side))
            if maze.board[i][j] == '+':
                pygame.draw.rect(dis, (255, 102, 0), (j * rect_side, i * rect_side, rect_side, rect_side))
    if current_cell.x == maze.cols - 1 and current_cell.y == maze.rows - 1:
        dis.fill((0, 0, 0))
        text = big_font.render("Поздравляем!", True, (255, 255, 255))
        dis.blit(text, (200, 400))
    text = small_font.render("используйте стрелочки для движения", True, (255, 255, 255))
    dis.blit(text, (10, rect_side * (2 * maze.rows + 1)))
    text = small_font.render("нажмите пробел чтобы показать путь", True, (255, 255, 255))
    dis.blit(text, (500, rect_side * (2 * maze.rows + 1)))
    return current_cell


class InputBox:
    def __init__(self, x, y, w, h, dis, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.Font(None, 40)
        self.active = False
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.txt_surface = self.font.render(text, True, self.color)
        self.dis = dis

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self):
        # Blit the text.
        self.dis.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))
        # Blit the rect.
        pygame.draw.rect(self.dis, self.color, self.rect, 1)


clock = pygame.time.Clock()
pygame.init()
game_over = False
Interface()
