import pygame
import Labirinth
import socket
import Generation


def Interface():
    pygame.init()
    FONT = pygame.font.Font(None, 40)
    dis = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Maze')
    big_font = pygame.font.Font(None, 80)
    game_over = False
    start_render = False
    input_box1 = InputBox(100, 150, 140, 40, dis)
    input_box2 = InputBox(100, 350, 140, 40, dis)
    input_boxes = [input_box1, input_box2]
    clock = pygame.time.Clock()
    cols = '0'
    str_maze = ''
    text_1 = FONT.render('', True, (255, 255, 255))
    defeat = False
    while not game_over:
        dis.fill((0, 0, 0))
        keys = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                client_socket.close()
            if event.type == pygame.KEYDOWN:
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
                if event.key == pygame.K_RETURN:
                    if input_boxes[0].text and input_boxes[1].text:
                        start_render = True
                        client_socket.connect((input_boxes[0].text, int(input_boxes[1].text)))
                    else:
                        text_1 = FONT.render('Введите все значения', True, (255, 255, 255))
            for box in input_boxes:
                box.handle_event(event)
        if start_render:
            if cols == '0':
                #rows = client_socket.recv(65536).decode()
                #cols = client_socket.recv(65536).decode()
                rows = 10
                cols = 10
                str_maze = client_socket.recv(65536).decode()
                rows = int(rows)
                cols = int(cols)
                all_cells = [Labirinth.Cell(col, row) for row in range(rows) for col in range(cols)]
                maze = Labirinth.Maze(rows, cols, all_cells)
                current_cell = maze.all_cells[0]
                rect_side = min(800 // (2 * maze.rows + 1), 800 // (2 * maze.cols + 1))
                dis = pygame.display.set_mode((rect_side * (2 * maze.cols + 1), rect_side * (2 * maze.rows + 1) + 20))
                for i in range(2 * rows + 1):
                    for j in range(2 * cols + 1):
                        maze.board[i][j] = str_maze[i * (2 * cols + 1) + j]
            else:
                current_cell = Render(maze, dis, current_cell, rect_side, keys)
                try:
                    mes = client_socket.recv(1024).decode()
                    if mes == 'Victory':
                        defeat = True
                except:
                    pass
                if defeat:
                    dis.fill((0, 0, 0))
                    text = big_font.render("Победа соперника", True, (255, 255, 255))
                    dis.blit(text, (200, 400))
                    pygame.display.update()

        else:
            for box in input_boxes:
                box.update()
            for box in input_boxes:
                box.draw()
            dis.blit(text_1, (100, 450))
            text = FONT.render('Введите IP сервера', True, (255, 255, 255))
            dis.blit(text, (120, 100))
            text = FONT.render('Введите порт сервера', True, (255, 255, 255))
            dis.blit(text, (120, 300))

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
        Generation.Way(maze)

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
        client_socket.send('Victory'.encode())
        text = big_font.render("Поздравляем!", True, (255, 255, 255))
        dis.blit(text, (200, 400))
    text = small_font.render("используйте стрелочки для движения", True, (255, 255, 255))
    dis.blit(text, (10, rect_side * (2 * maze.rows + 1)))
    #text = small_font.render("нажмите пробел чтобы показать путь", True, (255, 255, 255))
    #dis.blit(text, (500, rect_side * (2 * maze.rows + 1)))
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
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self):
        self.dis.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))
        pygame.draw.rect(self.dis, self.color, self.rect, 1)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
Interface()
