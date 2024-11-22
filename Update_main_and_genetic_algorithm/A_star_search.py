import numpy as np
import pygame
from minimax import (
    EMPTY_PIECE,
    ROW_COUNT,
    COL_COUNT,
    is_valid_location,
    get_next_open_row,
    drop_piece_animated,
    winning_move,
    PLAYER_PIECE,
    AI_PIECE,
    draw_board,
    change_board_orientation,
    increment_turn,
    drop_piece
)

# Initialize game variables
turn = AI_PIECE  # Set the initial turn to AI or PLAYER.
board = np.zeros((ROW_COUNT, COL_COUNT))  # Initialize an empty board.
game_over = False

# Pygame setup
pygame.init()
SQUARE_SIZE = 100
width = COL_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4 with AI using A* Search")
win_text = pygame.font.SysFont("helvetica", 75)

# Colors for rendering
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

def heuristic(board, piece):
    """
    Heuristic function to evaluate board state.
    The score is based on potential winning opportunities.
    """
    score = 0

    # Score center column for positional advantage
    center_array = [int(board[row][COL_COUNT // 2]) for row in range(ROW_COUNT)]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Check horizontal, vertical, and diagonal alignments
    for row in range(ROW_COUNT):
        for col in range(COL_COUNT - 3):
            window = list(board[row, col:col + 4])
            score += evaluate_window(window, piece)

    for col in range(COL_COUNT):
        for row in range(ROW_COUNT - 3):
            window = [board[row + i][col] for i in range(4)]
            score += evaluate_window(window, piece)

    for row in range(ROW_COUNT - 3):
        for col in range(COL_COUNT - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window, piece)

        for col in range(COL_COUNT - 3):
            window = [board[row + i][col + 3 - i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def evaluate_window(window, piece):
    """
    Evaluate a 4-cell window to calculate its score.
    """
    score = 0
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:  # AI has 4 pieces in a row (direct win)
        score += 1000  # High score, prioritize completing four-in-a-row for victory
    elif window.count(piece) == 3 and window.count(EMPTY_PIECE) == 1:  # AI has 3 pieces in a row, 1 empty spot
        score += 50  # High score, close to winning, AI should aim to complete four-in-a-row
    elif window.count(piece) == 2 and window.count(EMPTY_PIECE) == 2:  # AI has 2 pieces in a row, 2 empty spots
        score += 10  # Medium score, potential favorable position, AI should occupy it

    if window.count(opponent_piece) == 3 and window.count(
            EMPTY_PIECE) == 1:  # Opponent has 3 pieces in a row, 1 empty spot
        score -= 100  # High negative score, AI should prioritize blocking opponent's win
    elif window.count(opponent_piece) == 2 and window.count(
            EMPTY_PIECE) == 2:  # Opponent has 2 pieces in a row, 2 empty spots
        score -= 10  # Medium negative score, opponent's potential threat, AI should defend

    return score

def get_valid_locations(board):
    """
    Returns all valid columns where a piece can be dropped.
    """
    valid_locations = []
    for column in range(COL_COUNT):
        if is_valid_location(board, column):
            valid_locations.append(column)
    return valid_locations

def get_next_open_row(board, col):
    """
    Finds the next available row in the specified column.
    """
    for row in range(ROW_COUNT):
        if board[row][col] == EMPTY_PIECE:
            return row

def a_star_search(board, piece):
    """
    A* search algorithm to find the best move.
    """
    valid_locations = get_valid_locations(board)
    best_score = -float('inf')
    best_col = random.choice(valid_locations)  # Default to random valid move

    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = heuristic(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

# Main AI logic
if turn == AI_PIECE and not game_over:
    col = a_star_search(board, AI_PIECE)  # Use A* search to decide the column

    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece_animated(board, row, col, AI_PIECE)  # Animated piece drop

        if winning_move(board, AI_PIECE):
            label = win_text.render("AI wins!", 1, YELLOW)
            screen.blit(label, (width / 2 - label.get_width() / 2, 25))
            game_over = True

        change_board_orientation(board)
        draw_board(board)

        increment_turn()
