from constants import *
import copy

class TankGroup(pygame.sprite.Group):

    def __init__(self, board, bulletSprite, allSprite):
        super(TankGroup, self).__init__()
        self.static_board = copy.deepcopy(board)
        self.bulletSprite = bulletSprite
        self.allSprite = allSprite


    def generateCurrentMap(self,wallGroup, playerTank):
        change_board = copy.deepcopy(self.static_board)
        for tank in self:
            position = tank.get_current_tile()
            if change_board[position[1]][position[0]] == 0:
                change_board[position[1]][position[0]] = 'T'
        playerPosition = playerTank.get_current_tile()
        if change_board[playerPosition[1]][playerPosition[0]] == 0:
            change_board[playerPosition[1]][playerPosition[0]] = 'P'
        for tile in wallGroup:
            change_board[tile.row][tile.column] = tile.hard
        return change_board

    def update(self, wallGroup, playerTank):
        change_board = self.generateCurrentMap(wallGroup, playerTank)
        for tank in self:
            tank.updateAI(change_board, playerTank, self.bulletSprite, self.allSprite)

