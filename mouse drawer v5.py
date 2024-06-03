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
pygame.display.set_caption("Mouse Position Tracker with Drawing")

# Font for displaying the coordinates
font = pygame.font.SysFont(None, 24)

# Create a surface for drawing
drawing_surface = pygame.Surface((WIDTH, HEIGHT))
drawing_surface.fill(WHITE)

def save_image(surface, filename):
    pygame.image.save(surface, filename)
    print(f"Image saved as {filename}")

def main():
    clock = pygame.time.Clock()
    running = True

    # Variables to store drawing state
    drawing = False
    start_pos = (0, 0)
    lines = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                start_pos = pygame.mouse.get_pos()
                drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    end_pos = pygame.mouse.get_pos()
                    pygame.draw.line(drawing_surface, BLACK, start_pos, end_pos, 1)
                    lines.append((start_pos, end_pos))
                    drawing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_image(drawing_surface, "drawing.png")

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Clear the screen
        screen.fill(WHITE)

        # Copy the drawing surface to the screen
        screen.blit(drawing_surface, (0, 0))

        # Render the mouse coordinates
        coord_text = f"X: {mouse_x}, Y: {mouse_y}"
        text = font.render(coord_text, True, BLACK)

        # Draw the text on the top right of the screen
        screen.blit(text, (WIDTH - text.get_width() - 10, 10))

        # Draw the dynamic x and y axis lines
        pygame.draw.line(screen, RED, (0, mouse_y), (WIDTH, mouse_y), 1)  # Horizontal line
        pygame.draw.line(screen, RED, (mouse_x, 0), (mouse_x, HEIGHT), 1)  # Vertical line

        # Draw the current line if drawing
        if drawing:
            end_pos = pygame.mouse.get_pos()
            pygame.draw.line(screen, BLACK, start_pos, end_pos, 1)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
