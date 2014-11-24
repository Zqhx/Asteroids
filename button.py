import pygame
from pygame.locals import *
from pygame.color import THECOLORS as colour

import retroSnake


class Button(object):
    def __init__(self, position, callback, text, font=("", 32)):
        self.pos = position
        self.text = text
        self.font = font
        self.callback = callback
        self.hover = False

        self.genImages()

    def genImages(self):
        # Generate image for the black half of the screen
        textSurf = retroSnake.printf(self.font, (0, 80, 0), self.text)
        textRect = textSurf.get_rect()
        image = pygame.Surface((textRect.width+40, textRect.height+40))
        image.fill((0, 42, 0))
        image.set_clip(image.get_rect().inflate(-15, -15))
        image.fill((0, 0, 0))
        image.set_clip()
        blitCenter(image, textSurf, (textRect.height+40)/2 - textRect.height/2)
        self.image = image

        textSurf = retroSnake.printf(self.font, (0, 240, 0), self.text)
        textRect = textSurf.get_rect()
        image = pygame.Surface((textRect.width+40, textRect.height+40))
        image.fill((0, 200, 0))
        image.set_clip(image.get_rect().inflate(-15, -15))
        image.fill((0, 0, 0))
        image.set_clip()
        blitCenter(image, textSurf, (textRect.height+40)/2 - textRect.height/2)
        self.hImage = image

        # Generate bounding rect
        self.rect = image.get_rect()
        if self.pos[0] == "center":
            self.rect.top = self.pos[1]
            screen = pygame.display.get_surface()
            self.rect.left = screen.get_rect().width/2 - self.rect.width/2
        else:
            self.rect.topleft = self.pos

    def setText(self, text):
        # When text changes, the images need to be regenerated
        self.text = text
        self.genImages()

    def setCallback(self, func):
        self.callback = func

    def blit(self, dest):
        dest.blit(self.image if not self.hover else self.hImage, self.rect)

    def handle(self, event):
        mPos = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mPos):
                return self.callback()
        if event.type == MOUSEMOTION:
            self.hover = self.rect.collidepoint(mPos)


def blitCenter(dest, src, y):
    x = dest.get_rect().width/2 - src.get_rect().width/2
    dest.blit(src, (x, y))
