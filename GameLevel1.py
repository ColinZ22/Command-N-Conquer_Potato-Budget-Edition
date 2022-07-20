import pygame
import pygame_widgets
from pygame_widgets.button import Button
from MouseEventChecker import MouseEventChecker
from Units.Tank import Tank
from Units.Artillery import Artillery
from Hex import Hex
from Constants import *

class GameLevel1:
    def __init__(self, gridRows, gridCols):
        self.height = gridRows
        self.width = gridCols
        self.pixelMap = [[0 for x in range(gridCols)] for y in range(gridRows)]
        self.unitMap = [[0 for x in range(gridCols)] for y in range(gridRows)]
        self.prevHex = None
        self.selectedHex = None
        self.selectedHexIndex = None
        self.endTurnButton = None
        self.playerTurn = "Red"
        self.turnText = None
        self.turnTextRect = None
        self.roundInitialized = False
        self.unitMoving = False

        self.explosionGroup = pygame.sprite.Group()

        self.mouseEventChecker = MouseEventChecker()


    def switchTurns(self):
        if self.playerTurn == "Red":
            self.playerTurn = "Blue"
        elif self.playerTurn == "Blue":
            self.playerTurn = "Red"
        self.roundInitialized = False
        font = pygame.font.Font('freesansbold.ttf', 30)
        self.turnText = font.render(self.playerTurn + "'s Turn", True, PINK if self.playerTurn == "Red" else LIGHT_BLUE)
        self.turnTextRect = self.turnText.get_rect()
        self.turnTextRect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT - GRID_HEIGHT/4)

    def mapInit(self, screen):
        # the leftmost hex of the first row
        rowFirstHex = Hex(xPos=-GRID_WIDTH/2, yPos=-GRID_HEIGHT/3, row=0, col=0)
        hexes = [rowFirstHex]
        # initialize the rest of the hexes
        for x in range(self.height):
            # skipping the 0th row, adding hexes to bottom left of the previous row's left most hex for odd rows,
            # and adding hexes to bottom right of the previous row's right most hex for even rows
            if x != 0:
                if x % 2 == 1:
                    index = 2
                else:
                    index = 4
                # index 2 is bottom left corner, index 4 is bottom right corner
                position = rowFirstHex.corners[index]
                rowFirstHex = Hex(xPos=position[0], yPos=position[1], row=x, col=0)

                self.pixelMap[x][0] = rowFirstHex.getCenterPos()
                hexes.append(rowFirstHex)

            # initializing the rest of the row by placing hexagons to the right of leftmost hexagon, with equal y-values
            hex = rowFirstHex
            for i in range(self.width):
                hex = Hex(xPos=hex.xPos + hex.radius * 2, yPos=hex.yPos, row=x, col=i)
                self.pixelMap[x][i] = hex.getCenterPos()
                hexes.append(hex)

        for hex in hexes:
            hex.renderHex(screen)

        # initializing the end turn button
        buttonWidth, buttonHeight = 65, GRID_HEIGHT/2
        self.endTurnButton = Button(
            screen, WINDOW_WIDTH-buttonWidth, WINDOW_HEIGHT-buttonHeight, buttonWidth, buttonHeight, text='End Turn',
            fontSize=18, margin=10,
            inactiveColour=LIGHT_GREY,
            pressedColour=(CYAN), radius=20,
            onClick=lambda: self.switchTurns()
        )

        font = pygame.font.Font('freesansbold.ttf', 30)
        self.turnText = font.render(self.playerTurn + "'s Turn", True, PINK if self.playerTurn == "Red" else LIGHT_BLUE)
        self.turnTextRect = self.turnText.get_rect()
        self.turnTextRect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT - GRID_HEIGHT/4)

        return hexes, self.pixelMap

    def updateMap(self, screen, hexes, unitMap):
        # initializing each round
        if not self.roundInitialized:
            for hex in hexes:
                hex.canBeMovedTo = False
                hex.canBeAttacked = False
                if unitMap[hex.row][hex.col] != 0:
                    if unitMap[hex.row][hex.col].team == self.playerTurn:
                        unitMap[hex.row][hex.col].canMove = True
                        unitMap[hex.row][hex.col].canAttack = True
                    else:
                        unitMap[hex.row][hex.col].canMove = False
                        unitMap[hex.row][hex.col].canAttack = False
            self.roundInitialized = True

        mousePos = self.mouseEventChecker.mousePos

        # syncing hexMap data with unitMap data and doing some backend calculations like possible moves and attacks
        for hex in hexes:
            try:
                hex.onHexTeam = unitMap[hex.row][hex.col].team
            except:
                hex.onHexTeam = None
            if self.selectedHex is not None:
                if self.selectedHex.onHexTeam is None:
                    hex.canBeMovedTo = False
                else:
                    try:
                        possibleMoves = self.unitMap[self.selectedHex.row][self.selectedHex.col].getMoves(unitMap)
                        if (hex.row, hex.col) in possibleMoves:
                            hex.canBeMovedTo = True
                        else:
                            hex.canBeMovedTo = False
                    except:
                        hex.canBeMovedTo = False
                    try:
                        attacks = self.unitMap[self.selectedHex.row][self.selectedHex.col].getAttacks(unitMap)
                        if (hex.row, hex.col) in attacks and hex.onHexTeam is not None and self.unitMap[self.selectedHex.row][self.selectedHex.col].canAttack:
                            hex.canBeAttacked = True
                        else:
                            hex.canBeAttacked = False
                    except:
                        hex.canBeAttacked = False

        # hexMap state update and unit movement + attack executions
        for hex in hexes:
            hexUpdated = False
            if hex.mouseOnHex(mousePos):
                # if self.mouseEventChecker.leftHeldDown:
                if self.mouseEventChecker.leftClickeRelease():
                    if self.selectedHex is None:
                        # if no unit is selected and the mouse is clicked on a hex, select the hex
                        hex.hexState = 'Selected'
                        self.selectedHex = hex
                    else:
                        # if a unit is selected and the mouse is clicked on a hex
                        if hex.canBeAttacked:
                            try:
                                unitMap[self.selectedHex.row][self.selectedHex.col].attack(hex.row, hex.col, unitMap)
                            except Exception as e:
                                # catch error when the user somehow manages to click too fast
                                # (the unit has already moved)
                                print(e)
                                unitMap[self.prevHex.row][self.prevHex.col].attack(hex.row, hex.col, unitMap)
                        elif hex.canBeMovedTo:
                            try:
                                unitMap[self.selectedHex.row][self.selectedHex.col].moveTo(hex.row, hex.col, unitMap)
                            except Exception as e:
                                # catch error when the user somehow manages to click too fast
                                # (the unit has already moved)
                                print(e)
                            # update hex states after move/attack
                            self.selectedHex.hexState = 'Unselected'
                            hex.hexState = 'Unselected'
                            self.selectedHex = None
                        else:
                            # update hex states when no move/attack is possible
                            self.selectedHex.hexState = 'Unselected'
                            hex.hexState = 'Selected'
                            self.selectedHex = hex

                elif hex.hexState != 'Selected':
                    # when mouse is hovering but not clicking
                    if self.selectedHex is None:
                        hex.hexState = 'Hovering'
                    else:
                        hex.hexState = 'Unselected'
            else:
                # when mouse is not hovering
                if hex.hexState != 'Selected':
                    hex.hexState = 'Unselected'

            if self.selectedHex is None:
                hex.hexState = 'Unselected'
                hex.canBeMovedTo = False
                # hex.canBeAttacked = False

            if self.mouseEventChecker.rightClicked():
                # unselect everything and remove all effects on right click
                hex.hexState = 'Unselected'
                if self.selectedHex is not None:
                    self.selectedHex.hexState = 'Unselected'
                    self.selectedHex = None
                if hex.canBeMovedTo:
                    hex.canBeMovedTo = False
                if hex.canBeAttacked:
                    hex.canBeAttacked = False
            self.prevHex = self.selectedHex

        for hex in hexes:
            hex.renderHex(screen)

    def initUnits(self):

        Tank('Red', row=7, col=8, pixelMap=self.pixelMap, unitMap=self.unitMap)
        Tank('Red', row=7, col=9, pixelMap=self.pixelMap, unitMap=self.unitMap)
        Artillery('Red', row=8, col=9, pixelMap=self.pixelMap, unitMap=self.unitMap)
        Artillery('Red', row=8, col=10, pixelMap=self.pixelMap, unitMap=self.unitMap)
        Tank('Red', row=7, col=10, pixelMap=self.pixelMap, unitMap=self.unitMap)
        Tank('Red', row=7, col=11, pixelMap=self.pixelMap, unitMap=self.unitMap)
        Artillery('Blue', row=2, col=2, pixelMap=self.pixelMap, unitMap=self.unitMap)
        Artillery('Blue', row=3, col=3, pixelMap=self.pixelMap, unitMap=self.unitMap)
        Tank('Blue', row=2, col=3, pixelMap=self.pixelMap, unitMap=self.unitMap)
        Tank('Blue', row=2, col=4, pixelMap=self.pixelMap, unitMap=self.unitMap)
        Tank('Blue', row=3, col=4, pixelMap=self.pixelMap, unitMap=self.unitMap)
        Tank('Blue', row=3, col=10, pixelMap=self.pixelMap, unitMap=self.unitMap)
        Artillery('Blue', row=3, col=11, pixelMap=self.pixelMap, unitMap=self.unitMap)
        Artillery('Blue', row=3, col=12, pixelMap=self.pixelMap, unitMap=self.unitMap)

        return self.unitMap

    def renderUnits(self, screen, unitMap):
        for i in unitMap:
            for unit in i:
                if unit != 0:
                    self.unitMoving = unit.updateUnit(screen, unitMap, self.explosionGroup)
                    if self.unitMoving:
                        self.selectedHex = None
        self.explosionGroup.draw(screen)
        self.explosionGroup.update()

    def checkEndCondition(self, hexes):
        redTeamExists = False
        blueTeamExists = False
        for hex in hexes:
            if hex.onHexTeam == "Red":
                redTeamExists = True
            elif hex.onHexTeam == "Blue":
                blueTeamExists = True
        if not redTeamExists:
            return "Blue"
        elif not blueTeamExists:
            return "Red"
        else:
            return None

