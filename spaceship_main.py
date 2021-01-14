import sys
import pygame
import random   

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__()
        self.x_pos, self.y_pos = x_pos, y_pos
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos, y_pos))

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.screen_constrain()

    def screen_constrain(self):
        if self.rect.right >= 1280:
            self.rect.right = 1280
        elif self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 720:
            self.rect.bottom = 720

class Meteor(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, x_speed, y_speed):
        super().__init__()
        self.x_pos, self.y_pos = x_pos, y_pos
        self.x_speed, self.y_speed = x_speed, y_speed
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
 
    def update(self):
        self.x_pos = self.x_pos + self.x_speed
        self.y_pos = self.y_pos + self.y_speed
        self.rect.center = self.x_pos, self.y_pos
        #self.screen_constrain()

    def screen_constrain(self):
        if self.rect.right >= 1280:
            self.rect.right = 1280
        elif self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 720:
            self.rect.bottom = 720

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

spaceship = SpaceShip('spaceship.png', 640, 500, 10)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

meteor1 = Meteor('Meteor1.png', 400, -100, 1, 10)
meteor_group = pygame.sprite.Group()
meteor_group.add(meteor1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((42,45,51))
    #Meteors
    meteor_group.draw(screen)
    meteor_group.update()
    #Spaceship
    spaceship_group.draw(screen)
    spaceship_group.update()
    #Other
    pygame.display.update()
    clock.tick(120)
    