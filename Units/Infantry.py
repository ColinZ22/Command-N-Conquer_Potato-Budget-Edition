from Constants import *
from Units.Unit import Unit
import pygame


class Infantry(Unit):

    def __init__(self, team, row, col, pixelMap, unitMap):
        InfantryIcon = pygame.image.load('resources/InfantryIcon.png')
        InfantryIcon = pygame.transform.scale(InfantryIcon, (UNIT_IMAGE_WIDTH, UNIT_IMAGE_WIDTH))
        super().__init__(team, hp=75, atkPt=25, row=row, col=col, pixelMap=pixelMap, image=InfantryIcon, mobility=2, attackRange=1)
        unitMap[self.row][self.col] = self
        self.imageWidth = UNIT_IMAGE_WIDTH
        self.imageHeight = UNIT_IMAGE_WIDTH


    def __str__(self):
        return self.team + ' Infantry ' + 'at ' + str(self.row) + ', ' + str(self.col) + ' with ' + str(self.hp) + ' hp'
