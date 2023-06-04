import pygame
from pygame.locals import *
import os
import random
import time
pygame.init()
W, Height = 800, 640

screen = pygame.display.set_mode((W,Height))

SCREEN_SIZE = pygame.Rect((0,0,W,Height))
TILE_SIZE = 48

t0 = time.time()
font = pygame.font.SysFont(None, 24)
print("Time needed to create fonts: " + str(time.time() - t0))

vec = pygame.math.Vector2

# USER CAN MODIFY
ACC = 0.5
FRIC = -0.12
FPS = 60

clock = pygame.time.Clock()

class BlueBlock(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super(BlueBlock, self).__init__()
    self.surf = pygame.Surface((48,48))
    self.surf.fill((0,191,255))
    self.rect = self.surf.get_rect()
    self.original_surface = self.surf
    self.hover_surface = self.original_surface.copy()
    pygame.draw.rect(self.hover_surface, (255, 255, 0), self.hover_surface.get_rect(), 6)
    self.surf = self.original_surface
    self.rect = self.surf.get_rect(center = (x, y))
    self.hover = False
    self.mouse_pos = None
    self.count = 0
    
  def update(self):
    if player.mode == "build":
      mouse_pos = pygame.mouse.get_pos()
      self.hover = self.rect.collidepoint(mouse_pos)
      self.surf = self.hover_surface if self.hover else self.original_surface
      if self.hover and mouse_pos == self.mouse_pos:
        self.count += 1
      if self.count > 10:
        self.image = pygame.Surface((48,48))
        self.image.fill((255,255,255))

class textureblock(pygame.sprite.Sprite):
  def __init__(self, imagefile, x, y, type):
    super(textureblock, self).__init__()
      
    self.imagefile = imagefile
    self.original_image = pygame.image.load(imagefile).convert_alpha()
    self.original_image = pygame.transform.scale(self.original_image, (48,48))
    self.hover_image = self.original_image.copy()
    pygame.draw.rect(self.hover_image, (255, 255, 0), self.hover_image.get_rect(), 6)
    self.image = self.original_image 
    self.rect = self.image.get_rect(center = (x, y))
    self.hover = False
    self.mouse_pos = None
    self.count = 0
    self.type = type

  def update(self):
    if player.mode == "build":
      pygame.draw.rect(self.hover_image, (255,0,0), self.hover_image.get_rect(), 6)
    elif player.mode == "destroy":
      pygame.draw.rect(self.hover_image, (255, 255,0), self.hover_image.get_rect(), 6)
    mouse_pos = pygame.mouse.get_pos()
    self.hover = self.rect.collidepoint(mouse_pos)
    self.image = self.hover_image if self.hover else self.original_image
    if self.hover and mouse_pos == self.mouse_pos and player.mode == "destroy":
      self.count += 1
      if self.count > 10:
        self.image = pygame.Surface((48,48))
        self.image.fill((0,191,255))

        item = Item(self.imagefile, self.rect.x, self.rect.y, self.type)
        
        items.add(item)
        self.remove(blocks)
      
    else:
      self.count = 0
    self.mouse_pos = mouse_pos
  
class Player(pygame.sprite.Sprite):
  def __init__(self):
    super(Player, self).__init__()
    self.surf = pygame.Surface((40,40))
    self.surf.fill((255,0,0))
    self.rect = self.surf.get_rect()
    self.pos = vec(0,144) # Position
    self.vel = vec(0,0) # Velocity
    self.acc = vec(0,0) # Acceleration 
    self.inventory = {} # Items can be added
    self.mode = "destroy" # Mode. Probably will be changed later
    self.selected_item = None # Selected item

  def move(self, pressed_keys):
    self.acc = vec(0,0.5)
    if pressed_keys[K_LEFT]:
      self.acc.x = -ACC
      
    if pressed_keys[K_RIGHT]:
      self.acc.x = ACC
    
    self.acc.x += self.vel.x * FRIC
    self.vel += self.acc
    self.pos.x += self.vel.x + 0.5 * self.acc.x
    self.rect.midbottom = self.pos

    hit_side = False
    for entity in blocks:
        if self.rect.colliderect(entity.rect):

            # move left and hit the block on the right
            if self.vel.x < 0 and self.rect.right > entity.rect.right:
                self.rect.left = entity.rect.right
                self.pos.x = self.rect.centerx
                hit_side = True

            # move right and hit the block on the left
            if self.vel.x > 0 and self.rect.left < entity.rect.left:
                self.rect.right = entity.rect.left
                self.pos.x = self.rect.centerx
                hit_side = True

    if hit_side:
        self.vel.x = 0
        self.acc.x = 0

  def update(self):
    self.acc = vec(0,0.5)
    if pressed_keys[K_LEFT]:
      self.acc.x = -ACC
      
    if pressed_keys[K_RIGHT]:
      self.acc.x = ACC
    
    self.acc.x += self.vel.x * FRIC
    self.vel += self.acc
    self.pos.x += self.vel.x + 0.5 * self.acc.x
    self.rect.midbottom = self.pos

    hit_side = False
    for entity in blocks:
        if self.rect.colliderect(entity.rect):

            # move left and hit the block on the right
            if self.vel.x < 0 and self.rect.right > entity.rect.right:
                self.rect.left = entity.rect.right
                self.pos.x = self.rect.centerx
                hit_side = True

            # move right and hit the block on the left
            if self.vel.x > 0 and self.rect.left < entity.rect.left:
                self.rect.right = entity.rect.left
                self.pos.x = self.rect.centerx
                hit_side = True

    if hit_side:
        self.vel.x = 0
        self.acc.x = 0
    hits = pygame.sprite.spritecollide(self, blocks, False)

    self.pos.y += self.vel.y + 0.5 * self.acc.y
    self.rect.midbottom = self.pos

    for entity in blocks:
        if self.rect.colliderect(entity.rect):
            if self.vel.y > 0:
                self.rect.bottom = entity.rect.top
                self.pos.y = self.rect.bottom
                self.vel.y = 0
    if self.vel.y > 0:
      if hits: 
        self.pos.y = hits[0].rect.top + 1
        self.vel.y = 0

  def jump(self):
    self.vel.y = -15

# Item class - Spawned when a player breaks a block.
class Item(pygame.sprite.Sprite):
  def __init__(self, image, x, y, type):
    super(Item, self).__init__()
    self.image = pygame.image.load(image).convert_alpha()
    self.image = pygame.transform.scale(self.image, (24,24))
    self.rect = self.image.get_rect()
    
    self.pos = vec(x, y)
    self.vel = vec(0,0)
    self.acc = vec(0,0)
    self.type = type

  def move(self):
    self.acc = vec(0,0.5)
    
    self.acc.x += self.vel.x * FRIC
    self.vel += self.acc
    self.pos.x += self.vel.x + 0.5 * self.acc.x
    self.rect.midbottom = self.pos

    hit_side = False
    for entity in blocks:
        if self.rect.colliderect(entity.rect):

            # move left and hit the block on the right
            if self.vel.x < 0 and self.rect.right > entity.rect.right:
                self.rect.left = entity.rect.right
                self.pos.x = self.rect.centerx
                hit_side = True

            # move right and hit the block on the left
            if self.vel.x > 0 and self.rect.left < entity.rect.left:
                self.rect.right = entity.rect.left
                self.pos.x = self.rect.centerx
                hit_side = True

    if hit_side:
        self.vel.x = 0
        self.acc.x = 0

  def update(self):
    hits = pygame.sprite.spritecollide(self, blocks, False)

    self.pos.y += self.vel.y + 0.5 * self.acc.y
    self.rect.midbottom = self.pos

    for entity in blocks:
        if self.rect.colliderect(entity.rect):
            if self.vel.y > 0:
                self.rect.bottom = entity.rect.top
                self.pos.y = self.rect.bottom
                self.vel.y = 0
    if self.vel.y > 0:
      if hits: 
        self.pos.y = hits[0].rect.top + 1
        self.vel.y = 0

    # Now we check if we hit the Player
    if self.rect.colliderect(player.rect):
      # Attempt to check the player inventory
      if self.type not in player.inventory.keys():
        
        player.inventory[self.type] = 1
        self.kill()
      else:
        
        player.inventory.update({self.type: player.inventory.get(self.type) + 1})
        self.kill()
       
player = Player()
blueblock = BlueBlock(0,0)

running = True

all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
items = pygame.sprite.Group()
miscBlocks = pygame.sprite.Group()

def drawGraph(graph, start):
  y = start
  x = 0
  for item in graph:
    if item == "O":
      spr = BlueBlock(x, y)
      spr.rect.x = x
      spr.rect.y = y
      all_sprites.add(spr)
      miscBlocks.add(spr)
      screen.blit(spr.surf, spr.rect)
      x += 48
    elif item == "G":
      spr = textureblock("media/Grass.jpeg", x, y, "Grass")
      spr.rect.x = x
      spr.rect.y = y
      all_sprites.add(spr)
      blocks.add(spr)
      screen.blit(spr.image, spr.rect)
      x += 48
      
    elif item == "S":
      spr = textureblock("media/Stone.png",x,y, "Stone")
      spr.rect.x = x
      spr.rect.y = y
      all_sprites.add(spr)
      blocks.add(spr)
      screen.blit(spr.image, spr.rect)
      x += 48
    elif item == "C":
      spr = textureblock("media/Coal.jpeg",x,y, "Coal")
      spr.rect.x = x
      spr.rect.y = y
      all_sprites.add(spr)
      blocks.add(spr)
      screen.blit(spr.image, spr.rect)
      x += 48
    elif item == "NL":
      y += 48
      x = 0
    else:
      print("Item not found: " + item)
  print("[Debug] Generation finished. Amount of blocks: " + str(len(blocks.sprites())))

def randomGen(graph):
  print("[Debug] Begin randomGen...")
  # We assume the user has not done anything with the graph, so we add the sky and grass
  for i in range(20):
    newgraph.append('O')
  newgraph.append('NL')
  
  for i in range(20):
    newgraph.append('O')
  newgraph.append('NL')
  for i in range(20):
    newgraph.append('O')
  newgraph.append('NL')
  for i in range(20):
    newgraph.append('O')
  newgraph.append('NL')
  for i in range(20):
    newgraph.append('O')
  newgraph.append('NL')
  for i in range(20):
    newgraph.append('G')
  newgraph.append('NL')

  # Next begins the random ore gen
  
  for i in range(20):
    x = 0
    for i in range(20):
      # Chance of coal - 1 in 15
      iscoal = random.randint(1,15)
      
      if iscoal == 6:
        graph.append("C")
       
      else:
        graph.append("S")
      x += 48
    graph.append('NL')
  print("[Debug] randomGen finished. Block Stats: %s air blocks, %s grass blocks, %s stone blocks, %s coal blocks, and %s newlines." % (str(graph.count('O')), str(graph.count('G')), str(graph.count('S')), str(graph.count('C')), str(graph.count('NL'))))

newgraph = []
randomGen(newgraph)

all_sprites.add(player)

def update():
  for entity in all_sprites:
    try:
      screen.blit(entity.surf, entity.rect)
    except:
      screen.blit(entity.image, entity.rect)
  screen.blit(player.surf, player.rect)
  for entity in blocks:
    screen.blit(entity.image, entity.rect)
  for entity in items:
    screen.blit(entity.image, entity.rect)
  pygame.display.update()

drawGraph(newgraph, 0)

# Calculate the size of the level
level_width = 0
for i in newgraph:
  if i != "NL":
    level_width += 1
  elif i == "NL":
    break
level_width = level_width * TILE_SIZE

level_height = (newgraph.count("NL")-1)*TILE_SIZE

print("[Debug] Calculated level width and height: %s and %s" % (str(level_width), str(level_height)))

while running:
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        player.jump()
      if event.key == pygame.K_ESCAPE:
        running = False
        pygame.quit()
      if event.key == pygame.K_e:
        if len(player.inventory) == 0:
          print("Player Inventory: Empty")
        else:
          print("Player Inventory: " + str(player.inventory).replace("{", "").replace("}","").replace(":", " x").replace("'",""))
      if event.key == pygame.K_b:
        if player.mode == "build":
          player.mode = "destroy"
        elif player.mode == "destroy":
          player.mode = "build"
        print("Changed player mode to " + player.mode)
      if event.key == pygame.K_1:
        
        player.selected_item = list(player.inventory)[0]
        print("Item: " + list(player.inventory)[0])
    if event.type == pygame.MOUSEBUTTONDOWN:
      x,y = event.pos
    if event.type == pygame.QUIT:
      running = False
      pygame.quit()
      
  miscBlocks.update()
  blocks.update()
  blocks.draw(screen)
  
  pressed_keys = pygame.key.get_pressed()
  for entity in items:
    entity.move()
  # Commented out because it lagged everything.

  items.update()
  player.update()
  update()
  
  img1 = font.render("FPS: " + str(clock.get_fps()), True, (255,255,0))
  img2 = font.render("Mode: " + player.mode, True, (255,0,0))
  try:
    img3 = font.render("Selected Item: " + player.selected_item, True, (0,255,0))
  except Exception:
    img3 = font.render("Selected Item: None", True, (0,255,0))

  screen.blit(img1, (0,0))
  screen.blit(img2, (0,24))
  screen.blit(img3, (0,48))
  
  pygame.display.update()
  clock.tick(60)
