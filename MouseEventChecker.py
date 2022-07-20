import time
import pygame

class MouseEventChecker:
    def __init__(self):
        # start time
        self.start = time.time()

        # timer is the amount of time passed after mouse is pressed
        self.leftClickTimer = 0

        self.clicked = False
        self.released = False

        self.leftHeldDown = False
        self.rightHeldDown = False

        self.mousePos = None

        self.currentTime = 0

    def update(self):
        self.currentTime = time.time()

        # left click timer update
        if self.leftHeldDown:
            if self.clicked:
                self.leftClickTimer = self.currentTime - self.start
        elif self.rightHeldDown:
            self.leftClickTimer = 0
        else:
            if self.released:
                self.start = self.currentTime

        # mouse position update
        self.mousePos = pygame.mouse.get_pos()

    def leftClickeRelease(self):
        return self.released and self.leftClickTimer != 0

    def rightClicked(self):
        return self.rightHeldDown