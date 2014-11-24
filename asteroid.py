import math

import pygame
from pygame.locals import *

import retroSnake


class Asteroid(retroSnake.Entity):
    def __init__(self):
        super(Asteroid, self).__init__()

        self.sprite = retroSnake.loadSprite('asteroid')

        self.v0 = retroSnake.Vector(0, 0)

        self.angle = 0
        self.location = retroSnake.Vector(0, 15000)
        self.velocity = self.v0
        self.sprite.doTransform(retroSnake.ScaleMatrix(3))
        self.cBound = False
        self.inPlay = False
        self.sprite.calculateTransform(True)
        self.sprite.calculateBounds()

    def initialise(self):
        self.sprite.transform = retroSnake.RotateMatrix(self.angle)
        self.sprite.doTransform(retroSnake.ScaleMatrix(3))
        self.sprite.calculateTransform(True)
        self.sprite.calculateBounds()
        self.inPlay = False

        camera = retroSnake.game.game.camera
        cMin = camera.unproject(retroSnake.Vector(0, 0))
        cMax = camera.unproject(retroSnake.Vector(640, 480))
        self.cBound = [
            cMin.getX(), cMax.getX(),
            cMin.getY(), cMin.getY()
        ]

        internal = camera.unproject(
            retroSnake.Vector(
                retroSnake.rand(80, 560),
                retroSnake.rand(80, 400)
            )
        )
        a, d = retroSnake.rand(0, 360), 700
        p = retroSnake.RotateMatrix(a)*retroSnake.Vector(0, d)
        external = camera.unproject(p)
        self.location = external

        self.velocity = (internal-external)*.0025

        self.update()
        self.sprite.calculateTransform(True)
        self.sprite.calculateBounds(self.transform)

    def update(self):
        self.location += self.velocity
        self.transform = retroSnake.TranslateMatrix(self.location)
        self.sprite.update()  # Note: Copy pasta 'cos super hates me.

        x, y = self.location.getX(), self.location.getY()
        if self.inPlay:
            if -26.7 < x < 26.7:
                pass
            else:
                return True
            if -20 < y < 20:
                pass
            else:
                return True
        else:
            if -26.7 < x < 26.7 and -20 < y < 20:
                self.inPlay = True
