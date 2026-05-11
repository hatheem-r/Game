import pygame
import os

def load_assets(width, height):
    # 1. Load Background & Floor (as we did before)
    bg = pygame.image.load("assets/bg.bmp").convert()
    bg = pygame.transform.scale(bg, (width, height))
    
    floor = pygame.image.load("assets/floor.bmp").convert()
    floor = pygame.transform.scale(floor, (width, height - 510))

    # 2. Automated Naruto Idle Loader
    idle_frames = []
    folder_path = "assets/naruto/idle"
    
    # We loop from 0 to 24 to get all 25 frames
    for i in range(1, 26):
        file_path = f"{folder_path}/tile{i:03d}.png"
        img = pygame.image.load(file_path).convert_alpha()
        # Scale each frame to your 30x60 hitbox
        img = pygame.transform.scale(img, (30, 60))
        idle_frames.append(img)

    naruto_animations = {
        "idle": idle_frames
    }

    return bg, floor, naruto_animations