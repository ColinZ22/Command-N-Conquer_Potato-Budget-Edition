import pygame
from Constants import *


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 19):
            img = pygame.image.load(f"resources/explosion_sprite_pngs/tile{num}.png")
            img = pygame.transform.scale(img, (UNIT_IMAGE_WIDTH * 0.9, UNIT_IMAGE_HEIGHT * 0.9))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        # higher time value means slower animation speed
        explosion_time = 1
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_time and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_time:
            self.kill()
