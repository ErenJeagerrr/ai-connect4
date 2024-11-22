import numpy
import pygame
import sys
import math
import random

# setup of connect 4 matrix
COL_COUNT = 7
ROW_COUNT = 6
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY_PIECE = 0
WINDOW_LENGTH = 4

# players
PLAYER = 0
AI = 1

# connect 4 board set up
BLUE = (0, 0, 225)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# functions
def create_board():
    # matrix to represent board
    board = numpy.zeros((ROW_COUNT, COL_COUNT))
    return board


def drop_piece(board, row, col, piece):
    # 0 - empty space, 1 - player 1 piece, 2 - player2 piece
    board[row][col] = piece


def drop_piece_animated(board, row, col, piece):
    # 从顶部开始逐步下落到指定位置
    for r in range(ROW_COUNT + 1):
        # 绘制当前状态的棋盘
        draw_board(board)

        # 绘制当前下落位置的棋子
        pygame.draw.circle(
            screen, RED if piece == PLAYER_PIECE else YELLOW,
            (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(SQUARE_SIZE / 2 + r * SQUARE_SIZE)), RADIUS
        )

        pygame.display.update()
        pygame.time.wait(50)  # 调整动画速度

        # 如果到达目标行，停止动画
        if r == row:
            break

    # 将棋子真正放置到目标位置
    board[row][col] = piece

    # 最终将棋子放置到目标位置
    board[row][col] = piece
    draw_board(board)
    pygame.display.update()


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def increment_turn():
    global turn
    turn += 1
    turn = turn % 2

def initialize_population(pop_size, board):
    # 每个个体是一个动作序列，随机选择有效列
    population = []
    valid_locations = get_valid_locations(board)
    for _ in range(pop_size):
        individual = [random.choice(valid_locations) for _ in range(10)]  # 假设动作序列长度为10
        population.append(individual)
    return population

def fitness_function(individual, board, piece):
    temp_board = board.copy()
    score = 0
    for col in individual:
        if is_valid_location(temp_board, col):
            row = get_next_open_row(temp_board, col)
            drop_piece(temp_board, row, col, piece)
            score += score_position(temp_board, piece)
            if winning_move(temp_board, piece):
                score += 1000  # 优先赢得游戏
    return score


def change_board_orientation(board):
    print(numpy.flip(board, 0))


def winning_move(board, piece):
    # check row for 4 in a row: horizontal
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # check row for 4 in a row: vertical
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # check row for 4 in a row: negative diagonal
    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                    board[r - 3][c + 3] == piece:
                return True

    # check row for 4 in a row: positive diagonal
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and \
                    board[r+3][c+3] == piece:
                return True


def score_window(window, piece):
    score = 0

    opponent_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 1000
    elif window.count(piece) == 3 and window.count(EMPTY_PIECE) == 1:
        score += 500
    elif window.count(piece) == 2 and window.count(EMPTY_PIECE) == 2:
        score += 500

    if window.count(opponent_piece) == 3 and window.count(EMPTY_PIECE) == 1:
        score -= 5000

    return score


def draw_board(board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, ((c * SQUARE_SIZE),
                                            (r * SQUARE_SIZE) + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                draw_circle(c, r, RED)
            if board[r][c] == AI_PIECE:
                draw_circle(c, r, YELLOW)
    pygame.display.update()


def draw_circle(c, r, colour):
    pygame.draw.circle(screen, colour, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                        height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)


def score_position(board, piece):
    score = 0
    # prioritise the centre of the board
    centre_array = [int(i) for i in list(board[:, COL_COUNT // 2])]
    centre_count = centre_array.count(piece)
    score += centre_count * 10

    # check horizontal score
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COL_COUNT - 3):
            # breaking matrix up into slices of 4
            window = row_array[c:c+WINDOW_LENGTH]
            score += score_window(window, piece)

    # check vertical score
    for c in range(COL_COUNT):
        column_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            # breaking matrix up into slices of 4
            window = column_array[r:r+WINDOW_LENGTH]
            score += score_window(window, piece)

    # check positively sloped diagonal score
    for r in range(ROW_COUNT - 3):
        for c in range(COL_COUNT - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += score_window(window, piece)

    # check negatively sloped diagonal score
    for r in range(ROW_COUNT - 3):
        for c in range(COL_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += score_window(window, piece)

    return score


def get_valid_locations(board):
    valid_locations = []
    for column in range(COL_COUNT):
        if is_valid_location(board, column):
            valid_locations.append(column)
    return valid_locations


def select_parents(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    probabilities = [score / total_fitness for score in fitness_scores]
    # 使用加权随机选择两个父代
    parent1 = random.choices(population, probabilities)[0]
    parent2 = random.choices(population, probabilities)[0]
    return parent1, parent2

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def mutate(individual, mutation_rate, valid_locations):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.choice(valid_locations)
    return individual


def genetic_algorithm(board, piece, pop_size=20, generations=100, mutation_rate=0.1):
    population = initialize_population(pop_size, board)
    valid_locations = get_valid_locations(board)

    for _ in range(generations):
        fitness_scores = [fitness_function(individual, board, piece) for individual in population]
        new_population = []
        for _ in range(pop_size):
            parent1, parent2 = select_parents(population, fitness_scores)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate, valid_locations)
            new_population.append(child)
        population = new_population

    # 返回最佳个体的第一个动作
    best_individual = max(population, key=lambda ind: fitness_function(ind, board, piece))
    return best_individual[0]


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


# game status
game_over = False
turn = random.randint(0, 1)

pygame.init()

# screen set up
SQUARE_SIZE = 100
width = COL_COUNT * SQUARE_SIZE
height = (ROW_COUNT+1) * SQUARE_SIZE
RADIUS = int(SQUARE_SIZE/2 - (SQUARE_SIZE/10))

size = (width, height)

screen = pygame.display.set_mode(size)

pygame.display.set_caption('Connect 4')

# instantiations
board = create_board()
change_board_orientation(board)
draw_board(board)
pygame.display.update()

win_text = pygame.font.SysFont("helvetica", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            pos_x = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (pos_x, int(SQUARE_SIZE/2)), RADIUS)
        pygame.display.update()

        # 玩家落子
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            # 玩家落子
            if turn == PLAYER:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x / SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece_animated(board, row, col, PLAYER_PIECE)
                    if winning_move(board, PLAYER_PIECE):
                        label = win_text.render("You win!", 1, RED)
                        screen.blit(label, (width / 2 - label.get_width() / 2, 25))
                        game_over = True

                    increment_turn()

            # AI 落子
            if turn == AI and not game_over:
                col = genetic_algorithm(board, AI_PIECE)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece_animated(board, row, col, AI_PIECE)
                    if winning_move(board, AI_PIECE):
                        label = win_text.render("AI wins!", 1, YELLOW)
                        screen.blit(label, (width / 2 - label.get_width() / 2, 25))
                        game_over = True

                    change_board_orientation(board)
                    draw_board(board)
                    increment_turn()

        if game_over:
            pygame.time.wait(3000)