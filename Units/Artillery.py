from Constants import *
from Units.Unit import Unit
import pygame


class Artillery(Unit):

    def __init__(self, team, row, col, pixelMap, unitMap):
        artilleryIcon = pygame.image.load('resources/ArtilleryIcon.png')
        artilleryIcon = pygame.transform.scale(artilleryIcon, (UNIT_IMAGE_WIDTH, UNIT_IMAGE_WIDTH))
        super().__init__(team, hp=100, atkPt=75, row=row, col=col, pixelMap=pixelMap, image=artilleryIcon, mobility=1, attackRange=3, minAttackRange=1)
        unitMap[self.row][self.col] = self
        self.imageWidth = UNIT_IMAGE_WIDTH
        self.imageHeight = UNIT_IMAGE_WIDTH


    def __str__(self):
        return self.team + ' artillery ' + 'at ' + str(self.row) + ', ' + str(self.col) + ' with ' + str(self.hp) + ' hp'