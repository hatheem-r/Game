import pygame # pyright: ignore[reportMissingImports]

def draw_hud(surface, player1, player2, ui_assets=None):

    font = pygame.font.SysFont(None, 32)
    name1_text = font.render(player1.name, True, (50,255,50))
    surface.blit(name1_text, (50, 75))
    name2_text = font.render(player2.name, True, (50,255,50))
    surface.blit(name2_text, (680, 75))

    # Fallback to empty dictionary if no images are loaded yet
    ui_assets = ui_assets or {}

    # --- Player 1 (Naruto) UI (Top Left) ---
    
    # 1. Health Bar (Max Width: 200)
    # Background (Red)
    pygame.draw.rect(surface, (255, 0, 0), (50, 30, 200, 20))  
    
    # Fill (Green)
    p1_health_width = (player1._health / 100) * 200
    if p1_health_width > 0:
        pygame.draw.rect(surface, (0, 255, 0), (50, 30, p1_health_width, 20))
        
    # Border (Dark Gray)
    pygame.draw.rect(surface, (50, 50, 50), (50, 30, 200, 20), 3) 
    
    # 2. Chakra Bar (Max Width: 150)
    # Background (Black)
    pygame.draw.rect(surface, (0, 0, 0), (50, 60, 150, 10))
    
    # Fill (Blue)
    p1_chakra_width = (player1._chakra / 100) * 150
    if p1_chakra_width > 0:
        pygame.draw.rect(surface, (0, 191, 0), (50, 60, p1_chakra_width, 10))


    # --- Player 2 (Sasuke) UI (Top Right) ---
    
    # 1. Health Bar (Max Width: 200)
    # Background (Red)
    pygame.draw.rect(surface, (255, 0, 0), (550, 30, 200, 20))
    
    # Fill (Green) - Drains from left to right for Player 2!
    p2_health_width = (player2._health / 100) * 200
    if p2_health_width > 0:
        fill_x_position = 550 + (200 - p2_health_width)
        pygame.draw.rect(surface, (0, 255, 0), (fill_x_position, 30, p2_health_width, 20))
        
    # Border (Dark Gray)
    pygame.draw.rect(surface, (50, 50, 50), (550, 30, 200, 20), 3)