import pygame
import sys

from assets import load_assets
from shinobi_children import Naruto, Sasuke
from handling_collision import handle_collisions
from ui import draw_hud # NEW: Import your HUD manager

pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NINJAWAY")

# 1. Load Assets (Now unpacking 5 items!)
bg_image, floor_img, naruto_anims, sasuke_anims, ui_assets = load_assets(WIDTH, HEIGHT)

naruto = Naruto(100, 400, naruto_anims)
sasuke = Sasuke(650, 400, sasuke_anims) 
active_projectiles = []

clock = pygame.time.Clock()
running = True

# --- The Main Game Loop ---
while running:
    # --- 1. Event Listeners ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                new_kunai = naruto.throw_kunai()
                if new_kunai is not None: 
                    active_projectiles.append(new_kunai)
            elif event.key == pygame.K_x:
                ultimate = naruto.cast_ultimate()
                if ultimate is not None:
                    active_projectiles.append(ultimate)
    
    # --- 2. Keyboard Input ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: naruto.jump()
    if keys[pygame.K_DOWN]: naruto.dodge()
    if keys[pygame.K_LEFT]: naruto.move_left()
    if keys[pygame.K_RIGHT]: naruto.move_right()

    # --- 3. Update Physics ---
    naruto.update()
    sasuke.update() 
    for projectile in active_projectiles:
        projectile.update()

    handle_collisions(naruto, sasuke, active_projectiles)

    # --- 4. Render Phase ---
    screen.blit(bg_image, (0, 0))
    screen.blit(floor_img, (0, 515))

    naruto.draw(screen) 
    sasuke.draw(screen)

    for projectile in active_projectiles:
        projectile.draw(screen)

    # NEW: Draw the HUD over everything else
    draw_hud(screen, naruto, sasuke, ui_assets)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()