import pygame
pygame.init()

WIDTH = 540
TILESIZE = 60
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREY = (211, 211, 211)
GREEN = (0, 255, 0)


win = pygame.display.set_mode((WIDTH+1, WIDTH+1))
win.fill(GREY)
surface = pygame.Surface((TILESIZE-1, TILESIZE-1))
surface.fill(RED)

def mouse_pos():
    surface_place = (1, 1)
    for x in range(0, 9, TILESIZE):
        for y in range(x):
            surface_place = list(surface_place)
            surface_place[0] += TILESIZE
            surface_place[1] += TILESIZE
            surface_place = tuple(surface_place)
            win.blit(surface, surface_place)

    if surface.get_rect().collidepoint(pygame.mouse.get_pos()):
        win.blit(surface, surface_place)
        surface.fill(GREEN)
    else:
        win.blit(surface, surface_place)
        surface.fill(RED)

def draw_grid():
    for x in range(0, WIDTH+1, TILESIZE):
        pygame.draw.line(win, BLACK, (x, 0), (x, WIDTH))
    for y in range(0, WIDTH+1, TILESIZE):
        pygame.draw.line(win, BLACK, (0, y), (WIDTH, y))

clicked = False
while not clicked:
    draw_grid()
    mouse_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            clicked = True

    pygame.display.update()
