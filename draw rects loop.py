import pygame as pg
import sys




pg .init()


screen = pg.display.set_mode((1200,800))

    




while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()





def drawStyleRect(surface):
    pg.draw.rect(surface, (0,0,255), (x,y,150,150), 0)
    for i in range(4):
        pg.draw.rect(surface, (0,0,0), (x-i,y-i,155,155), 1)
        screen.blit(surface, rect)



def create_rect(width, height, border, color, border_color):
    surf = pygame.Surface((width+border*2, height+border*2), pygame.SRCALPHA)
    pygame.draw.rect(surf, color, (border, border, width, height), 0)
    for i in range(1, border):
        pygame.draw.rect(surf, border_color, (border-i, border-i, width+5, height+5), 1)
    return surf

rect_surf1 = create_rect(150, 150, 5, (0, 0, 255), (0, 0, 0))
# [...]

run = True
while run:

    # [...]
    drawStyleRect(screen)
    screen.blit(rect_surf1, (x, y))

    # [...]

pg.display.update()

        
