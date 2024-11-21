import pygame
import sys
import subprocess
import time

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_BORDER_COLOR = (50, 50, 50)
TITLE_BG_COLOR = (50, 50, 50)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect 4 - Game Mode Selection")

# Font settings
title_font = pygame.font.SysFont("helvetica", 75)
button_font = pygame.font.SysFont("helvetica", 40)

# Helper function to draw buttons
def draw_button(text, x, y, color):
    button_width = 300
    button_height = 60
    button_rect = pygame.Rect(x - button_width // 2, y - button_height // 2, button_width, button_height)

    # Check if mouse is hovering
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)  # Hover color
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)  # Default color

    # Draw button border
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, button_rect, 3)

    # Draw text
    button_text = button_font.render(text, True, color)
    text_rect = button_text.get_rect(center=(x, y))
    screen.blit(button_text, text_rect)

    return button_rect

# Transition screen
def transition_screen(text):
    screen.fill(BLACK)

    # Display transition text
    transition_font = pygame.font.SysFont("helvetica", 50)
    transition_text = transition_font.render(text, True, YELLOW)
    screen.blit(transition_text, (
        SCREEN_WIDTH / 2 - transition_text.get_width() / 2, SCREEN_HEIGHT / 2 - transition_text.get_height() / 2))

    pygame.display.update()
    time.sleep(2)

# Main menu
def main_menu():
    screen.fill(BLACK)

    # Display title
    title_text = "Connect-4"
    title_surface = title_font.render(title_text, True, YELLOW)
    screen.blit(title_surface, (SCREEN_WIDTH / 2 - title_surface.get_width() / 2, 100))

    # Draw buttons
    human_ai_button = draw_button("Human vs AI", SCREEN_WIDTH / 2, 250, RED)
    two_player_button = draw_button("Two Human Players", SCREEN_WIDTH / 2, 350, BLUE)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if human_ai_button.collidepoint(event.pos):
                    ai_algorithm_menu()
                elif two_player_button.collidepoint(event.pos):
                    print("Starting Two Player...")
                    transition_screen("Loading Two Player Mode...")
                    try:
                        subprocess.run([sys.executable, "connect_4_two_player.py"])
                    except Exception as e:
                        print(f"Error: {e}")
                    pygame.quit()
                    sys.exit()

# AI algorithm menu
def ai_algorithm_menu():
    screen.fill(BLACK)

    # Display title
    title_text = "Select AI Algorithm"
    title_surface = title_font.render(title_text, True, YELLOW)
    screen.blit(title_surface, (SCREEN_WIDTH / 2 - title_surface.get_width() / 2, 100))

    # Draw buttons
    minimax_button = draw_button("Minimax", SCREEN_WIDTH / 2, 250, RED)
    mcts_button = draw_button("MCTS", SCREEN_WIDTH / 2, 350, BLUE)
    astar_button = draw_button("A* Search", SCREEN_WIDTH / 2, 450, YELLOW)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if minimax_button.collidepoint(event.pos):
                    print("Starting Minimax AI...")
                    transition_screen("Loading Minimax AI...")
                    try:
                        subprocess.run([sys.executable, "minimax.py"])
                    except Exception as e:
                        print(f"Error: {e}")
                    pygame.quit()
                    sys.exit()
                elif mcts_button.collidepoint(event.pos):
                    print("Starting MCTS AI...")
                    transition_screen("Loading MCTS AI...")
                    try:
                        subprocess.run([sys.executable, "MCTS.py"])
                    except Exception as e:
                        print(f"Error: {e}")
                    pygame.quit()
                    sys.exit()
                elif astar_button.collidepoint(event.pos):
                    print("Starting A_star_search AI...")
                    transition_screen("Loading A_star_search AI...")
                    try:
                        subprocess.run([sys.executable, "A_star_search.py"])
                    except Exception as e:
                        print(f"Error: {e}")
                    pygame.quit()
                    sys.exit()

# Run the main menu
main_menu()