def main():

    running = True
    pygame.init()

    gameLevel1 = GameLevel1(gridRows=GRID_ROWS, gridCols=GRID_COLS)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Game Level 1")
    clock = pygame.time.Clock()
    hexes = gameLevel1.mapInit(screen)[0]
    units = gameLevel1.initUnits()

    while running:
        events = pygame.event.get()
        gameLevel1.mouseEventChecker.leftHeldDown = pygame.mouse.get_pressed()[0]
        gameLevel1.mouseEventChecker.rightHeldDown = pygame.mouse.get_pressed()[2]
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                gameLevel1.mouseEventChecker.clicked = True
            if not event.type == pygame.MOUSEBUTTONDOWN:
                gameLevel1.mouseEventChecker.clicked = False
            if event.type == pygame.MOUSEBUTTONUP:
                gameLevel1.mouseEventChecker.released = True
            if not event.type == pygame.MOUSEBUTTONUP:
                gameLevel1.mouseEventChecker.released = False

        gameLevel1.mouseEventChecker.update()
        gameLevel1.updateMap(screen, hexes, units)
        gameLevel1.renderUnits(screen, units)
        pygame.draw.rect(screen,
                         RED if gameLevel1.playerTurn == "Red" else BLUE,
                         pygame.Rect(0, WINDOW_HEIGHT - (GRID_HEIGHT + 1) / 2, WINDOW_WIDTH, GRID_HEIGHT))
        pygame_widgets.update(events)

        screen.blit(gameLevel1.turnText, gameLevel1.turnTextRect)

        endTeam = gameLevel1.checkEndCondition(hexes)
        if endTeam is not None:
            font = pygame.font.Font('freesansbold.ttf', 50)
            winText = font.render(endTeam + " Won!!!", True, RED if endTeam == "Red" else BLUE)
            winTextRect = winText.get_rect()
            winTextRect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            screen.blit(winText, winTextRect)

        pygame.display.flip()

        clock.tick(GAME_FPS)
    pygame.display.quit()
