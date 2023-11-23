import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("String Input Example")

# Set up fonts
font = pygame.font.Font(None, 36)
input_string = ""

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Check if the key is an alphanumeric character or space
            if event.unicode.isalnum() or event.unicode.isspace():
                input_string += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                input_string = input_string[:-1]

    # Clear the screen
    screen.fill((255, 255, 255))

    # Render the input string
    text_surface = font.render(input_string, True, (0, 0, 0))
    screen.blit(text_surface, (10, 10))

    # Update the display
    pygame.display.flip()