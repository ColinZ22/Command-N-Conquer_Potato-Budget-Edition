from Constants import *
from typing import Tuple
import pygame
import math

class Hex:
    def __init__(self, xPos, yPos, row, col, hexState="Unselected"):
        self.xPos = xPos
        self.yPos = yPos
        self.radius = GRID_WIDTH / 2
        self.maxRadius = GRID_WIDTH / 2
        self.corners = self.calculateCorners()
        self.hexState = hexState
        self.row = row
        self.col = col

        self.hexBlueFadeGen = self.getColorFadeGen(LIGHT_GREY, BLUE)
        self.hexRedFadeGen = self.getColorFadeGen(LIGHT_GREY, RED)
        self.hexLGreenFadeGen = self.getColorFadeGen(LIGHT_GREY, LIGHT_GREEN)
        self.attackedGen = self.getColorFadeGen(LIGHT_GREY, ORANGE)
        self.onHexTeam = None
        self.canBeMovedTo = False
        self.canBeAttacked = False

    def calculateCorners(self):
        halfMaxRadius = self.maxRadius / 2
        halfRadius = self.radius / 2
        return [
            (self.xPos, self.yPos),                                   # Top Corner
            (self.xPos - self.radius, self.yPos + halfMaxRadius),     # Top Left Corner
            (self.xPos - self.radius, self.yPos + 3 * halfMaxRadius), # Bottom Left Corner
            (self.xPos, self.yPos + 2 * self.maxRadius),              # Bottom Corner
            (self.xPos + self.radius, self.yPos + 3 * halfMaxRadius), # Bottom Right Corner
            (self.xPos + self.radius, self.yPos + halfMaxRadius),     # Top Right Corner
        ]

    def getCenterPos(self):
        return self.xPos, self.yPos + self.maxRadius

    def mouseOnHex(self, mousePos: Tuple[float, float]):
        return abs(mousePos[0] - self.getCenterPos()[0]) < self.radius * 0.9 and \
               abs(mousePos[1] - self.getCenterPos()[1]) < self.radius * 0.9

    def renderHex(self, screen):
        if self.hexState == "Unselected":
            if self.onHexTeam == "Red":
                pygame.draw.polygon(screen, RED, self.corners)
            elif self.onHexTeam == "Blue":
                pygame.draw.polygon(screen, BLUE, self.corners)
            else:
                self.unselectedHex(screen)
        elif self.hexState == "Selected":
            if self.canBeAttacked:
                pass
            if self.onHexTeam == "Red":
                self.redTeamUnit(screen)
            elif self.onHexTeam == "Blue":
                self.blueTeamUnit(screen)
            else:
                self.neutralUnit(screen)
        elif self.hexState == "Hovering":
            if self.onHexTeam == "Red":
                pygame.draw.polygon(screen, RED, self.corners)
            elif self.onHexTeam == "Blue":
                pygame.draw.polygon(screen, BLUE, self.corners)
            else:
                self.hoverHex(screen)

        if self.canBeAttacked:
            self.showAttackedCircle(screen)
        if self.canBeMovedTo:
            self.showMoveCircle(screen)

    def redTeamUnit(self, screen):
        pygame.draw.polygon(screen, self.hexRedFadeGen.__next__(), self.corners)
        pygame.draw.aalines(screen, BLUE, closed=True, points=self.corners, blend=1)

    def blueTeamUnit(self, screen):
        pygame.draw.polygon(screen, self.hexBlueFadeGen.__next__(), self.corners)
        pygame.draw.aalines(screen, BLUE, closed=True, points=self.corners, blend=1)

    def neutralUnit(self, screen):
        pygame.draw.polygon(screen, self.hexLGreenFadeGen.__next__(), self.corners)
        pygame.draw.aalines(screen, BLUE, closed=True, points=self.corners, blend=1)

    def hoverHex(self, screen):
        pygame.draw.polygon(screen, LIGHT_GREY, self.corners)
        pygame.draw.aalines(screen, BLUE, closed=True, points=self.corners, blend=1)

    def unselectedHex(self, screen):
        pygame.draw.polygon(screen, BACKGROUND_COLOR, self.corners)
        pygame.draw.aalines(screen, GREY, closed=True, points=self.corners)

    def showMoveCircle(self, screen):
        width = GRID_WIDTH / 2 * 0.7
        height = GRID_HEIGHT / 2 * 0.6
        circle = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(circle, LIME_GREEN, (width, width), width)
        screen.blit(circle, (self.getCenterPos()[0] - width, self.getCenterPos()[1] - height))

    def showAttackedCircle(self, screen):
        width = GRID_WIDTH / 2 * 0.7
        height = GRID_HEIGHT / 2 * 0.6
        circle = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(circle, self.attackedGen.__next__(), (width, width), width)
        screen.blit(circle, (self.getCenterPos()[0] - width, self.getCenterPos()[1] - height))

    def getColorFadeGen(self, fromRGB, toRGB, fadeSteps=20):
        rDiff = toRGB[0] - fromRGB[0]
        gDiff = toRGB[1] - fromRGB[1]
        bDiff = toRGB[2] - fromRGB[2]
        newRGB = fromRGB
        while True:
            if newRGB.__eq__(toRGB):
                tempRGB = toRGB
                toRGB = fromRGB
                fromRGB = tempRGB
                rDiff = -rDiff
                gDiff = -gDiff
                bDiff = -bDiff
            if abs(toRGB[0] - newRGB[0]) < 1.5 * abs(rDiff / fadeSteps):
                r = toRGB[0]
            else:
                r = newRGB[0] + rDiff / fadeSteps
            if abs(toRGB[1] - newRGB[1]) < 1.5 * abs(gDiff / fadeSteps):
                g = toRGB[1]
            else:
                g = newRGB[1] + gDiff / fadeSteps
            if abs(toRGB[2] - newRGB[2]) < 1.5 * abs(bDiff / fadeSteps):
                b = toRGB[2]
            else:
                b = newRGB[2] + bDiff / fadeSteps
            newRGB = (r, g, b)
            yield newRGB


