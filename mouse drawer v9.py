import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mouse Position Tracker with Drawing, Undo, and Redo")

# Font for displaying the coordinates
font = pygame.font.SysFont(None, 24)

# Create a surface for drawing
drawing_surface = pygame.Surface((WIDTH, HEIGHT))
drawing_surface.fill(WHITE)

def save_image(surface, filename):
    pygame.image.save(surface, filename)
    print(f"Image saved as {filename}")

def redraw_drawing_surface(surface, lines, grid_mode, gradient_shapes):
    surface.fill(WHITE)
    if grid_mode:
        draw_grid(surface)
    for start_pos, end_pos in lines:
        pygame.draw.line(surface, BLACK, start_pos, end_pos, 1)
    for shape in gradient_shapes:
        draw_gradient_shape(surface, shape)

def draw_grid(surface):
    for x in range(0, WIDTH, 10):  # Adjusted step size for better visibility
        pygame.draw.line(surface, GRAY, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 10):  # Adjusted step size for better visibility
        pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y), 1)

def draw_gradient_shape(surface, shape):
    shape_type, start_pos, end_pos = shape
    if shape_type == "circle":
        radius = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
        pygame.draw.circle(surface, BLACK, start_pos, radius, 1)
    elif shape_type == "ellipse":
        pygame.draw.ellipse(surface, BLACK, pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])), 1)
    elif shape_type == "parabola":
        draw_parabola(surface, start_pos, end_pos)

def draw_parabola(surface, start_pos, end_pos):
    a = (end_pos[1] - start_pos[1]) / ((end_pos[0] - start_pos[0]) ** 2)
    for x in range(start_pos[0], end_pos[0]):
        y = int(a * ((x - start_pos[0]) ** 2) + start_pos[1])
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            surface.set_at((x, y), BLACK)

def main():
    clock = pygame.time.Clock()
    running = True

    # Variables to store drawing state
    drawing = False
    gradient_mode = False
    gradient_shape_type = "circle"
    start_pos = (0, 0)
    lines = []
    undone_lines = []
    gradient_shapes = []
    undone_shapes = []
    grid_mode = False

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
                    if gradient_mode:
                        gradient_shapes.append((gradient_shape_type, start_pos, end_pos))
                        draw_gradient_shape(drawing_surface, (gradient_shape_type, start_pos, end_pos))
                    else:
                        pygame.draw.line(drawing_surface, BLACK, start_pos, end_pos, 1)
                        lines.append((start_pos, end_pos))
                    drawing = False
                    undone_lines.clear()  # Clear redo stack on new draw
                    undone_shapes.clear()  # Clear redo stack on new draw
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_image(drawing_surface, "drawing.png")
                elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if gradient_shapes or lines:
                        if gradient_shapes:
                            undone_shapes.append(gradient_shapes.pop())
                        else:
                            undone_lines.append(lines.pop())
                        redraw_drawing_surface(drawing_surface, lines, grid_mode, gradient_shapes)
                elif event.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if undone_shapes or undone_lines:
                        if undone_shapes:
                            gradient_shapes.append(undone_shapes.pop())
                        else:
                            lines.append(undone_lines.pop())
                        redraw_drawing_surface(drawing_surface, lines, grid_mode, gradient_shapes)
                elif event.key == pygame.K_SPACE:
                    grid_mode = not grid_mode
                    redraw_drawing_surface(drawing_surface, lines, grid_mode, gradient_shapes)  # Redraw with grid
                elif event.key == pygame.K_g and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    gradient_mode = not gradient_mode

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
            if gradient_mode:
                draw_gradient_shape(screen, (gradient_shape_type, start_pos, end_pos))
            else:
                pygame.draw.line(screen, BLACK, start_pos, end_pos, 1)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
