from Constants import *
from Units.Unit import Unit
import pygame


class HeavyInfantry(Unit):

    def __init__(self, team, row, col, pixelMap, unitMap):
        HeavyInfantryIcon = pygame.image.load('resources/HeavyInfantryIcon.png')
        HeavyInfantryIcon = pygame.transform.scale(HeavyInfantryIcon, (UNIT_IMAGE_WIDTH, UNIT_IMAGE_WIDTH))
        super().__init__(team, hp=80, atkPt=45, row=row, col=col, pixelMap=pixelMap, image=HeavyInfantryIcon, mobility=2, attackRange=1)
        unitMap[self.row][self.col] = self
        self.imageWidth = UNIT_IMAGE_WIDTH
        self.imageHeight = UNIT_IMAGE_WIDTH


    def __str__(self):
        return self.team + ' HeavyInfantry ' + 'at ' + str(self.row) + ', ' + str(self.col) + ' with ' + str(self.hp) + ' hp'
