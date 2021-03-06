import sys
import pygame
import random   

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.x_pos, self.y_pos = x_pos, y_pos

        self.uncharged = pygame.image.load(path)
        self.charged = pygame.image.load('spaceship_charged.png')

        self.image = self.uncharged
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        self.sheild_surface = pygame.image.load('shield.png')
        self.health = 5

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.screen_constrain()
        self.display_health()

    def screen_constrain(self):
        if self.rect.right >= 1280:
            self.rect.right = 1280
        elif self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 720:
            self.rect.bottom = 720

    def display_health(self):
        for index, shield in enumerate(range(self.health)):
            screen.blit(self.sheild_surface, (10 + index * 40, 10))

    def get_damage(self, damage_amount):
        self.health -= damage_amount
    
    def charge(self):
        self.image = self.charged
    
    def discharge(self):
        self.image = self.uncharged

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

        if self.rect.centery >= 800:
            self.kill()
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


class Laser(pygame.sprite.Sprite):
    def __init__(self, path, pos, speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed

    def update(self):
        self.rect.centery -= self.speed
        if self.rect.centery <= -100:
            self.kill()
            


def main_game():
    global laser_active
    meteor_score = 0
    laser_group.draw(screen)
    laser_group.update()
    #Meteors
    meteor_group.draw(screen)
    meteor_group.update()
    #Spaceship
    spaceship_group.draw(screen)
    spaceship_group.update()
    #collide
    if pygame.sprite.spritecollide(spaceship_group.sprite, meteor_group, True):
        spaceship_group.sprite.get_damage(1)
        impact.play()

    for laser in laser_group:
        if pygame.sprite.spritecollide(laser, meteor_group, True):
            meteor_score = 1
            explode.play()
        
    #laser timer
    if pygame.time.get_ticks() - laser_timer >= 1000:
        laser_active = True
        spaceship_group.sprite.charge()
    
    return 1, meteor_score

def end_game():
    text_surface = game_font.render('Game Over', True, (5, 254, 0))
    text_rect = text_surface.get_rect(center = (640, 300))
    screen.blit(text_surface, text_rect)

    score_surface = score_font.render(f'score: {score}', True, (5, 254, 0))
    score_rect = score_surface.get_rect(center = (640, 380))
    screen.blit(score_surface, score_rect)
    

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont('Goudy Stout', 90)
score_font = pygame.font.SysFont('Goudy Stout', 60)
meteor_score_font = pygame.font.SysFont('Goudy Stout', 20)
score = 0
meteor_score2 = 0
laser_timer = 0
laser_active = False

spaceship = SpaceShip('spaceship.png', 640, 500)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

meteor_group = pygame.sprite.Group()
METEOR_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT, 100)

laser_group = pygame.sprite.Group()
game_active = True

#sounds
lasershoot = pygame.mixer.Sound('Laser Blasts-SoundBible.com-108608437.mp3')
explode = pygame.mixer.Sound('Bomb-SoundBible.com-891110113.mp3')
impact = pygame.mixer.Sound('Light Bulb Breaking-SoundBible.com-53066515.mp3')
game_over = pygame.mixer.Sound('Sad_Trombone-Joe_Lamb-665429450.mp3')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == METEOR_EVENT:
            meteor_path = random.choice(('Meteor1.png', 'Meteor2.png', 'Meteor3.png')) 
            random_x_pos = random.randrange(0, 1280)
            random_y_pos = random.randrange(-500, -50)
            random_x_speed = random.randrange(-1, 1)
            random_y_speed = random.randrange(4, 10)
            meteor = Meteor(meteor_path, random_x_pos, random_y_pos, random_x_speed, random_y_speed)
            meteor_group.add(meteor)

        if event.type == pygame.MOUSEBUTTONDOWN and laser_active:
            new_laser = Laser('laser.png', event.pos, 15)
            laser_group.add(new_laser)
            laser_timer = pygame.time.get_ticks()
            laser_active = False
            spaceship_group.sprite.discharge()
            lasershoot.play()

        if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.health <= 0:
            spaceship_group.sprite.health = 5
            meteor_group.empty()
            score = 0
            meteor_score2 = 0
            game_active = True
    

    screen.fill((42,45,51))
    if spaceship_group.sprite.health > 0:
        score_temp, meteor_score2_temp = main_game()
        score += score_temp
        if meteor_score2_temp > 0:
            meteor_score2 += meteor_score2_temp 
        meteor_score_surface = meteor_score_font.render(f'meteors hit: {meteor_score2}', True, (250, 250, 250))
        meteor_score_rect = meteor_score_surface.get_rect(center = (850, 20))
        screen.blit(meteor_score_surface, meteor_score_rect) 

        score_surface = meteor_score_font.render(f'score: {score}', True, (250, 250, 250))
        score_rect = score_surface.get_rect(center = (1150, 20))
        screen.blit(score_surface, score_rect) 
        
    else:
        end_game()
        if game_active:
            game_over.play()
            game_active = False

    #Other
    pygame.display.update()
    clock.tick(120)
    