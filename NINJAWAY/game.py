import pygame
import sys

# --- Window Setup ---
# 1. Initialize all imported pygame modules
pygame.init()

# 2. Create the game window (800 pixels wide, 600 pixels tall)
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 3. Give the window a title
pygame.display.set_caption("NINJAWAY")

# 4. Define our RGB colors so we can use them later
BG_COLOR = (50, 100, 100)       # A dark gray for the arena background
NARUTO_COLOR = (255, 140, 0)  # Orange
SASUKE_COLOR = (0, 0, 139)    # Dark Blue

# --- The Base Class (Shinobi) ---
class Shinobi:
    def __init__(self, x, y, color):
        self._x = x          # Protected variable for X coordinate
        self._y = y          # Protected variable for Y coordinate
        self._color = color  # Protected variable for the character's color
        self._width = 50     # Hardcoded width for the rectangle
        self._height = 100   # Hardcoded height for the rectangle

    def draw(self, surface):
        # This method draws the rectangle onto the screen
        pygame.draw.rect(surface, self._color, (self._x, self._y, self._width, self._height))

class Naruto(Shinobi):
    def __init__(self, x, y):
        # Passes the x, y, and the specific orange color up to the base class
        super().__init__(x, y, NARUTO_COLOR)

class Sasuke(Shinobi):
    def __init__(self, x, y):
        # Passes the x, y, and the specific dark blue color up to the base class
        super().__init__(x, y, SASUKE_COLOR)




















# 1. Instantiate our characters before the loop starts
naruto = Naruto(100, 400)  # Spawns Naruto on the left
sasuke = Sasuke(650, 400)  # Spawns Sasuke on the right

# --- The Main Game Loop ---
running = True

while running:

    # 1. Listen for events (like clicking the 'X' to close the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    # 2. Fill the screen with our background color to clear the frame
    screen.fill(BG_COLOR)

    # 2. Draw the characters
    naruto.draw(screen)
    sasuke.draw(screen)

    # 3. Update the display so the background actually renders
    pygame.display.flip()

# 4. Safely quit Pygame and Python when the loop ends
pygame.quit()
sys.exit()
