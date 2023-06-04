import pygame
import uuid
import client.renderCycle as renderCycle

class sprite(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], size: tuple[int, int], image: str):

        super().__init__()

        self.rect = pygame.Rect(position, size)
        self.size = size
        
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, size)

        self.id = str(uuid.uuid4())

        self.position = pygame.Vector2(position[0], position[1])
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)

        self.ignoreCollisionsWith = []

    def setVelocity(self, v: pygame.Vector2) -> None:
        self.velocity = v

    def setAcceleration(self, a: pygame.Vector2):
        self.acceleration = a


    def draw(self):
        print('drawing', self.rect)
        renderCycle.getScreen().blit(self.image, self.rect)

    def getRectPoints(self):
        return (pygame.Vector2(self.rect.topleft), pygame.Vector2(self.rect.topright), pygame.Vector2(self.rect.bottomleft), pygame.Vector2(self.rect.bottomright))

    def checkCollision(self, nextP: pygame.Vector2, s1):
        return pygame.Rect(nextP, self.size).colliderect(s1.rect)

    def update(self, allSpriteGroups: dict[str, pygame.sprite.Group]):

        target = self.position + (self.velocity + self.acceleration)

        self.acceleration = pygame.Vector2(0, 0)

        doesPass = True

        for group in allSpriteGroups.values():
            for sprite in group:
                if sprite.id in self.ignoreCollisionsWith or sprite == self:
                    continue

                check = self.checkCollision(target, sprite)
                if check:
                    doesPass = False
            if not doesPass:
                break

        if doesPass:
            self.position = target
            self.rect = pygame.Rect(self.position, self.size)

        pygame.sprite.Sprite.update(self)

    def delete(self):
        renderCycle.removeTaskFromRenderCycle(self.id)
        pass
