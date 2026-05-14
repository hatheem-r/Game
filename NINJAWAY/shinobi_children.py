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
        # We can add AI-specific variables here later 
        # (like an "aggression" level or a "reaction timer")

    # --- NEW: The AI Abstraction ---
    def decide_next_move(self, opponent, active_projectiles):
        """
        AI Decision Engine (Stubbed).
        Input: 
          - opponent: Allows Sasuke to read Naruto's _x, _y, and _state.
          - active_projectiles: Allows Sasuke to see incoming attacks to dodge.
        """
        # For now, we do absolutely nothing.
        pass

    def cast_ultimate(self):
        return self._shoot(Chidori, chakra_cost=0)