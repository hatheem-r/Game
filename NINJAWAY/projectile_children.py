from projectile import Projectile





class Kunai(Projectile):
    def __init__(self, x, y, direction):
        speed = 6.25 * direction 
        gray = (192, 192, 192)
        super().__init__(x, y, 20, 5, speed, gray)
        
    def on_hit(self, target):
        target.take_damage(3)





class Rasenshuriken(Projectile):
    def __init__(self, x, y, direction):
        speed = 17 * direction 
        light_blue = (135, 206, 250)
        super().__init__(x, y, 30, 30, speed, light_blue) 
        self.direction = direction
        
    def on_hit(self, target):
        target.take_damage(10)
        target._x += 3 * self.direction 





class Chidori(Projectile):
    def __init__(self, x, y, direction):
        speed = 17 * direction 
        yellow = (255, 255, 0)
        super().__init__(x, y, 30, 30, speed, yellow)
        
    def on_hit(self, target):
        target.take_damage(10)