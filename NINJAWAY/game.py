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

        # --- NEW: State and Physics Variables ---
        self._state = "idle"
        self._velocity_y = 0
        self._gravity = 0.175
        self._original_height = self._height
        self._ground_y = 400

        self._dodge_start_time = 0     # Renamed
        self._dodge_duration = 500     # Let's make it 500ms (half a second) for a quick dodge

    # --- Action Methods ---
    def jump(self):
        # Only jump if we are not already in the air
            # 1. If we are already in the air, ignore the jump command
        if self._state == "jumping":
            return
            
        # 2. NEW: If we are dodging, instantly restore our height and ground position
        if self._state == "dodging":
            self._height = self._original_height
            self._y = self._ground_y
            
        # 3. Launch into the air and update the state
        if self._state != "jumping":
            self._velocity_y = -8.25
            self._state = "jumping"

    def dodge(self):
        # Only dodge if we are on the ground and not already dodging
        if self._y == self._ground_y and self._state != "dodging":
            self._state = "dodging"
            self._height = self._original_height // 2  
            self._y = self._ground_y + self._height    
            self._dodge_start_time = pygame.time.get_ticks()
    
    
    # --- Physics Engine ---
    def update(self):
        # 1. Apply gravity
        self._y += self._velocity_y
        self._velocity_y += self._gravity

        # 2. Dynamically calculate where the ground should be
        # If he is standing, target_ground is 400. If ducking, it becomes 450.
        target_ground_y = self._ground_y + (self._original_height - self._height)

        # 3. Floor Collision Logic
        if self._y >= target_ground_y:
            self._y = target_ground_y     # Snap to the dynamic ground level
            self._velocity_y = 0          # Stop falling
            if self._state == "jumping":
                self._state = "idle"      # Reset state when landing

        if self._state == "dodging":
            current_time = pygame.time.get_ticks()
            if current_time - self._dodge_start_time >= self._dodge_duration:
                # Restore normal height and position directly
                self._height = self._original_height
                self._y = self._ground_y
                self._state = "idle"

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
    

    # --- 2. Keyboard Input for Actions ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        naruto.jump()
    if keys[pygame.K_DOWN]:
        naruto.dodge()

    

    # --- 3. Update Physics BEFORE Drawing ---
    naruto.update()
    sasuke.update() # (Sasuke doesn't move yet, but he needs gravity applied!)

    screen.fill(BG_COLOR)
    naruto.draw(screen) # 2. Draw the characters
    sasuke.draw(screen)

    # 3. Update the display so the background actually renders
    pygame.display.flip()

# 4. Safely quit Pygame and Python when the loop ends
pygame.quit()
sys.exit()
