from Bullet import *
from constants import *
from queue import Queue


class Tank(pygame.sprite.Sprite):
    tank_speed = 2.5

    green_right_frames = green_tank_right
    green_left_frames = green_tank_left
    green_up_frames = green_tank_up
    green_down_frames = green_tank_down

    blue_right_frames = blue_tank_right
    blue_left_frames = blue_tank_left
    blue_up_frames = blue_tank_up
    blue_down_frames = blue_tank_down

    def __init__(self, x, y, orientation, health):
        super(Tank, self).__init__()
        self.frame_nums = len(Tank.green_right_frames)
        self.life = 3
        self.orientation = orientation
        self.health = health
        if self.orientation == "R":
            self.cur_frames = Tank.green_right_frames
        elif self.orientation == "L":
            self.cur_frames = Tank.green_left_frames
        elif self.orientation == "U":
            self.cur_frames = Tank.green_up_frames
        elif self.orientation == "D":
            self.cur_frames = Tank.green_down_frames
        elif self.orientation == "r":
            self.cur_frames = Tank.blue_right_frames
        elif self.orientation == "l":
            self.cur_frames = Tank.blue_left_frames
        elif self.orientation == "u":
            self.cur_frames = Tank.blue_up_frames
        else:
            self.cur_frames = Tank.blue_down_frames
        self.cur_frame_num = 0
        self.image = self.cur_frames[self.cur_frame_num]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        self.counter = 0
        self.last_shoot_counter = FPS

    def changeVLeft(self):
        self.vx = -Tank.tank_speed
        self.vy = 0
        self.orientation = "L"
        self.cur_frames = Tank.green_left_frames

    def changeVRight(self):
        self.vx = Tank.tank_speed
        self.vy = 0
        self.orientation = "R"
        self.cur_frames = Tank.green_right_frames

    def changeVDown(self):
        self.vx = 0
        self.vy = Tank.tank_speed
        self.orientation = "D"
        self.cur_frames = Tank.green_down_frames

    def changeVUp(self):
        self.vx = 0
        self.vy = -Tank.tank_speed
        self.orientation = "U"
        self.cur_frames = Tank.green_up_frames

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

    def get_current_tile(self):
        x = self.rect.x
        y = self.rect.y
        if self.rect.x % 50 >= 45:
            x = self.rect.x + 5
        if self.rect.y % 50 >= 45:
            y = self.rect.y + 5
        return (x // BLOCK_SIZE, y // BLOCK_SIZE)

    def update(self):
        self.counter += 1
        self.last_shoot_counter += 1
        self.change_frame(10)

    def change_frame(self, switch_counter):
        if self.counter % switch_counter == 0:
            self.cur_frame_num += 1
        if self.cur_frame_num > (self.frame_nums - 1):
            self.cur_frame_num = 0
        self.image = self.cur_frames[self.cur_frame_num]

    def shoot(self):
        if self.last_shoot_counter >= FPS / 2:
            if self.orientation == "R":
                bullet = Bullet(self.rect.x + BLOCK_SIZE + 2, self.rect.y + BLOCK_SIZE / 2 - Bullet.x_size / 2,
                                bullet_img, 10, 0)
            elif self.orientation == "L":
                bullet = Bullet(self.rect.x - 2, self.rect.y + BLOCK_SIZE / 2 - Bullet.x_size / 2, bullet_img, -10, 0)
            elif self.orientation == "D":
                bullet = Bullet(self.rect.x + BLOCK_SIZE / 2 - Bullet.x_size / 2, self.rect.y + BLOCK_SIZE + 2,
                                bullet_img, 0, 10)
            else:  # up
                bullet = Bullet(self.rect.x + BLOCK_SIZE / 2 - Bullet.x_size / 2, self.rect.y - 2, bullet_img, 0, -10)
            self.last_shoot_counter = 0
            return bullet
        return None

    def damage(self):
        self.health = self.health - 10


class TankAI(Tank):
    # state: S stop
    # state: M moving

    def __init__(self, x, y, orientation, state, health):
        super(TankAI, self).__init__(x, y, orientation,health)
        self.shortest_path_tree = dict()
        self.state = state
        self.health = health

    def findShortestPathRecursive(self, map, tank_pos, queue, already_traversed):
        source = queue.get()
        source_column = source[0]
        source_row = source[1]
        destination_column = tank_pos[0]
        destination_row = tank_pos[1]
        height = len(map)
        width = len(map[0])

        latest_distance = self.shortest_path_tree[(source_column, source_row)]

        if source_column + 1 == destination_column and source_row == destination_row:
            self.shortest_path_tree[(source_column + 1, source_row)] = latest_distance + 1
            return
        elif source_column - 1 == destination_column and source_row == destination_row:
            self.shortest_path_tree[(source_column - 1, source_row)] = latest_distance + 1
            return
        elif source_column == destination_column and source_row + 1 == destination_row:
            self.shortest_path_tree[(source_column, source_row + 1)] = latest_distance + 1
            return
        elif source_column == destination_column and source_row - 1 == destination_row:
            self.shortest_path_tree[(source_column, source_row - 1)] = latest_distance + 1
            return

        if source_column + 1 < width and map[source_row][source_column + 1] == 0 and (
        source_column + 1, source_row) not in already_traversed:
            self.shortest_path_tree[(source_column + 1, source_row)] = latest_distance + 1
            queue.put((source_column + 1, source_row))
            already_traversed.add((source_column + 1, source_row))
        if source_column - 1 < width and map[source_row][source_column - 1] == 0 and (
        source_column - 1, source_row) not in already_traversed:
            self.shortest_path_tree[(source_column - 1, source_row)] = latest_distance + 1
            queue.put((source_column - 1, source_row))
            already_traversed.add((source_column - 1, source_row))
        if source_row + 1 < height and map[source_row + 1][source_column] == 0 and (
        source_column, source_row + 1) not in already_traversed:
            self.shortest_path_tree[(source_column, source_row + 1)] = latest_distance + 1
            queue.put((source_column, source_row + 1))
            already_traversed.add((source_column, source_row + 1))
        if source_row - 1 < height and map[source_row - 1][source_column] == 0 and (
        source_column, source_row - 1) not in already_traversed:
            self.shortest_path_tree[(source_column, source_row - 1)] = latest_distance + 1
            queue.put((source_column, source_row - 1))
            already_traversed.add((source_column, source_row - 1))

        if queue.qsize() > 0:
            self.findShortestPathRecursive(map, tank_pos, queue, already_traversed)

    def fill_shortest_path_tree(self):
        row_num = display_height // BLOCK_SIZE
        column_num = display_width // BLOCK_SIZE
        for r in range(row_num):
            for c in range(column_num):
                self.shortest_path_tree[(c, r)] = MAX_INT

    def findShortestPath(self, destination, map):
        queue = Queue()
        self.fill_shortest_path_tree()
        source = self.get_current_tile()
        source_column = source[0]
        source_row = source[1]
        already_traversed = set()
        self.shortest_path_tree[(destination[0], destination[1])] = 0
        queue.put((destination[0], destination[1]))
        already_traversed.add((destination[0], destination[1]))
        self.findShortestPathRecursive(map, (source_column, source_row), queue, already_traversed)

    def change_states(self, map, playerTank, bulletSprite, allSprite):
        player_location = playerTank.get_current_tile()
        my_position = self.get_current_tile()
        if player_location[0] == my_position[0]:
            if playerTank.rect.x < self.rect.x and self.orientation == "u":
                bullet = self.shoot()
                if (bullet):
                    print("Shooting")
                    bulletSprite.add(bullet)
                    allSprite.add(bullet)
            elif playerTank.rect.x > self.rect.x and self.orientation == "d":
                bullet = self.shoot()
                if (bullet):
                    print("Shooting")
                    bulletSprite.add(bullet)
                    allSprite.add(bullet)
        elif player_location[1] == my_position[1]:
            if playerTank.rect.y < self.rect.y and self.orientation == "l":
                bullet = self.shoot()
                if (bullet):
                    print("Shooting")
                    bulletSprite.add(bullet)
                    allSprite.add(bullet)
            elif playerTank.rect.y > self.rect.y and self.orientation == "r":
                bullet = self.shoot()
                if (bullet):
                    print("Shooting")
                    bulletSprite.add(bullet)
                    allSprite.add(bullet)

    def updateAI(self, map, playerTank, bulletSprite, allSprite):
        self.counter += 1
        self.last_shoot_counter += 1
        if self.state != "S":  # if state is not static, then move
            self.change_states(map, playerTank, bulletSprite, allSprite)
            if self.counter % 1000:
                player_location = playerTank.get_current_tile()

                self.findShortestPath(player_location, map)
                # Helper.print_map(map)
                # Helper.print_best_move_map(self.shortest_path_tree, map)
                current_x = self.rect.x // BLOCK_SIZE
                current_y = self.rect.y // BLOCK_SIZE
                # print(self.shortest_path_tree[(current_x, current_y)])
                left = current_x - 1
                right = current_x + 1
                up = current_y - 1
                down = current_y + 1

                if abs(self.rect.y - current_y * BLOCK_SIZE) < delta and \
                    (left, current_y) in self.shortest_path_tree and \
                    (current_x, current_y) in self.shortest_path_tree and \
                    self.shortest_path_tree[(left, current_y)] < self.shortest_path_tree[(current_x, current_y)]:
                    self.changeVLeft()
                elif abs(self.rect.y - current_y * BLOCK_SIZE) < delta and \
                    (right, current_y) in self.shortest_path_tree and \
                    (current_x, current_y) in self.shortest_path_tree and \
                    self.shortest_path_tree[(right, current_y)] < self.shortest_path_tree[(current_x, current_y)]:
                    self.changeVRight()
                elif abs(self.rect.x - current_x * BLOCK_SIZE) < delta and \
                    (current_x, up) in self.shortest_path_tree and \
                    (current_x, current_y) in self.shortest_path_tree and \
                    self.shortest_path_tree[(current_x, up)] < self.shortest_path_tree[(current_x, current_y)]:
                    self.changeVUp()
                elif abs(self.rect.x - current_x * BLOCK_SIZE) < delta and \
                    (current_x, down) in self.shortest_path_tree and \
                    (current_x, current_y) in self.shortest_path_tree and \
                    self.shortest_path_tree[(current_x, down)] < self.shortest_path_tree[(current_x, current_y)]:
                    self.changeVDown()
                self.move()
        self.change_frame(10)

    def changeVLeft(self):
        self.vx = -Tank.tank_speed
        self.vy = 0
        self.orientation = "L"
        self.cur_frames = TankAI.blue_left_frames

    def changeVRight(self):
        self.vx = Tank.tank_speed
        self.vy = 0
        self.orientation = "R"
        self.cur_frames = TankAI.blue_right_frames

    def changeVDown(self):
        self.vx = 0
        self.vy = Tank.tank_speed
        self.orientation = "D"
        self.cur_frames = TankAI.blue_down_frames

    def changeVUp(self):
        self.vx = 0
        self.vy = -Tank.tank_speed
        self.orientation = "U"
        self.cur_frames = TankAI.blue_up_frames

    def damage(self):
        self.health = self.health - 10
