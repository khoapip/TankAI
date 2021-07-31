import Helper, os, pygame
DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(DIR_ROOT, "images")
initial_board = Helper.readFile("map.txt")
playerHealth=100
enemyHealth=30

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
BLOCK_SIZE = 50
FPS = 40
display_width = 1000
display_height = 700
row_num = display_height // BLOCK_SIZE
column_num = display_width // BLOCK_SIZE
MAX_INT = 10000
delta = 2.5

green_tank_left = Helper.cut_subsurface(os.path.join(IMAGES, "green_tank_left.png"), BLOCK_SIZE, BLOCK_SIZE)
green_tank_down = Helper.cut_subsurface(os.path.join(IMAGES, "green_tank_down.png"), BLOCK_SIZE, BLOCK_SIZE)
green_tank_up = Helper.cut_subsurface(os.path.join(IMAGES, "green_tank_up.png"), BLOCK_SIZE, BLOCK_SIZE)
green_tank_right = Helper.cut_subsurface(os.path.join(IMAGES, "green_tank_right.png"), BLOCK_SIZE, BLOCK_SIZE)

blue_tank_left = Helper.cut_subsurface(os.path.join(IMAGES, "blue_tank_left.png"), BLOCK_SIZE, BLOCK_SIZE)
blue_tank_down = Helper.cut_subsurface(os.path.join(IMAGES, "blue_tank_down.png"), BLOCK_SIZE, BLOCK_SIZE)
blue_tank_up = Helper.cut_subsurface(os.path.join(IMAGES, "blue_tank_up.png"), BLOCK_SIZE, BLOCK_SIZE)
blue_tank_right = Helper.cut_subsurface(os.path.join(IMAGES, "blue_tank_right.png"), BLOCK_SIZE, BLOCK_SIZE)

wall1_img = pygame.image.load(os.path.join(IMAGES, 'wall.png'))
wall2_img = pygame.image.load(os.path.join(IMAGES, "wall2.png"))
road_img = pygame.image.load(os.path.join(IMAGES, "road.png"))
bullet_img = pygame.image.load(os.path.join(IMAGES, "bullet.png"))
explosion_img=pygame.image.load(os.path.join(IMAGES, "explosion.png"))
