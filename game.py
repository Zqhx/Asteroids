import pygame
from pygame.locals import *

import retroSnake

from ship import Ship
from asteroid import Asteroid

import random


class Game():
    def __init__(self, game):
        self.game = game

        self.ship = Ship()
        self.asteroidPool = [Asteroid() for i in xrange(5)]
        self.asteroids = []
        self.nextAsteroid = 0

        self.camera = retroSnake.Camera()
        self.camera.buildMatrix()
        self.pointer = retroSnake.Vector(0, 0)
        self.font = pygame.font.Font('assets/starcraft.ttf', 24)

        self.score = 0
        self.lives = 3
        self.isDead = False
        self.reset()

    def reset(self):
        self.score = 0
        self.lives = 3
        self.isDead = False

        for a in self.asteroids:
            self.asteroidPool.append(a)
            self.asteroids.remove(a)
        self.nextAsteroid = 0

    def update(self):
        self.ship.dead = self.isDead
        self.ship.update()

        if len(self.asteroidPool) != 0 and\
           self.nextAsteroid < pygame.time.get_ticks() and\
           not self.isDead:
            asteroid = self.asteroidPool.pop()
            asteroid.initialise()
            self.asteroids.append(asteroid)
            self.nextAsteroid = pygame.time.get_ticks() + 250

        if self.isDead and len(self.asteroids) == 0:
            self.isDead = False

        for asteroid in self.asteroids:
            if asteroid.update():
                self.asteroids.remove(asteroid)
                self.asteroidPool.append(asteroid)

        for asteroid in self.asteroids:
            s = self.ship.sprite.bound
            a = asteroid.sprite.bound

            if self.ship.shotOverlap(a):
                self.asteroids.remove(asteroid)
                self.asteroidPool.append(asteroid)
                self.score += 1
            elif (not self.isDead) and self.overlap(s, a) and realClip(s, a):
                self.lives -= 1
                self.isDead = True
                self.ship.reset()
                if self.lives == 0:
                    self.game.nextState()

    def render(self, screen):
        if not self.isDead:
            self.ship.render(screen, self.camera.transform)
        for asteroid in self.asteroids:
            asteroid.render(screen, self.camera.transform)
        screen.blit(
            retroSnake.printf(self.font, (0, 255, 0), 'score: %d', self.score),
            (0, 50)
        )
        screen.blit(
            retroSnake.printf(self.font, (0, 255, 0), 'lives: %d', self.lives),
            (0, 100)
        )

    def onEvent(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.game.nextState()
        if event.type == MOUSEMOTION:
            self.pointer = self.camera.unproject(
                retroSnake.Vector(*pygame.mouse.get_pos())
                )

    def overlap(self, a, b):
        retVal = True and not a[1] < b[0]
        retVal = retVal and not a[0] > b[1]
        retVal = retVal and not a[3] < b[2]
        retVal = retVal and not a[2] > b[3]

        return retVal


def realClip(a, b):
    # Actually use the clipping data, not just bounds.
    return True
