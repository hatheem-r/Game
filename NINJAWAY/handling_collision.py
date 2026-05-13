def handle_collisions(player1, player2, active_projectiles):
    rect1 = player1.get_rect()
    rect2 = player2.get_rect()

    if rect1.colliderect(rect2):
        if player1._x < player2._x:
            player1._x = player2._x - player1._width
        else:
            player1._x = player2._x + player2._width

    for proj in active_projectiles[:]:
        proj_rect = proj.get_rect()

        if proj_rect.colliderect(rect2) and proj.owner != player2:
            proj.on_hit(player2)            
            active_projectiles.remove(proj) 
            continue 
            
        if proj_rect.colliderect(rect1) and proj.owner != player1:
            proj.on_hit(player1)
            active_projectiles.remove(proj)