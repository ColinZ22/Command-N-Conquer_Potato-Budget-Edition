from Constants import *
from Units.Unit import Unit
import pygame


class Tank(Unit):

    def __init__(self, team, row, col, pixelMap, unitMap):
        tankIcon = pygame.image.load('resources/TankIcon.png')
        tankIcon = pygame.transform.scale(tankIcon, (UNIT_IMAGE_WIDTH, UNIT_IMAGE_WIDTH))
        super().__init__(team, hp=160, atkPt=60, row=row, col=col, pixelMap=pixelMap, image=tankIcon, mobility=3, attackRange=1)
        unitMap[self.row][self.col] = self
        self.imageWidth = UNIT_IMAGE_WIDTH
        self.imageHeight = UNIT_IMAGE_WIDTH


    def __str__(self):
        return self.team + ' tank ' + 'at ' + str(self.row) + ', ' + str(self.col) + ' with ' + str(self.hp) + ' hp'
