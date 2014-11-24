import pygame
from pygame.locals import *

import retroSnake

from button import Button


class Menu():
    def __init__(self, game):
        self.game = game

        self.title = retroSnake.Entity()
        self.title.setSprite(retroSnake.loadSprite('title'))
        self.title.doTransform(retroSnake.TranslateMatrix(0, -20))
        self.title.sprite.doTransform(retroSnake.ScaleMatrix(6))

        self.camera = retroSnake.Camera()
        self.camera.scale = 10
        self.camera.buildMatrix()

        self.font = pygame.font.Font('assets/starcraft.ttf', 24)
        self.b1 = Button(('center', 280), game.nextState, 'Play', self.font)
        self.b2 = Button(('center', 280), game.exit, 'Quit', self.font)
        self.b1.rect.move_ip(-100, 0)
        self.b2.rect.move_ip(+100, 0)

        self.score = -42
        self.reset()

    def reset(self):
        if self.score < 0:
            score = 'WASD+Space'
        else:
            score = '%d' % self.score
        font = pygame.font.Font('assets/starcraft.ttf', 46)
        self.scoreText = retroSnake.printf(font, (0, 255, 0), score)
        self.scorePos = (320-(self.scoreText.get_rect().width/2), 160)

    def update(self):
        return

    def render(self, screen):
        self.title.render(screen, self.camera.transform)
        self.b1.blit(screen)
        self.b2.blit(screen)

        if self.score is not None:
            pygame.display.get_surface().blit(
                self.scoreText,
                self.scorePos
            )

    def onEvent(self, event):
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                self.game.nextState()
        if event.type == MOUSEBUTTONDOWN:
            p = retroSnake.Vector(*pygame.mouse.get_pos())
        if event.type == MOUSEMOTION:
            self.pointer = self.camera.unproject(
                retroSnake.Vector(*pygame.mouse.get_pos())
                )
        self.b1.handle(event)
        self.b2.handle(event)
