import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mouse Position Tracker with Axes")

# Font for displaying the coordinates
font = pygame.font.SysFont(None, 24)

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Clear the screen
        screen.fill(WHITE)

        # Render the mouse coordinates
        coord_text = f"X: {mouse_x}, Y: {mouse_y}"
        text = font.render(coord_text, True, BLACK)

        # Draw the text on the top right of the screen
        screen.blit(text, (WIDTH - text.get_width() - 10, 10))

        # Draw the dynamic x and y axis lines
        pygame.draw.line(screen, RED, (0, mouse_y), (WIDTH, mouse_y), 1)  # Horizontal line
        pygame.draw.line(screen, RED, (mouse_x, 0), (mouse_x, HEIGHT), 1)  # Vertical line

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
