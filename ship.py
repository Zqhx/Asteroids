import math

import pygame
from pygame.locals import *

import retroSnake
from bullet import Bullet


class Ship(retroSnake.Entity):
    def __init__(self):
        super(Ship, self).__init__()

        self.sprite = retroSnake.loadSprite('ship')

        self.bulletPool = [Bullet() for i in xrange(10)]
        self.bullets = []
        self.nextBullet = 0

        self.v0 = retroSnake.Vector(0, 0)

        self.angle = 0
        self.rotSpeed = .25
        self.drag = .025
        self.accel = retroSnake.Vector(0, -.1)
        self.location = self.v0
        self.velocity = self.v0
        self.checkInput = 0
        self.cBound = False
        self.reset()

    def reset(self):
        self.angle = 0
        self.location = self.v0
        self.velocity = self.v0
        self.sprite.transform = retroSnake.RotateMatrix(self.angle)
        self.sprite.calculateTransform(True)
        self.sprite.calculateBounds()

    def update(self):
        if not self.cBound:
            self.setup()
        self.checkInput += 1
        needUpdate = False

        if self.checkInput >= 2 and not self.dead:
            self.checkInput = 0

            keys = pygame.key.get_pressed()
            if keys[K_a]:
                self.angle -= self.rotSpeed
                needUpdate = True
            elif keys[K_d]:
                self.angle += self.rotSpeed
                needUpdate = True

            if keys[K_w]:
                self.accelerate()
            if keys[K_SPACE]:
                if len(self.bulletPool) != 0 and\
                   self.nextBullet < pygame.time.get_ticks():
                    bullet = self.bulletPool.pop()
                    bullet.location = self.location
                    bullet.velocity = self.velocity
                    bullet.angle = self.angle
                    bullet.initialise()
                    self.bullets.append(bullet)
                    self.nextBullet = pygame.time.get_ticks() + 250

        if needUpdate:
            self.sprite.transform = retroSnake.RotateMatrix(self.angle)
            self.sprite.calculateTransform(True)
            self.sprite.calculateBounds()

        self.applyDrag()
        self.location += self.velocity
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
        self.transform = retroSnake.TranslateMatrix(self.location)
        self.sprite.update()  # Note: Copy pasta 'cos super hates me.

        for bullet in self.bullets:
            if bullet.update():
                self.bullets.remove(bullet)
                self.bulletPool.append(bullet)

    def applyDrag(self):
        x, y = self.velocity.data[:2]
        fx, fy = math.fabs(x), math.fabs(y)

        if fx < self.drag:
            dx = x
        else:
            dx = (self.velocity.normalised()*self.drag).data[0]

        if fy < self.drag:
            dy = y
        else:
            dy = (self.velocity.normalised()*self.drag).data[1]

        self.velocity -= retroSnake.Vector(dx, dy)

    def accelerate(self):
        self.velocity += self.sprite.transform*self.accel

    def render(self, dest, transform):
        self.sprite.render(dest, self.transform, transform)
        for bullet in self.bullets:
            bullet.render(dest, transform)

    def shotOverlap(self, a):
        for bullet in self.bullets:
            if bullet.overlap(a):
                return True
        return False

    def setup(self):
        camera = retroSnake.game.game.camera
        cMin = camera.unproject(retroSnake.Vector(0, 0))
        cMax = camera.unproject(retroSnake.Vector(640, 480))
        self.cBound = [
            cMin.getX(), cMax.getX(),
            cMin.getY(), cMin.getY()
        ]
