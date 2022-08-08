import math
from Constants import *
from Explosion import Explosion


class Unit(object):

    def __init__(self, team, hp, atkPt, row, col, pixelMap, image, mobility, attackRange, minAttackRange=0):
        self.team = team
        self.hp = hp
        self.atkPt = atkPt
        self.row = row
        self.col = col
        self.pixelMap = pixelMap
        self.image = image
        self.mobility = mobility
        self.attackRange = attackRange
        self.minAttackRange = minAttackRange
        self.canMove = False
        self.canAttack = False
        self.underAttack = False
        self.moving = False

        self.imageWidth = UNIT_IMAGE_WIDTH
        self.imageHeight = UNIT_IMAGE_WIDTH

        self.rowPixel = pixelMap[row][col][0] - self.imageWidth // 2
        self.colPixel = pixelMap[row][col][1] - self.imageHeight // 2

    def getMoves(self, unitMap):
        minHexDiameter = GRID_WIDTH
        moves = []
        if self.canMove:
            for i in range(self.row - self.mobility, self.row + self.mobility + 1):
                for j in range(self.col - self.mobility, self.col + self.mobility + 1):
                    if 0 <= i < GRID_ROWS and 0 <= j < GRID_COLS:
                        distanceBetween = math.dist(self.pixelMap[self.row][self.col], self.pixelMap[i][j])
                        outOfBounds = self.pixelMap[i][j][0] > WINDOW_WIDTH or self.pixelMap[i][j][1] > WINDOW_HEIGHT
                        if round(distanceBetween, 4) <= self.mobility * minHexDiameter and unitMap[i][j] == 0 \
                                and not outOfBounds:
                            moves.append((i, j))
        else:
            pass
        return moves

    def getAttacks(self, unitMap):
        minHexDiameter = GRID_WIDTH
        attackHexes = []
        for i in range(self.row - self.attackRange, self.row + self.attackRange + 1):
            for j in range(self.col - self.attackRange, self.col + self.attackRange + 1):
                if 0 <= i < GRID_ROWS and 0 <= j < GRID_COLS:
                    distanceBetween = math.dist(self.pixelMap[self.row][self.col], self.pixelMap[i][j])
                    outOfBounds = self.pixelMap[i][j][0] > WINDOW_WIDTH or self.pixelMap[i][j][1] > WINDOW_HEIGHT
                    if self.attackRange * minHexDiameter >= round(distanceBetween, 4) >= self.minAttackRange * minHexDiameter and \
                            unitMap[i][j] != 0 and not outOfBounds and unitMap[i][j].team != self.team and \
                            unitMap[i][j].hp > 0 and (i, j) != (self.row, self.col):
                        attackHexes.append((i, j))
        return attackHexes

    def attack(self, row, col, unitMap):
        if self.canAttack:
            unitMap[row][col].hp = unitMap[row][col].hp - self.atkPt
            unitMap[row][col].underAttack = True
            print(unitMap[self.row][self.col], "attacked,")
            print(unitMap[row][col], "remaining was hit!!!")
            self.canAttack = False

    def moveTo(self, row, col, unitMap):
        if self.canMove:
            self.moving = True
            unitMap[self.row][self.col] = 0
            self.row = row
            self.col = col
            unitMap[self.row][self.col] = self
            self.canMove = False
            return True
        else:
            return False

    def moveUnitImage(self, row, col):
        rowDiff = self.pixelMap[row][col][0] - self.imageWidth // 2
        colDiff = self.pixelMap[row][col][1] - self.imageHeight // 2
        if self.rowPixel < rowDiff and not abs(rowDiff) < 1:
            self.rowPixel += UNIT_MOVE_SPEED
        elif self.rowPixel > rowDiff and not abs(rowDiff) < 1:
            self.rowPixel -= UNIT_MOVE_SPEED
        if self.colPixel < colDiff and not abs(colDiff) < 1:
            self.colPixel += UNIT_MOVE_SPEED
        elif self.colPixel > colDiff and not abs(colDiff) < 1:
            self.colPixel -= UNIT_MOVE_SPEED

        if abs(self.rowPixel - (self.pixelMap[row][col][0] - self.imageWidth // 2)) < 2 and \
                abs(self.colPixel - (self.pixelMap[row][col][1] - self.imageHeight // 2)) < 2:
            self.rowPixel = self.pixelMap[row][col][0] - self.imageWidth // 2
            self.colPixel = self.pixelMap[row][col][1] - self.imageHeight // 2
            self.moving = False

    def updateUnit(self, screen, unitMap, explosionGroup):
        if self.hp > 0:
            if self.moving:
                # iterates image coordinates and moves it towards the target hex
                self.moveUnitImage(self.row, self.col)
            if self.underAttack:
                # animate explosion if unit is alive and under attack
                explosion = Explosion(self.pixelMap[self.row][self.col][0], self.pixelMap[self.row][self.col][1])
                explosionGroup.add(explosion)
                self.underAttack = False

            screen.blit(self.image, (self.rowPixel, self.colPixel))
        else:
            # animate explosion if unit is killed
            explosion = Explosion(self.pixelMap[self.row][self.col][0], self.pixelMap[self.row][self.col][1])
            explosionGroup.add(explosion)
            self.underAttack = False

            print(self, "removed from map")
            unitMap[self.row][self.col] = 0
        return self.moving




