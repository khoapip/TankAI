from Tank import *
from Wall import *
from TankGroup import *
from constants import *

#initializing variables
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("TANKS")

pressedLeft = False
pressedDown = False
pressedRight = False
pressedUp = False
gameExit = False

#groups
allSprite = pygame.sprite.LayeredUpdates()  # to update a portion of a map per frame
bulletSprites = pygame.sprite.Group()
tankSprites = TankGroup(initial_board, bulletSprites, allSprite)  #enemy tank only
wallGroup = pygame.sprite.Group()
unbreakableWallGroup = pygame.sprite.Group()

for r in range(len(initial_board)):
    for c in range(len(initial_board[r])):
        if initial_board[r][c] == 1:
            wall = Wall(initial_board[r][c], r, c, wall1_img)
            gameDisplay.blit(wall.image, (c* BLOCK_SIZE, r * BLOCK_SIZE))
            unbreakableWallGroup.add(wall)
        elif initial_board[r][c] == 2:
            wall = Wall(initial_board[r][c], r, c, wall2_img)
            wallGroup.add(wall)
            allSprite.add(wall)
        elif initial_board[r][c] == 0:
            gameDisplay.blit(road_img, (c * BLOCK_SIZE, r * BLOCK_SIZE))

pygame.display.update()
background = gameDisplay.copy()

playerTank = Tank(50, 150, "R",playerHealth)
allSprite.add(playerTank)

enemy_tank1 = TankAI(900, 50, "l", "M",enemyHealth)
#testmap = tankSprites.generateCurrentMap(wallGroup, playerTank)
#enemy_tank1.findShortestPath((1, 3), testmap)
#Helper.print_best_move_map(enemy_tank1.shortest_path_tree, testmap)
tankSprites.add(enemy_tank1)
allSprite.add(enemy_tank1)

enemy_tank3 = TankAI(900, 350, "u", "M",enemyHealth) #enemy tank in class Tank.py
tankSprites.add(enemy_tank3)
allSprite.add(enemy_tank3)


