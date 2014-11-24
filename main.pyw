import sys

import pygame
from pygame.locals import *

import retroSnake

from game import Game
from menu import Menu


class Asteroids(retroSnake.Game):
    def __init__(self):
        super(Asteroids, self).__init__()

        self.menu = Menu(self)
        self.game = Game(self)
        self.state = self.menu

        self.mask = pygame.display.get_surface().convert_alpha()
        self.mask.fill((0, 0, 0, 0))
        for y in xrange(0, 480, 2):
            pygame.draw.line(self.mask, (0, 0, 0, 255), (0, y), (640, y), 1)
        self.badLines = range(0, 480, 480/3)

    def update(self):
        self.state.update()
        self.badLines = [(x+1) % 480 for x in self.badLines]

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.state.render(screen)

        screen.blit(self.mask, (0, 0))
        for y in self.badLines:
            pygame.draw.line(screen, (0, 0, 0, 128), (0, y), (640, y))

        retroSnake.flipDisplay()

    def onEvent(self, event):
        if event.type == QUIT:
            retroSnake.quit()
            raise SystemExit
        else:
            self.state.onEvent(event)

    def nextState(self):
        if self.state == self.menu:
            self.state = self.game
        else:
            self.state = self.menu
        self.state.reset()

if __name__ == '__main__':
    retroSnake.init('Asteroids')
    if '--profile' in sys.argv:
        import cProfile
        cProfile.run('Asteroids().run()')
    else:
        Asteroids().run()
