import pygame

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("First Game")
clock = pygame.time.Clock()

ground_y = 400
x, y = 200, ground_y
width, height = 40, 60
vel_x, vel_y = 5, 0
acc_y = 0

PLAYER_ACC = 15
PLAYER_GRAV = 1

run = True
while run:
    acc_y = PLAYER_GRAV
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                acc_y = -PLAYER_ACC
                vel_y = 0

    keys = pygame.key.get_pressed()
    x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * vel_x
    x = max(0, min(500 - width, x))

    vel_y += acc_y
    y += vel_y

    if y + height > ground_y:
        y = ground_y - height
        vel_y = 0
        acc_y = 0

    win.fill((0, 0, 0))
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
