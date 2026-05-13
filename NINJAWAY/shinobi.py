import pygame
from projectile_children import Kunai 

class Shinobi:
    # Notice we take both color AND a placeholder for animations
    def __init__(self, x, y, color, animations=None):
        self._x = x          
        self._y = y          
        self._width = 30    
        self._height = 60   
        self._color = color
        
        # Stored safely for when you activate animations later!
        self._animations = animations or {} 

        self._facing_right = True
        self._walk_speed = 3.3
        self._state = "idle"
        self._velocity_y = 0
        self._gravity = 0.5
        self._original_height = self._height
        self._ground_y = 480

        self._dodge_start_time = 0     
        self._dodge_duration = 500     

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
        if self._health < 0: self._health = 0
        print(f"Health dropped to {self._health}!")

    def cast_ultimate(self):
        pass 

    def jump(self):
        if self._state == "jumping": return
        if self._state == "dodging":
            self._height = self._original_height
            self._y = self._ground_y
        if self._state != "jumping":
            self._velocity_y = -10
            self._state = "jumping"

    def dodge(self):
        if self._y == self._ground_y and self._state != "dodging":
            self._state = "dodging"
            self._height = self._original_height // 2  
            self._y = self._ground_y + self._height    
            self._dodge_start_time = pygame.time.get_ticks()
    
    def update(self):
        self._y += self._velocity_y
        self._velocity_y += self._gravity
        target_ground_y = self._ground_y + (self._original_height - self._height)

        if self._y >= target_ground_y:
            self._y = target_ground_y     
            self._velocity_y = 0          
            if self._state == "jumping": self._state = "idle"      

        if self._state == "dodging":
            current_time = pygame.time.get_ticks()
            if current_time - self._dodge_start_time >= self._dodge_duration:
                self._height = self._original_height
                self._y = self._ground_y
                self._state = "idle"

        if self._x < 0:
            self._x = 0  
        elif self._x + self._width > 800:
            self._x = 800 - self._width  

    def _shoot(self, ProjectileClass, chakra_cost=0):
        if self._state == "dodging": return None 
        if self._chakra < chakra_cost:
            print("Not enough chakra!")
            return None

        self._chakra -= chakra_cost
        direction = 1 if self._facing_right else -1
        spawn_x = self._x + (self._width // 2)
        spawn_y = self._y + (self._height // 4)

        new_projectile = ProjectileClass(spawn_x, spawn_y, direction)
        new_projectile.owner = self  
        return new_projectile

    def throw_kunai(self):
        return self._shoot(Kunai, chakra_cost=0)

    def draw(self, surface):
        # Good old reliable rectangles!
        pygame.draw.rect(surface, self._color, (self._x, self._y, self._width, self._height))

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._width, self._height)