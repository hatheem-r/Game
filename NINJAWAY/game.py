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





class Projectile:
    def __init__(self, x, y, width, height, speed, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color

    def update(self):
        # Move horizontally across the screen
        self.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))






class Kunai(Projectile):
    def __init__(self, x, y, direction):
        # direction is 1 (right) or -1 (left)
        speed = 1 * direction 
        gray = (192, 192, 192)
        # width: 20, height: 5
        super().__init__(x, y, 20, 5, speed, gray)












# --- The Base Class (Shinobi) ---
class Shinobi:
    def __init__(self, x, y, color):
        self._x = x          # Protected variable for X coordinate
        self._y = y          # Protected variable for Y coordinate
        self._color = color  # Protected variable for the character's color
        self._width = 30    # Hardcoded width for the rectangle 50
        self._height = 60   # Hardcoded height for the rectangle 100

        self._facing_right = True
        self._walk_speed = 0.38

        # --- NEW: State and Physics Variables ---
        self._state = "idle"
        self._velocity_y = 0
        self._gravity = 0.045
        self._original_height = self._height
        self._ground_y = 450

        self._dodge_start_time = 0     # Renamed
        self._dodge_duration = 500     # Let's make it 500ms (half a second) for a quick dodge

        self._health = 100
        self._chakra = 100


    
    def move_left(self):
        self._x -= self._walk_speed
        self._facing_right = False

    def move_right(self):
        self._x += self._walk_speed
        self._facing_right = True

    def take_damage(self, amount):
        self._health -= amount
        if self._health < 0:
            self._health = 0
        print(f"Health dropped to {self._health}!") # For testing

    # The base polymorphic method
    def cast_ultimate(self):
        pass # Will be overridden by subclasses

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
            self._velocity_y = -4.15
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

            # 5. Arena Border Collision
        if self._x < 0:
            self._x = 0  # Hit left wall
        elif self._x + self._width > 800:
            self._x = 800 - self._width  # Hit right wall



    def throw_kunai(self):
        # NEW: Refuse to throw if currently dodging
        if self._state == "dodging":
            return None 

        direction = 1 if self._facing_right else -1
        spawn_x = self._x + (self._width // 2)
        spawn_y = self._y + (self._height // 3)
        return Kunai(spawn_x, spawn_y, direction)
    






    
        



    def draw(self, surface):
        # This method draws the rectangle onto the screen
        pygame.draw.rect(surface, self._color, (self._x, self._y, self._width, self._height))


    def get_rect(self):
        # Creates a mathematical bounding box for collision detection
        return pygame.Rect(self._x, self._y, self._width, self._height)

    







class Naruto(Shinobi):
    def __init__(self, x, y):
        super().__init__(x, y, NARUTO_COLOR)

    def cast_ultimate(self):
        # Override to throw Rasenshuriken
        if self._chakra >= 50 and self._state != "dodging":
            self._chakra -= 50
            direction = 1 if self._facing_right else -1
            spawn_x = self._x + (self._width // 2)
            spawn_y = self._y + (self._height // 4)
            return Rasenshuriken(spawn_x, spawn_y, direction)
        return None

class Sasuke(Shinobi):
    def __init__(self, x, y):
        super().__init__(x, y, SASUKE_COLOR)

    def cast_ultimate(self):
        # Override to throw Chidori (no chakra check needed for NPC yet)
        direction = 1 if self._facing_right else -1
        spawn_x = self._x + (self._width // 2)
        spawn_y = self._y + (self._height // 4)
        return Chidori(spawn_x, spawn_y, direction)






































# --- The Collision Manager ---
def handle_collisions(player1, player2, active_projectiles):
    # --- 1. Character vs. Character Collision ---
    rect1 = player1.get_rect()
    rect2 = player2.get_rect()

    if rect1.colliderect(rect2):
        # If Player 1 is on the left, push them smoothly against Player 2's left side
        if player1._x < player2._x:
            player1._x = player2._x - player1._width
        # If Player 1 is on the right, push them against Player 2's right side
        else:
            player1._x = player2._x + player2._width
            
    # --- 2. Projectile Collisions (Coming Next!) ---
    # We will add the Kunai hit detection right here in the next step.



# 1. Instantiate our characters before the loop starts
naruto = Naruto(100, 400)  # Spawns Naruto on the left
sasuke = Sasuke(650, 400)  # Spawns Sasuke on the right


# NEW: A list to keep track of all active weapons on screen
active_projectiles = []


clock = pygame.time.Clock()
# --- The Main Game Loop ---
running = True

while running:

    # 1. Listen for events (like clicking the 'X' to close the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # NEW: Listen for a single Spacebar tap to throw
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                new_kunai = naruto.throw_kunai()
                # NEW: Only add to the list if a kunai was actually created
                if new_kunai is not None: 
                    active_projectiles.append(new_kunai)
    

    # --- 2. Keyboard Input for Actions ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        naruto.jump()
    if keys[pygame.K_DOWN]:
        naruto.dodge()
    # NEW: Left and Right movement
    if keys[pygame.K_LEFT]:
        naruto.move_left()
    if keys[pygame.K_RIGHT]:
        naruto.move_right()

    

    # --- 3. Update Physics BEFORE Drawing ---
    naruto.update()
    sasuke.update() # (Sasuke doesn't move yet, but he needs gravity applied!)

    for projectile in active_projectiles:
        projectile.update()




    handle_collisions(naruto, sasuke, active_projectiles)


   

    screen.fill(BG_COLOR)
    naruto.draw(screen) # 2. Draw the characters
    sasuke.draw(screen)

    for projectile in active_projectiles:
        projectile.draw(screen)

    # 3. Update the display so the background actually renders
    pygame.display.flip()

# 4. Safely quit Pygame and Python when the loop ends
pygame.quit()
sys.exit()
