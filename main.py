import pygame
import sys
import subprocess
import time

# 初始化 pygame
pygame.init()

# 屏幕设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY_DARK = (100, 100, 100)  # 定义深灰色
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_BORDER_COLOR = (50, 50, 50)
TITLE_BG_COLOR = (50, 50, 50)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect 4 - Game Mode Selection")

# 字体设置
title_font = pygame.font.SysFont("helvetica", 75)
button_font = pygame.font.SysFont("helvetica", 40)

# 按钮函数
def draw_button(text, x, y, color):
    # 按钮的尺寸
    button_width = 300
    button_height = 60
    button_rect = pygame.Rect(x - button_width // 2, y - button_height // 2, button_width, button_height)

    # 检测鼠标是否悬停在按钮上
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)  # 悬停颜色
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)  # 默认颜色

    # 绘制按钮边框
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, button_rect, 3)  # 边框颜色和宽度

    # 绘制文本
    button_text = button_font.render(text, True, color)
    text_rect = button_text.get_rect(center=(x, y))
    screen.blit(button_text, text_rect)

    return button_rect

# 过渡页面函数
def transition_screen(text):
    screen.fill(BLACK)

    # 显示过渡文本
    transition_font = pygame.font.SysFont("helvetica", 50)
    transition_text = transition_font.render(text, True, YELLOW)
    screen.blit(transition_text, (
        SCREEN_WIDTH / 2 - transition_text.get_width() / 2, SCREEN_HEIGHT / 2 - transition_text.get_height() / 2))

    pygame.display.update()
    time.sleep(2)  # 显示 2 秒过渡页面

# 主页面函数
def start_screen():
    # 加载背景图片并缩放
    try:
        background_image = pygame.image.load("Con4.png")  # 确保Con4.png在同一目录下
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background_image, (0, 0))
    except pygame.error as e:
        print(f"Failed to load background image: {e}")
        screen.fill(BLACK)

    # 设置标题文本和标题框
    title_text = "Connect-4"
    title_surface = title_font.render(title_text, True, YELLOW)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))

    # 绘制标题框（比文字稍大）
    title_box_padding = 20  # 让框比文字大一些
    title_box_rect = pygame.Rect(
        title_rect.x - title_box_padding / 2,
        title_rect.y - title_box_padding / 2,
        title_rect.width + title_box_padding,
        title_rect.height + title_box_padding
    )
    pygame.draw.rect(screen, TITLE_BG_COLOR, title_box_rect)  # 标题框背景颜色
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, title_box_rect, 3)  # 标题框边框

    # 绘制标题文字
    screen.blit(title_surface, title_rect)

    # 绘制按钮
    single_button_rect = draw_button("Single Player (AI)", SCREEN_WIDTH / 2, 250, RED)
    multi_button_rect = draw_button("Two Player", SCREEN_WIDTH / 2, 350, BLUE)

    pygame.display.update()

    # 等待玩家点击按钮
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 检查是否点击了单人游戏按钮
                if single_button_rect.collidepoint(event.pos):
                    print("Starting Single Player (AI)...")
                    transition_screen("Loading Single Player (AI) Mode...")
                    try:
                        subprocess.run([sys.executable, "connect_4_with_ai.py"])
                    except Exception as e:
                        print(f"Error: {e}")
                    pygame.quit()
                    sys.exit()
                # 检查是否点击了双人游戏按钮
                elif multi_button_rect.collidepoint(event.pos):
                    print("Starting Two Player...")
                    transition_screen("Loading Two Player Mode...")
                    try:
                        subprocess.run([sys.executable, "connect_4_two_player.py"])
                    except Exception as e:
                        print(f"Error: {e}")
                    pygame.quit()
                    sys.exit()

# 显示主页面
start_screen()
