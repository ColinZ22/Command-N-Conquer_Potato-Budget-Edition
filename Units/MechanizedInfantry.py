from Constants import *
from Units.Unit import Unit
import pygame


class MechanizedInfantry(Unit):

    def __init__(self, team, row, col, pixelMap, unitMap):
        MechanizedInfantryIcon = pygame.image.load('resources/MechanizedInfantryIcon.png')
        MechanizedInfantryIcon = pygame.transform.scale(MechanizedInfantryIcon, (UNIT_IMAGE_WIDTH, UNIT_IMAGE_WIDTH))
        super().__init__(team, hp=110, atkPt=35, row=row, col=col, pixelMap=pixelMap, image=MechanizedInfantryIcon, mobility=4, attackRange=1)
        unitMap[self.row][self.col] = self
        self.imageWidth = UNIT_IMAGE_WIDTH
        self.imageHeight = UNIT_IMAGE_WIDTH


    def __str__(self):
        return self.team + ' MechanizedInfantry ' + 'at ' + str(self.row) + ', ' + str(self.col) + ' with ' + str(self.hp) + ' hp'
