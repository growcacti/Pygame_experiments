import pygame as pg
import math
from math import tan, copysign, pi, hypot, cos, sin, atan2, degrees, radians
from pygame.math import Vector2
from constants import Constants
import get_info

con = Constants
screen = con.screen
WIDTH = con.WIDTH
HEIGHT = con.HEIGHT
W = con.W
H = con.H
CW = W // 2
CH = H // 2
W2 = W * 2
H2 = H * 2


class Player(pg.sprite.Sprite):
    def __init__(self, x=CW, y=CH, angle=0.0, length=4, max_rotation=10, max_acceleration=5.0, *groups):
        super().__init__(*groups)
        self.image = pg.image.load("gx/ships/51.png").convert_alpha()
        self.rect = pg.Rect(self.image.get_rect(center=(x, y)))
        self.orig_image = pg.image.load("gx/ships/51.png").convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.size = self.image.get_size()

        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = 20
        self.max_rotation = max_rotation
        self.max_velocity = 20
        self.thrust = 25
        self.sim_inertia = 0.05
        self.font = pg.font.Font(None, 20)
        self.acceleration = 0.5
        self.rotation = 0.0
        self.background = Vector2(self.position)
        self.camera = Vector2(0, 0)
        self.cam = self.camera
        self.x = x
        self.y = y
        self.cam.x, self.cam.y = self.cam
        self.revcam = Vector2(0, 0)
        self.subcam = Vector2(0, 0)
        self.invcam = Vector2(0, 0)
        self.extcam = Vector2(0, 0)
        self.extcam1 = Vector2(1000, 1000)
        self.extcam2 = Vector2(5000, 5000)
        self.extcam3 = Vector2(10000, 10000)
        self.extcam4 = Vector2(50000, 50000)
        self.extcam5 = Vector2(2000, 2000)
        self.extcam6 = Vector2(100, 100)
        self.fcam = Vector2(0, 0)
        self.direction = Vector2(0, 0)
        self.warp = 0
        self.camrect = pg.Rect(self.cam.x, self.cam.y, W, H)
        self.fuel = 900000
        self.shields = 100
        self.hitcount = 0
        self.mask = pg.mask.from_surface(self.image)

    def update(self, dt, warp=0):
        con = Constants
        self.warp = warp

        if self.warp == 0:
            self.max_velocity = 20
            self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
            self.velocity.y = max(-self.max_velocity, min(self.velocity.y, self.max_velocity))
            self.velocity += (self.acceleration * dt, 0)
            self.fuel -= 1
        elif self.warp.
