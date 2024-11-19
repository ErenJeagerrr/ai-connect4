import numpy as np
import random
import math
import pygame

from connect_4_with_ai import (
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
turn =  AI_PIECE # 或 PLAYER，初始设置

# Board setup
board = np.zeros((ROW_COUNT, COL_COUNT))  # 空棋盘
game_over = False  # 游戏结束标志

# Pygame screen setup
pygame.init()
SQUARE_SIZE = 100
width = COL_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4 with MCTS AI")
win_text = pygame.font.SysFont("helvetica", 75)




# players
PLAYER = 0
AI = 1

# connect 4 board set up
BLUE = (0, 0, 225)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class Node:
    def __init__(self, state, parent=None):
        self.state = state  # 当前棋盘状态
        self.parent = parent  # 父节点
        self.children = []  # 子节点列表
        self.visits = 0  # 节点访问次数
        self.value = 0  # 节点的累积奖励值

    def is_fully_expanded(self):
        # 如果当前节点的所有子节点都已展开，则为 True
        return len(self.children) == len(get_valid_locations(self.state))

    def best_child(self, exploration_weight=1.0):
        # 使用UCT公式选择最佳子节点
        best_score = -float('inf')
        best_child = None
        for child in self.children:
            uct_score = (
                child.value / child.visits +
                exploration_weight * math.sqrt(math.log(self.visits) / child.visits)
            )
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child


def simulate_random_game(board, piece):
    """
    模拟一个随机游戏，从当前棋盘状态随机落子直到游戏结束。
    """
    current_piece = piece
    while not is_terminal_node(board):
        valid_locations = get_valid_locations(board)
        column = random.choice(valid_locations)
        row = get_next_open_row(board, column)
        drop_piece(board, row, column, current_piece)
        current_piece = PLAYER_PIECE if current_piece == AI_PIECE else AI_PIECE

    # 游戏结束，返回模拟的奖励值
    if winning_move(board, AI_PIECE):
        return 1  # AI 胜利
    elif winning_move(board, PLAYER_PIECE):
        return -1  # 玩家胜利
    else:
        return 0  # 平局


def backpropagate(node, reward):
    """
    反向传播阶段：从当前节点更新所有祖先节点的访问次数和奖励值。
    """
    while node is not None:
        node.visits += 1
        node.value += reward
        reward = -reward  # 奖励值在不同回合之间切换
        node = node.parent


def expand_node(node, piece):
    """
    扩展当前节点，生成一个新的子节点。
    """
    untried_locations = [
        col for col in get_valid_locations(node.state)
        if col not in [child.state for child in node.children]
    ]
    if len(untried_locations) > 0:
        column = random.choice(untried_locations)
        row = get_next_open_row(node.state, column)
        new_state = node.state.copy()
        drop_piece(new_state, row, column, piece)
        child_node = Node(new_state, node)
        node.children.append(child_node)
        return child_node
    return None
def mcts(board, piece, iterations=1000):
    """
    主MCTS函数，使用蒙特卡罗树搜索选择最佳下一步落子位置。
    """
    root = Node(board)

    for _ in range(iterations):
        node = root

        # 选择阶段：通过UCT选择一个未完全展开的节点
        while not is_terminal_node(node.state) and node.is_fully_expanded():
            node = node.best_child()

        # 扩展阶段：扩展一个子节点
        if not is_terminal_node(node.state):
            node = expand_node(node, piece)

        # 模拟阶段：从扩展的新节点开始模拟游戏
        reward = simulate_random_game(node.state.copy(), piece)

        # 回传阶段：更新当前路径的节点信息
        backpropagate(node, reward)

    # 从根节点的子节点中选择访问次数最多的节点
    best_move = root.best_child(exploration_weight=0).state
    for col in range(COL_COUNT):
        if not np.array_equal(best_move, board):
            return col
    return random.choice(get_valid_locations(board))  # 回退到随机选择


def is_terminal_node(board):
    """
    判断当前棋盘状态是否为终止节点。
    """
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def get_valid_locations(board):
    """
    获取所有有效落子位置（可放置棋子的列）。
    """
    valid_locations = []
    for column in range(COL_COUNT):
        if is_valid_location(board, column):
            valid_locations.append(column)
    return valid_locations


def get_next_open_row(board, col):
    """
    获取指定列的下一个空行索引。
    """
    for row in range(ROW_COUNT):
        if board[row][col] == EMPTY_PIECE:
            return row


def drop_piece(board, row, col, piece):
    """
    在棋盘中指定位置放置棋子。
    """
    board[row][col] = piece


# 替换AI落子逻辑
if turn == AI and not game_over:
    col = mcts(board, AI_PIECE, iterations=500)  # 调整迭代次数以控制AI计算强度

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
