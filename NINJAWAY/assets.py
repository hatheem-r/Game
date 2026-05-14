import pygame # pyright: ignore[reportMissingImports]

def load_assets(width, height):
    bg = pygame.image.load("assets/bg.bmp").convert()
    bg = pygame.transform.scale(bg, (width, height))
    
    floor = pygame.image.load("assets/floor.bmp").convert()
    floor = pygame.transform.scale(floor, (width, height - 515))

    # Placeholders for future animations
    naruto_anims = {} 
    sasuke_anims = {}
    
    # NEW: Placeholder for future UI elements (portraits, bar frames)
    ui_assets = {}

    # Now returning 5 items
    return bg, floor, naruto_anims, sasuke_anims, ui_assets