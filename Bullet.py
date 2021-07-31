from constants import *

class Bullet(pygame.sprite.Sprite):
    damage = 1
    x_size = 10
    y_size = 10
    layer = 9

    def __init__(self, x, y, bullet_image, vx, vy):
        super(Bullet, self).__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = vx
        self.vy = vy

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy


    def update(self):
        self.move()
        if 0 > self.rect.x or self.rect.x > display_width:
            self.kill()
        elif 0 > self.rect.y or self.rect.y > display_height:
            self.kill()
        if initial_board[int(self.rect.y/50)][int(self.rect.x/50)]==1:
            self.kill()



