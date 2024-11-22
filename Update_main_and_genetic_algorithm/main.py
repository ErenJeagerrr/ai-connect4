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
def draw_button(text, x, y, color, is_pressed=False):
    button_width = 300
    button_height = 60
    button_rect = pygame.Rect(x - button_width // 2, y - button_height // 2, button_width, button_height)

    # Choose color based on the status
    if is_pressed:
        pygame.draw.rect(screen, (100, 100, 100), button_rect)  # 按下时的颜色
    else:
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)  # 悬停颜色
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect)  # 默认颜色

    # Draw the button border
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, button_rect, 3)

    # Add text
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
    pressed_button = None  # To record which button has been pressed

    # Load and display the background image
    try:
        background_image = pygame.image.load("Con4.png")  # Ensure Con4.png is in the same directory
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background_image, (0, 0))
    except pygame.error as e:
        print(f"Failed to load background image: {e}")
        screen.fill(BLACK)

    # Display the title
    title_text = "Connect-4"
    title_surface = title_font.render(title_text, True, YELLOW)
    screen.blit(title_surface, (SCREEN_WIDTH / 2 - title_surface.get_width() / 2, 100))

    pygame.display.update()

    while True:
        # Clear the screen and redraw the background and title
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))
        screen.blit(title_surface, (SCREEN_WIDTH / 2 - title_surface.get_width() / 2, 100))

        # Draw buttons with pressed state handling
        human_ai_button = draw_button("Human vs AI", SCREEN_WIDTH / 2, 250, RED, pressed_button == "human_ai")
        two_player_button = draw_button("Two Human Players", SCREEN_WIDTH / 2, 350, BLUE, pressed_button == "two_player")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Detect which button is pressed
                if human_ai_button.collidepoint(event.pos):
                    pressed_button = "human_ai"
                elif two_player_button.collidepoint(event.pos):
                    pressed_button = "two_player"

            elif event.type == pygame.MOUSEBUTTONUP:
                # Trigger actions based on the pressed button when the mouse is released
                if pressed_button == "human_ai" and human_ai_button.collidepoint(event.pos):
                    ai_algorithm_menu()
                elif pressed_button == "two_player" and two_player_button.collidepoint(event.pos):
                    print("Starting Two Player...")
                    transition_screen("Loading Two Player Mode...")
                    try:
                        subprocess.run([sys.executable, "connect_4_two_player.py"])
                    except Exception as e:
                        print(f"Error: {e}")
                    pygame.quit()
                    sys.exit()
                pressed_button = None  # Reset the button state after the action

# AI algorithm menu
def ai_algorithm_menu():
    pressed_button = None  # To record which button has been pressed

    try:
        background_image = pygame.image.load("Con4.png")
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background_image, (0, 0))
    except pygame.error as e:
        print(f"Failed to load background image: {e}")
        screen.fill(BLACK)

    # Title
    title_text = "Select AI Algorithm"
    title_surface = title_font.render(title_text, True, YELLOW)
    screen.blit(title_surface, (SCREEN_WIDTH / 2 - title_surface.get_width() / 2, 100))

    pygame.display.update()

    while True:
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))
        screen.blit(title_surface, (SCREEN_WIDTH / 2 - title_surface.get_width() / 2, 100))

        # Determine which button is pressed based on pressed_button
        minimax_button = draw_button("Minimax", SCREEN_WIDTH / 2, 250, RED, pressed_button == "minimax")
        mcts_button = draw_button("MCTS", SCREEN_WIDTH / 2, 350, BLUE, pressed_button == "mcts")
        astar_button = draw_button("A* Search", SCREEN_WIDTH / 2, 450, YELLOW, pressed_button == "astar")
        genetic_button = draw_button("Genetic", SCREEN_WIDTH / 2, 550, (238, 130, 238, 255), pressed_button == "genetic")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if minimax_button.collidepoint(event.pos):
                    pressed_button = "minimax"
                elif mcts_button.collidepoint(event.pos):
                    pressed_button = "mcts"
                elif astar_button.collidepoint(event.pos):
                    pressed_button = "astar"
                elif genetic_button.collidepoint(event.pos):
                    pressed_button = "genetic"
            elif event.type == pygame.MOUSEBUTTONUP:
                if pressed_button == "minimax" and minimax_button.collidepoint(event.pos):
                    transition_screen("Loading Minimax AI...")
                    subprocess.run([sys.executable, "minimax.py"])
                    pygame.quit()
                    sys.exit()
                elif pressed_button == "mcts" and mcts_button.collidepoint(event.pos):
                    transition_screen("Loading MCTS AI...")
                    subprocess.run([sys.executable, "MCTS.py"])
                    pygame.quit()
                    sys.exit()
                elif pressed_button == "astar" and astar_button.collidepoint(event.pos):
                    transition_screen("Loading A* Search AI...")
                    subprocess.run([sys.executable, "A_star_search.py"])
                    pygame.quit()
                    sys.exit()
                elif pressed_button == "genetic" and genetic_button.collidepoint(event.pos):
                    transition_screen("Loading Genetic Algorithm AI...")
                    subprocess.run([sys.executable, "Genetic_algorithm.py"])
                    pygame.quit()
                    sys.exit()
                pressed_button = None  # Reset the button status


# Run the main menu
main_menu()
