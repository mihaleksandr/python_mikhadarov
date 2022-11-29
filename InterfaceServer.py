import pygame
import Generation
import Labirinth
import socket
import http.client

def Interface():
    pygame.init()
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
    game_over = False
    clock = pygame.time.Clock()
    main_socket.listen(2)
    players_socket = []
    score = 0
    score_curr = 5000
    while not game_over:
        keys = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                main_socket.close()
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
                    all_cells = [Labirinth.Cell(col, row) for row in range(rows) for col in range(cols)]
                    maze = Labirinth.Maze(rows, cols, all_cells)
                    maze.board = board
                    for i in all_cells:
                        i.visited = True
                else:
                    rows = int(input_boxes[0].text)
                    cols = int(input_boxes[1].text)
                    all_cells = [Labirinth.Cell(col, row) for row in range(rows) for col in range(cols)]
                    maze = Labirinth.Maze(rows, cols, all_cells)
                    maze.InitBoard()
                maze.board[1][1] = '+'
                current_cell = maze.all_cells[0]
                rect_side = min(800 // (2 * maze.rows + 1), 800 // (2 * maze.cols + 1))
                dis = pygame.display.set_mode((rect_side * (2 * maze.cols + 1), rect_side * (2 * maze.rows + 1) + 20))
                if mode == "DFS":
                    Generation.DFS(maze)
                if mode == "MST":
                    Generation.MinSpanningTree(maze)
                if mode == "Kraskal":
                    Generation.Kraskal(maze)
                if players_socket:
                    str_maze = ''
                    for row in maze.board:
                        str_maze += ''.join([elem for elem in row])
                    players_socket[0].send(str_maze.encode())
                first = False
            current_cell = Render(maze, dis, current_cell, rect_side, keys, players_socket, score)

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
            dis.blit(text_r, (30, 150))
            text_3 = small_font.render("Подключенные игроки", True, (255, 255, 255))
            dis.blit(text_3, (280, 180))
            text_3 = small_font.render("локальныый IP и номер порта", True, (255, 255, 255))
            dis.blit(text_3, (40, 180))
            text_3 = small_font.render(str(socket.gethostbyname(socket.gethostname())), True, (255, 255, 255))
            dis.blit(text_3, (40, 220))
            text_3 = small_font.render(str(25000), True, (255, 255, 255))
            dis.blit(text_3, (150, 220))
            if players_socket:
                text_4 = small_font.render(str(players_socket[0].getsockname()), True, (255, 255, 255))
                dis.blit(text_4, (280, 220))
            try:
                new_socket, addr = main_socket.accept()
                print("Подлючение")
                new_socket.setblocking(False)
                players_socket.append(new_socket)
            except:
                pass
        pygame.display.update()
        score_curr -= 5
        clock.tick(30)
    pygame.quit()
    quit()


def Render(maze, dis, current_cell, rect_side, keys, players_socket, score):
    vict = False
    small_font = pygame.font.Font(None, 20)
    big_font = pygame.font.Font(None, 80)
    global defeat
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
        text = big_font.render("Поздравляем!", True, (255, 255, 255))
        defeat = True
        dis.blit(text, (200, 400))

    text = small_font.render("используйте стрелочки для движения", True, (255, 255, 255))
    dis.blit(text, (10, rect_side * (2 * maze.rows + 1)))
    if players_socket:
        text = small_font.render("Текущий счет:", True, (255, 255, 255))
        dis.blit(text, (500, rect_side * (2 * maze.rows + 1)))
        text = small_font.render(str(score), True, (255, 255, 255))
        dis.blit(text, (700, rect_side * (2 * maze.rows + 1)))
        try:
            mes = players_socket[0].recv(1024).decode()
            if mes == 'Victory':
                vict = True
        except:
            pass
        if vict:
            dis.fill((0, 0, 0))
            text = big_font.render("Победа соперника", True, (255, 255, 255))
            dis.blit(text, (200, 400))
            pygame.display.update()
            return current_cell
    else:
        text = small_font.render("нажмите пробел чтобы показать путь", True, (255, 255, 255))
        dis.blit(text, (500, rect_side * (2 * maze.rows + 1)))
    if defeat:
        players_socket[0].send('Victory'.encode())
    else:
        players_socket[0].send('0'.encode())
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

defeat = False
#conn = http.client.HTTPConnection("ifconfig.me")
#http.client.HTTPConnection("ifconfig.me").request("GET", "/ip")
#conn.getresponse().read()
main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind((socket.gethostbyname(socket.gethostname()), 25000))
main_socket.setblocking(False)
Interface()
