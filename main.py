import pygame
import sys
import time

pygame.init()

# ============================
# Classes do Solver (Adaptadas para 6x6)
# ============================

class Cell:
    '''Representa uma célula do Sudoku.'''

    def __init__(self, row, col, value, editable):
        self.row = row
        self.col = col
        self.value = value
        self._editable = editable

    @property
    def row(self): return self._row
    @row.setter
    def row(self, row):
        if row < 0 or row > 5:
            raise AttributeError('Row must be between 0 and 5.')
        self._row = row

    @property
    def col(self): return self._col
    @col.setter
    def col(self, col):
        if col < 0 or col > 5:
            raise AttributeError('Col must be between 0 and 5.')
        self._col = col

    @property
    def value(self): return self._value
    @value.setter
    def value(self, value):
        if value is not None and (value < 1 or value > 6):
            raise AttributeError('Value must be between 1 and 6.')
        self._value = value

    @property
    def editable(self): return self._editable

    def __repr__(self): return f'{self.__class__.__name__}({self.value})'


class Sudoku:
    '''Representa o jogo Sudoku 6x6.'''

    def __init__(self, board):
        self.board = []
        for row in range(6):
            self.board.append([])
            for col in range(6):
                if board[row][col] == 0:
                    val, editable = None, True
                else:
                    val, editable = board[row][col], False
                self.board[row].append(Cell(row, col, val, editable))

    def check_move(self, cell, num):
        # Valida linha
        for col in range(6):
            if self.board[cell.row][col].value == num and col != cell.col:
                return False
        # Valida coluna
        for row in range(6):
            if self.board[row][cell.col].value == num and row != cell.row:
                return False
        # Valida Bloco 2x3 (2 linhas, 3 colunas)
        box_row_start = (cell.row // 2) * 2
        box_col_start = (cell.col // 3) * 3
        for row in range(box_row_start, box_row_start + 2):
            for col in range(box_col_start, box_col_start + 3):
                if self.board[row][col].value == num and (row != cell.row or col != cell.col):
                    return False
        return True

    def get_empty_cell(self):
        for row in range(6):
            for col in range(6):
                if self.board[row][col].value is None:
                    return self.board[row][col]
        return False

    def solve(self):
        cell = self.get_empty_cell()
        if not cell: return True
        for val in range(1, 7):
            if not self.check_move(cell, val): continue
            cell.value = val
            if self.solve(): return True
            cell.value = None
        return False

    def reset(self):
        for row in self.board:
            for cell in row:
                if cell.editable:
                    cell.value = None


# ============================
# Parte gráfica (pygame adaptada para 6x6)
# ============================

cell_size = 50
minor_grid_size = 1
major_grid_size = 3
buffer = 5
button_height = 40  
button_width = 105   
button_border = 2

# Janela ligeiramente mais larga para acomodar perfeitamente os 3 botões lado a lado
width = 350 
height = cell_size*6 + minor_grid_size*4 + major_grid_size*3 + button_height + buffer*5 + button_border*2
size = width, height

white = 255, 255, 255
black = 0, 0, 0
gray = 200, 200, 200
green = 15, 15, 15
red = 200, 0, 0
inactive_btn = 15, 175, 51
active_btn = 20, 125, 45
blue_btn = 30, 144, 255
blue_btn_active = 28, 110, 200

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Mini-SudoKemistry 6x6')


class RectCell(pygame.Rect):
    def __init__(self, left, top, row, col):
        super().__init__(left, top, cell_size, cell_size)
        self.row = row
        self.col = col


def create_cells():
    '''Cria as 36 células para o tabuleiro 6x6.'''
    cells = [[] for _ in range(6)]
    row = 0
    col = 0
    left = buffer + major_grid_size
    top = buffer + major_grid_size

    while row < 6:
        while col < 6:
            cells[row].append(RectCell(left, top, row, col))

            left += cell_size + minor_grid_size
            if col != 0 and (col + 1) % 3 == 0:
                left = left + major_grid_size - minor_grid_size
            col += 1

        top += cell_size + minor_grid_size
        if row != 0 and (row + 1) % 2 == 0:
            top = top + major_grid_size - minor_grid_size
        left = buffer + major_grid_size
        col = 0
        row += 1

    return cells


def draw_grid():
    '''Desenha as linhas internas e de bloco para o Sudoku 6x6.'''
    for i in [1, 3, 5]:
        pos_y = buffer + major_grid_size + i * cell_size + ((i // 2) * major_grid_size) + ((i - (i // 2) - 1) * minor_grid_size)
        pygame.draw.line(screen, black, (buffer, pos_y), (cell_size*6 + minor_grid_size*4 + major_grid_size*3 + buffer, pos_y), minor_grid_size)
    
    for j in [1, 2, 4, 5]:
        pos_x = buffer + major_grid_size + j * cell_size + ((j // 3) * major_grid_size) + ((j - (j // 3) - 1) * minor_grid_size)
        pygame.draw.line(screen, black, (pos_x, buffer), (pos_x, cell_size*6 + minor_grid_size*4 + major_grid_size*3 + buffer), minor_grid_size)

    for i in [0, 2, 4, 6]:
        pos_y = buffer + (i // 2) * (cell_size * 2 + minor_grid_size + major_grid_size)
        if i == 6: pos_y = cell_size*6 + minor_grid_size*4 + major_grid_size*2 + buffer
        pygame.draw.line(screen, black, (buffer, pos_y), (cell_size*6 + minor_grid_size*4 + major_grid_size*3 + buffer, pos_y), major_grid_size)
        
    for j in [0, 3, 6]:
        pos_x = buffer + (j // 3) * (cell_size * 3 + minor_grid_size * 2 + major_grid_size)
        if j == 6: pos_x = cell_size*6 + minor_grid_size*4 + major_grid_size*2 + buffer
        pygame.draw.line(screen, black, (pos_x, buffer), (pos_x, cell_size*6 + minor_grid_size*4 + major_grid_size*2 + buffer), major_grid_size)


def fill_cells(cells, board):
    '''Preenche as células com a tabela periódica (Elementos 1 a 6).'''
    font_simbolo = pygame.font.Font(None, 34)
    font_atomico = pygame.font.Font(None, 18)

    tabela_periodica = {
        1: "H",
        2: "He",
        3: "Li",
        4: "Be",
        5: "B",
        6: "C"
    }

    for row in range(6):
        for col in range(6):
            val = board.board[row][col].value
            if val is None or val == 0:
                continue

            simbolo_txt = tabela_periodica.get(val, str(val))
            atomico_txt = str(val)

            if not board.board[row][col].editable:
                font_simbolo.bold = True
                cor = black
            else:
                font_simbolo.bold = False
                if board.check_move(board.board[row][col], val):
                    cor = green
                else:
                    cor = red

            txt_simbolo = font_simbolo.render(simbolo_txt, 1, cor)
            txt_atomico = font_atomico.render(atomico_txt, 1, cor)

            x_centro, y_centro = cells[row][col].center
            
            box_simbolo = txt_simbolo.get_rect(center=(x_centro + 5, y_centro + 2))
            box_atomico = txt_atomico.get_rect()
            box_atomico.right = box_simbolo.left - 2
            box_atomico.top = box_simbolo.top - 2

            screen.blit(txt_simbolo, box_simbolo)
            screen.blit(txt_atomico, box_atomico)


def draw_button(left, top, width, height, border, color, border_color, text):
    pygame.draw.rect(screen, border_color, (left, top, width+border*2, height+border*2))
    button = pygame.Rect(left+border, top+border, width, height)
    pygame.draw.rect(screen, color, button)
    font = pygame.font.Font(None, 18) 
    text = font.render(text, 1, black)
    xpos, ypos = button.center
    textbox = text.get_rect(center=(xpos, ypos))
    screen.blit(text, textbox)
    return button


def draw_board(active_cell, cells, game):
    draw_grid()
    if active_cell is not None:
        pygame.draw.rect(screen, gray, active_cell)
    fill_cells(cells, game)


def show_help_screen():
    '''Mostra uma tela sobreposta com as instruções em inglês.'''
    showing_help = True
    while showing_help:
        screen.fill((40, 40, 40))
        
        font_title = pygame.font.Font(None, 28)
        font_text = pygame.font.Font(None, 18)
        
        lines = [
            "HOW TO PLAY",
            "",
            "Instructions:",
            "Please, type ONLY the atomic number",
            "of the chemical elements from 1 to 6.",
            "",
            "Elements Reference:",
            "1: H (Hydrogen)   2: He (Helium)",
            "3: Li (Lithium)   4: Be (Beryllium)",
            "5: B (Boron)      6: C (Carbon)",
            "",
            "Press any key or click to return."
        ]
        
        y_offset = 40
        for line in lines:
            if line == "HOW TO PLAY":
                rendered = font_title.render(line, True, (255, 215, 0))
            elif ":" in line and not "Press" in line:
                rendered = font_text.render(line, True, (173, 216, 230))
            else:
                rendered = font_text.render(line, True, white)
                
            rect = rendered.get_rect(center=(width // 2, y_offset))
            screen.blit(rendered, rect)
            y_offset += 24

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP:
                showing_help = False


def visual_solve(game, cells):
    cell = game.get_empty_cell()
    if not cell:
        return True

    for val in range(1, 7): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        cell.value = val

        screen.fill(white)
        draw_board(None, cells, game)
        cell_rect = cells[cell.row][cell.col]
        pygame.draw.rect(screen, red, cell_rect, 5)
        pygame.display.update([cell_rect])
        time.sleep(0.04)

        if not game.check_move(cell, val):
            cell.value = None
            continue

        screen.fill(white)
        pygame.draw.rect(screen, green, cell_rect, 5)
        draw_board(None, cells, game)
        pygame.display.update([cell_rect])
        if visual_solve(game, cells):
            return True

        cell.value = None

    screen.fill(white)
    pygame.draw.rect(screen, white, cell_rect, 5)
    draw_board(None, cells, game)
    pygame.display.update([cell_rect])
    return False


def check_sudoku(sudoku):
    if sudoku.get_empty_cell():
        raise ValueError('Game is not complete')

    row_sets = [set() for _ in range(6)]
    col_sets = [set() for _ in range(6)]
    box_sets = [set() for _ in range(6)]

    for row in range(6):
        for col in range(6):
            box = (row // 2) * 2 + col // 3
            value = sudoku.board[row][col].value

            if value in row_sets[row] or value in col_sets[col] or value in box_sets[box]:
                return False

            row_sets[row].add(value)
            col_sets[col].add(value)
            box_sets[box].add(value)
    return True


def play():
    mini_easy = [
        [1, 0, 0, 4, 0, 0],
        [0, 0, 4, 0, 1, 0],
        [0, 4, 0, 0, 0, 3],
        [3, 0, 0, 0, 4, 0],
        [0, 1, 0, 3, 0, 0],
        [0, 0, 3, 0, 0, 1]
    ]
    
    game = Sudoku(mini_easy)
    cells = create_cells()
    active_cell = None
    
    # Define as posições fixas dos botões na parte inferior
    y_buttons = height - button_height - button_border*2 - buffer
    x_solve = buffer
    x_help = x_solve + button_width + buffer * 2
    x_reset = width - button_width - buffer - button_border*2

    # Instancia objetos fictícios iniciais para evitar o erro de NameError na primeira leitura
    solve_btn = pygame.Rect(x_solve, y_buttons, button_width, button_height)
    help_btn = pygame.Rect(x_help, y_buttons, button_width, button_height)
    reset_btn = pygame.Rect(x_reset, y_buttons, button_width, button_height)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if reset_btn.collidepoint(mouse_pos):
                    game.reset()

                if help_btn.collidepoint(mouse_pos):
                    show_help_screen()

                if solve_btn.collidepoint(mouse_pos):
                    screen.fill(white)
                    active_cell = None
                    draw_board(active_cell, cells, game)
                    pygame.display.flip()
                    visual_solve(game, cells)

                active_cell = None
                for row in cells:
                    for cell in row:
                        if cell.collidepoint(mouse_pos):
                            active_cell = cell

                if active_cell and not game.board[active_cell.row][active_cell.col].editable:
                    active_cell = None

            if event.type == pygame.KEYUP:
                if active_cell is not None:
                    if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                        game.board[active_cell.row][active_cell.col].value = None
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        game.board[active_cell.row][active_cell.col].value = 1
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        game.board[active_cell.row][active_cell.col].value = 2
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        game.board[active_cell.row][active_cell.col].value = 3
                    if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        game.board[active_cell.row][active_cell.col].value = 4
                    if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        game.board[active_cell.row][active_cell.col].value = 5
                    if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        game.board[active_cell.row][active_cell.col].value = 6
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        game.board[active_cell.row][active_cell.col].value = None

        screen.fill(white)
        draw_board(active_cell, cells, game)

        # Cores interativas (Hover)
        c_solve = active_btn if solve_btn.collidepoint(mouse_pos) else inactive_btn
        c_help = blue_btn_active if help_btn.collidepoint(mouse_pos) else blue_btn
        c_reset = active_btn if reset_btn.collidepoint(mouse_pos) else inactive_btn

        # Desenha os botões na tela atualizando suas dimensões reais de clique
        solve_btn = draw_button(x_solve, y_buttons, button_width, button_height, button_border, c_solve, black, 'Solve Please')
        help_btn = draw_button(x_help, y_buttons, button_width, button_height, button_border, c_help, black, 'Help')
        reset_btn = draw_button(x_reset, y_buttons, button_width, button_height, button_border, c_reset, black, 'Reset')

        if not game.get_empty_cell():
            if check_sudoku(game):
                font = pygame.font.Font(None, 30)
                text = font.render(' ', 1, (15, 175, 51))
                textbox = text.get_rect(center=(width//2, y_buttons - 15))
                screen.blit(text, textbox)

        pygame.display.flip()


if __name__ == '__main__':
    play()