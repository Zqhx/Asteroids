import math

import pygame
from pygame.locals import *

import retroSnake


class Bullet(retroSnake.Entity):
    def __init__(self):
        super(Bullet, self).__init__()

        self.sprite = retroSnake.loadSprite('bullet')

        self.v0 = retroSnake.Vector(0, 0)

        self.angle = 0
        self.location = self.v0
        self.velocity = self.v0
        self.time = 0

    def initialise(self):
        bSpeed = retroSnake.Vector(0, -.5)
        self.sprite.transform = retroSnake.RotateMatrix(self.angle)
        self.sprite.calculateTransform(True)
        self.sprite.calculateBounds()
        self.velocity += retroSnake.RotateMatrix(self.angle)*bSpeed
        self.time = pygame.time.get_ticks() + 1500

        camera = retroSnake.game.game.camera
        cMin = camera.unproject(retroSnake.Vector(0, 0))
        cMax = camera.unproject(retroSnake.Vector(640, 480))
        self.cBound = [
            cMin.getX(), cMax.getX(),
            cMin.getY(), cMin.getY()
        ]

    def update(self):
        self.location += self.velocity
        self.transform = retroSnake.TranslateMatrix(self.location)
        self.sprite.update()  # Note: Copy pasta 'cos super hates me.

        x, y = self.location.getX(), self.location.getY()
        if -26.7 < x < 26.7:
            pass
        else:
            x *= -1
        if -20 < y < 20:
            pass
        else:
            y *= -1
        self.location = retroSnake.Vector(x, y)

        if pygame.time.get_ticks() > self.time:
            return True
        else:
            return False

    def render(self, dest, transform):
        self.sprite.render(dest, self.transform, transform)

    def overlap(self, b):
        a = self.sprite.bound
        retVal = True and not a[1] < b[0]
        retVal = retVal and not a[0] > b[1]
        retVal = retVal and not a[3] < b[2]
        retVal = retVal and not a[2] > b[3]

        return retVal
