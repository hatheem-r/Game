import pygame # pyright: ignore[reportMissingImports]
from shinobi import Shinobi
from projectile_children import Rasenshuriken, Chidori

NARUTO_COLOR = (255, 140, 0)
SASUKE_COLOR = (0, 0, 139)

class Naruto(Shinobi):
    def __init__(self, x, y, animations=None):
        super().__init__(x, y, NARUTO_COLOR, animations)

    def cast_ultimate(self):
        return self._shoot(Rasenshuriken, chakra_cost=25)

class Sasuke(Shinobi):
    def __init__(self, x, y, animations=None):
        super().__init__(x, y, SASUKE_COLOR, animations)
        
        # --- NEW: AI Timers ---
        self._last_attack_time = pygame.time.get_ticks()
        self._attack_cooldown = 4000  # 4000 milliseconds = 4 seconds

    def decide_next_move(self, opponent, active_projectiles):
        # 1. Track the opponent (Face the correct direction)
        if opponent._x > self._x:
            self._facing_right = True
        else:
            self._facing_right = False

        # 2. Check the clock for the 4-second cooldown
        current_time = pygame.time.get_ticks()
        if current_time - self._last_attack_time >= self._attack_cooldown:
            
            self._last_attack_time = current_time # Reset the timer
            
            # Execute the attack! (This returns a Kunai object)
            return self.throw_kunai() 
        
        # Return nothing if the 4 seconds haven't passed yet
        return None 

    def cast_ultimate(self):
        return self._shoot(Chidori, chakra_cost=0)