while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pressedLeft = True
            elif event.key == pygame.K_RIGHT:
                pressedRight = True
            elif event.key == pygame.K_UP:
                pressedUp = True
            elif event.key == pygame.K_DOWN:
                pressedDown = True
            if event.key == pygame.K_SPACE:
                bullet = playerTank.shoot()
                if bullet:
                    bulletSprites.add(bullet)
                    allSprite.add(bullet)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                pressedLeft = False
            elif event.key == pygame.K_RIGHT:
                pressedRight = False
            elif event.key == pygame.K_UP:
                pressedUp = False
            elif event.key == pygame.K_DOWN:
                pressedDown = False
    if pressedLeft:
        playerTank.vx = 0
        playerTank.vy = 0
        if (pygame.sprite.spritecollide(playerTank, wallGroup, dokill=False) or pygame.sprite.spritecollide(playerTank,
                                                                                                            unbreakableWallGroup,
                                                                                                            dokill=False)):
            if int(playerTank.rect.y) % BLOCK_SIZE > 45 or int(playerTank.rect.y) % BLOCK_SIZE < 5:
                wallPosx = int((playerTank.rect.y + 5) / BLOCK_SIZE)
                wallPosy = int(playerTank.rect.x / BLOCK_SIZE)
                if wallPosy < 0:
                    wallPosy = 0
                if initial_board[wallPosx][wallPosy] == 0:
                    playerTank.changeVLeft()
            else:
                wallPosx = int(playerTank.rect.y / BLOCK_SIZE)
                wallPosy = int(playerTank.rect.x / BLOCK_SIZE)
                if wallPosy < 0:
                    wallPosy = 0
                wallPosx2 = int(playerTank.rect.y / BLOCK_SIZE) + 1
                if wallPosx2 > 13:
                    wallPosx2 = 13
                if initial_board[wallPosx][wallPosy] == 0 and initial_board[wallPosx2][wallPosy] == 0:
                    playerTank.changeVLeft()
        else:
            playerTank.changeVLeft()
        playerTank.move()
    elif pressedUp:
        playerTank.vx = 0
        playerTank.vy = 0
        if (pygame.sprite.spritecollide(playerTank, wallGroup, dokill=False) or pygame.sprite.spritecollide(playerTank,
                                                                                                            unbreakableWallGroup,
                                                                                                            dokill=False)):
            if int(playerTank.rect.x) % BLOCK_SIZE > 45 or int(playerTank.rect.x) % BLOCK_SIZE < 5:
                wallPosx = int(playerTank.rect.y / BLOCK_SIZE)
                wallPosy = int((playerTank.rect.x + 5) / BLOCK_SIZE)
                if wallPosx < 0:
                    wallPosx = 0
                if initial_board[wallPosx][wallPosy] == 0:
                    playerTank.changeVUp()
            else:
                wallPosx = int(playerTank.rect.y / BLOCK_SIZE)
                wallPosy = int(playerTank.rect.x / BLOCK_SIZE)
                if wallPosx < 0:
                    wallPosx = 0
                wallPosy2 = int(playerTank.rect.x / BLOCK_SIZE) + 1
                if wallPosy2 > 19:
                    wallPosy2 = 19
                if initial_board[wallPosx][wallPosy] == 0 and initial_board[wallPosx][wallPosy2] == 0:
                    playerTank.changeVUp()
        else:
            playerTank.changeVUp()
        playerTank.move()
    elif pressedDown:
        playerTank.vx = 0
        playerTank.vy = 0
        if (pygame.sprite.spritecollide(playerTank, wallGroup, dokill=False) or pygame.sprite.spritecollide(playerTank,
                                                                                                            unbreakableWallGroup,
                                                                                                            dokill=False)):
            if int(playerTank.rect.x) % BLOCK_SIZE > 45 or int(playerTank.rect.x) % BLOCK_SIZE < 5:
                wallPosx = int(playerTank.rect.y / BLOCK_SIZE) + 1
                wallPosy = int((playerTank.rect.x + 5) / BLOCK_SIZE)
                if wallPosx > 13:
                    wallPosx = 13
                if initial_board[wallPosx][wallPosy] == 0:
                    playerTank.changeVDown()
            else:
                wallPosx = int(playerTank.rect.y / BLOCK_SIZE) + 1
                wallPosy = int(playerTank.rect.x / BLOCK_SIZE)
                if wallPosx < 0:
                    wallPosx = 0
                wallPosy2 = int(playerTank.rect.x / BLOCK_SIZE) + 1
                if wallPosy2 > 19:
                    wallPosy2 = 19
                if initial_board[wallPosx][wallPosy] == 0 and initial_board[wallPosx][wallPosy2] == 0:
                    playerTank.changeVDown()
        else:
            playerTank.changeVDown()
        playerTank.move()
    elif pressedRight:
        playerTank.vx=0
        playerTank.vy=0
        if (pygame.sprite.spritecollide(playerTank, wallGroup, dokill=False) or pygame.sprite.spritecollide(playerTank,
                                                                                                            unbreakableWallGroup,
                                                                                                            dokill=False)):
            if int(playerTank.rect.y) % BLOCK_SIZE > 45 or int(playerTank.rect.y) % BLOCK_SIZE < 5:
                wallPosx = int((playerTank.rect.y + 5) / BLOCK_SIZE)
                wallPosy = int(playerTank.rect.x / BLOCK_SIZE) + 1
                if wallPosy > 19:
                    wallPosy = 19
                if initial_board[wallPosx][wallPosy] == 0:
                    playerTank.changeVRight()
            else:
                wallPosx = int(playerTank.rect.y / BLOCK_SIZE)
                wallPosy = int(playerTank.rect.x / BLOCK_SIZE) + 1
                if wallPosy < 0:
                    wallPosy = 0
                wallPosx2 = int(playerTank.rect.y / BLOCK_SIZE) + 1
                if wallPosx2 > 13:
                    wallPosx2 = 13
                if initial_board[wallPosx][wallPosy] == 0 and initial_board[wallPosx2][wallPosy] == 0:
                    playerTank.changeVRight()
        else:
            playerTank.changeVRight()
        playerTank.move()
    if (pygame.sprite.spritecollide(playerTank,tankSprites, dokill=False)):
        for tank in tankSprites:
            print(tank.rect.x, tank.rect.y)
    for bullet in bulletSprites:
        for tank in tankSprites:
            if pygame.sprite.collide_rect(bullet, tank):
                bullet.kill()
                tank.damage()
                print(tank.health)
                if tank.health==0:
                    tank.kill()
    playerTank.update()
    bulletSprites.update()
    tankSprites.update(wallGroup, playerTank)
    allSprite.clear(gameDisplay, background)
    new_positions = allSprite.draw(gameDisplay)
    pygame.display.update(new_positions)

    clock.tick(FPS)


pygame.quit()
quit()
