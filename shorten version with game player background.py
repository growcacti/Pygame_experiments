import pygame as pg
import os
import random
from constants import Constants


class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.dt = self.clock.tick(60) / 1000.0
        self.screen = pg.display.set_mode((Constants.W, Constants.H))
        self.player = Player(100, 100)
        self.background = ExpandingGalaxy(self.player)

    def run(self):
        while True:
            self.dt = self.clock.tick(60) / 1000.0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            self.player.handle_input()
            self.player.update(self.dt)
            self.background.update(self.player.camera)

            self.screen.fill((0, 0, 0))
            self.background.draw(self.screen)
            self.player.draw(self.screen)
            pg.display.flip()


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((32, 32))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pg.Vector2(x, y)
        self.velocity = pg.Vector2(0, 0)
        self.angle = 0

    def handle_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rotate_left()
        if keys[pg.K_RIGHT]:
            self.rotate_right()
        if keys[pg.K_UP]:
            self.accelerate()

    def update(self, dt):
        self.velocity *= 0.99  # Apply friction
        self.position += self.velocity * dt
        self.rect.center = self.position

    def rotate_left(self):
        self.angle += 5

    def rotate_right(self):
        self.angle -= 5

    def accelerate(self):
        acceleration = pg.Vector2(0, -0.1).rotate(-self.angle)
        self.velocity += acceleration

    def draw(self, surface):
        rotated_image = pg.transform.rotate(self.image, self.angle)
        rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, rect)


class ExpandingGalaxy:
    def __init__(self, player):
        self.player = player
        self.imagelist = self.load_images()
        self.bgdata = []
        self.stars = 200000

    @staticmethod
    def load_images():
        path = "gx/bg"
        filenames = [f for f in os.listdir(path) if f.endswith('.png')]
        imagelist = []
        for name in filenames:
            imagename = os.path.splitext(name)[0]
            imagelist.append(pg.image.load(os.path.join(path, name)).convert_alpha())
        return imagelist

    def coordinates(self, camx, camy, objw, objh):
        camrect = pg.Rect(camx, camy, Constants.W, Constants.H)
        while True:
            startx = int(camx) - Constants.W // 1
            stopx = int(camx) + Constants.W2 // 1
            starty = int(camy) - Constants.H // 1
            stopy = int(camy) + Constants.H2 // 1
            rx = random.randint(startx, stopx)
            ry = random.randint(starty, stopy)
            objrect = pg.Rect(rx, ry, objw, objh)
            if not objrect.colliderect(camrect):
                return rx, ry

    def add_bg(self, camx, camy):
        bg = {}
        bg['image'] = random.randint(0, len(self.imagelist) - 1)
        bg['width'] = self.imagelist[bg['image']].get_width()
        bg['height'] = self.imagelist[bg['image']].get_height()
        bg['x'], bg['y'] = self.coordinates(camx, camy, bg['width'], bg['height'])
        bg['rect'] = pg.Rect([bg['x'], bg['y'], bg['width'], bg['height']])
        return bg

    def boundaries(self, camx, camy, bg):
        bounds_left = camx - Constants.W
        bounds_top = camy - Constants.H
        boundsrect = pg.Rect(bounds_left, bounds_top, Constants.W2 * 2, Constants.H2 * 2)
        objrect = pg.Rect(bg['x'], bg['y'], bg['width'], bg['height'])
        return not boundsrect.colliderect(objrect)

    def update(self, cam):
        camx, camy = cam
        if len(self.bgdata) < self.stars:
            self.bgdata.append(self.add_bg(camx, camy))
        for bg in self.bgdata:
            mrect = pg.Rect((bg['x'] - camx, bg['y'] - camy, bg['width'], bg['height']))
            self.player.screen.blit(self.imagelist[bg['image']], mrect)

        for i in range(len(self.bgdata) - 1, -1, -1):
            if self.boundaries(camx, camy, self.bgdata[i]):
                del self.bgdata[i]


if __name__ == '__main__':
    game = Game()
    game.run()
