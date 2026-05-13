import pygame

def load_assets(width, height):
    # 1. Environment
    bg = pygame.image.load("assets/bg.bmp").convert()
    bg = pygame.transform.scale(bg, (width, height))
    
    floor = pygame.image.load("assets/floor.bmp").convert()
    floor = pygame.transform.scale(floor, (width, height - 515))

    # 2. PLACEHOLDER: Ready for your animations later!
    # Returning empty dictionaries so the rest of the game is pre-wired.
    naruto_anims = {} 
    sasuke_anims = {}

    return bg, floor, naruto_anims, sasuke_anims