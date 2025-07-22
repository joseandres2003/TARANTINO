# ¡instalar pygame primero!
#---------------------------------------------------
import pygame
import sys

pygame.init()

# Configuracion general
WINDOW_SIZE = 300
GRID_SIZE = 100
LINE_WIDTH = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (0, 0, 0)
BOX_COLOR = (200, 200, 200)
BOX_BORDER = (50, 50, 50)
BUTTON_COLOR = (100, 200, 100)
BUTTON_HOVER = (80, 180, 80)
EXIT_BUTTON_COLOR = (255, 100, 100)
EXIT_HOVER = (230, 80, 80)
FONT = pygame.font.SysFont(None, 32)

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Tres en Raya')

# Crear tablero
def crear_tablero():
    return [[' ' for _ in range(3)] for _ in range(3)]

game_board = crear_tablero()
current_player = 'X'

# Comprobar ganador
def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Comprobar empate
def tablero_lleno(board):
    return all(cell != ' ' for row in board for cell in row)

# Dibujar lineas del tablero
def draw_lines():
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * GRID_SIZE, 0), (i * GRID_SIZE, WINDOW_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, i * GRID_SIZE), (WINDOW_SIZE, i * GRID_SIZE), LINE_WIDTH)

# Dibujar X
def draw_x(row, col):
    offset = GRID_SIZE // 4
    pygame.draw.line(screen, LINE_COLOR, (col * GRID_SIZE + offset, row * GRID_SIZE + offset),
                     ((col + 1) * GRID_SIZE - offset, (row + 1) * GRID_SIZE - offset), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, ((col + 1) * GRID_SIZE - offset, row * GRID_SIZE + offset),
                     (col * GRID_SIZE + offset, (row + 1) * GRID_SIZE - offset), LINE_WIDTH)

# Dibujar O
def draw_o(row, col):
    offset = GRID_SIZE // 4
    pygame.draw.circle(screen, LINE_COLOR, (col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2),
                       GRID_SIZE // 2 - offset, LINE_WIDTH)

# Mostrar mensaje con botones de reinicio y salir
def mostrar_mensaje_con_botones(texto):
    box_width, box_height = 280, 140
    box_x = (WINDOW_SIZE - box_width) // 2
    box_y = (WINDOW_SIZE - box_height) // 2

    reiniciar_btn = pygame.Rect(box_x + 20, box_y + 80, 100, 40)
    salir_btn = pygame.Rect(box_x + 160, box_y + 80, 100, 40)

    while True:
        # Dibuja la caja del mensaje
        pygame.draw.rect(screen, BOX_COLOR, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, BOX_BORDER, (box_x, box_y, box_width, box_height), 3)

        # Texto principal
        texto_render = FONT.render(texto, True, BLACK)
        texto_rect = texto_render.get_rect(center=(WINDOW_SIZE // 2, box_y + 35))
        screen.blit(texto_render, texto_rect)

        # Detectar mouse
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        # Botón Reiniciar
        if reiniciar_btn.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER, reiniciar_btn)
            if click:
                pygame.time.wait(200)
                return "reiniciar"
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, reiniciar_btn)

        reiniciar_text = FONT.render("Reiniciar", True, BLACK)
        screen.blit(reiniciar_text, reiniciar_text.get_rect(center=reiniciar_btn.center))

        # Botón Salir
        if salir_btn.collidepoint(mouse_pos):
            pygame.draw.rect(screen, EXIT_HOVER, salir_btn)
            if click:
                pygame.time.wait(200)
                return "salir"
        else:
            pygame.draw.rect(screen, EXIT_BUTTON_COLOR, salir_btn)

        salir_text = FONT.render("Salir", True, BLACK)
        screen.blit(salir_text, salir_text.get_rect(center=salir_btn.center))

        pygame.display.flip()

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Bucle principal
def jugar():
    global game_board, current_player
    game_board = crear_tablero()
    current_player = 'X'
    game_over = False
    running = True

    while running:
        screen.fill(WHITE)
        draw_lines()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // GRID_SIZE, x // GRID_SIZE

                if game_board[row][col] == ' ':
                    game_board[row][col] = current_player

                    if check_win(game_board, current_player):
                        game_over = True
                        pygame.time.wait(300)
                        resultado = mostrar_mensaje_con_botones(f"¡Jugador {current_player} gana!")
                        if resultado == "reiniciar":
                            jugar()
                        else:
                            pygame.quit()
                            sys.exit()
                    elif tablero_lleno(game_board):
                        game_over = True
                        pygame.time.wait(300)
                        resultado = mostrar_mensaje_con_botones("¡Empate!")
                        if resultado == "reiniciar":
                            jugar()
                        else:
                            pygame.quit()
                            sys.exit()
                    else:
                        current_player = 'O' if current_player == 'X' else 'X'

        for row in range(3):
            for col in range(3):
                if game_board[row][col] == 'X':
                    draw_x(row, col)
                elif game_board[row][col] == 'O':
                    draw_o(row, col)

        pygame.display.flip()
jugar()