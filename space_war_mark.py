# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1000
HEIGHT = 1000
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)


# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 96)


# Images
ship_img = pygame.image.load('assets/images/player.png').convert_alpha()
laser_img = pygame.image.load('assets/images/laserRed.png').convert_alpha()
enemy_img = pygame.image.load('assets/images/Tie_Fighter.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/laserGreen.png').convert_alpha()
shield_img = pygame.image.load('assets/images/shield.png').convert_alpha()
star_Background_img = pygame.image.load('assets/images/Background/starBackground.png').convert_alpha()
star_Background_img = pygame.transform.scale(star_Background_img, (1000,1000))

# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
SHOOT = pygame.mixer.Sound("assets/sounds/shoot.wav")

# Stages
START = 0
PLAYING = 1
END = 2
PAUSE = 4

#Shield
health = 3
global hits
meter = [0,25,99,50]
hit1 = [0,25,33.33,50]
hit2 = [33.33,25,33.33,50]
hit3 = [66.66,25,33.33,50]
meters = [meter]
hits = [hit1,hit2,hit3]

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5
        self.is_alive = True

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        SHOOT.play()
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        laser.add(lasers)



    def update(self):
        '''Edge detection'''
        if self.rect.left <0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        '''killing ship'''
        hit_list = pygame.sprite.spritecollide(self,bombs,True,pygame.sprite.collide_mask)
        hit_list1 = pygame.sprite.spritecollide(self,mobs,False,pygame.sprite.collide_mask)

        if len(hit_list) or len(hit_list1) > 0:
            EXPLOSION.play()
            self.is_alive = False
            self.kill()



class Shield(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.health = 3

    def update(self):
        global hits
        self.rect.x = ship.rect.x - 25
        self.rect.y = HEIGHT - 100

        hit_list = pygame.sprite.spritecollide(self,bombs,True)
        hit_list1 = pygame.sprite.spritecollide(self,mobs,False,)

        for hit in hit_list:
            self.health -= 1
            del hits[-1]

        if len(hit_list1) > 0:
            self.kill()

        if self.health == 0:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


        self.speed = 10

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self):
        hit_list = pygame.sprite.spritecollide(self,lasers,True,pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            EXPLOSION.play()
            self.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        SHOOT.play()
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.image)



    def update(self):
        self.rect.y += self.speed

        if self.rect.bottom > HEIGHT:
            self.kill()

class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 5
        self.moving_right = True
        self.moving_down = True
        self.drop_speed = 10
        self.bomb_rate = 60


    def move(self):
        hits_egde = False
        hits_bottom = False
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_egde = True
            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_egde = True

        if hits_egde:
            self.reverse()
            self.move_down()

        if hits_bottom:
            self.move_up()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop_speed

    def move_up(self):
        self.moving_down = not self.moving_down
        for m in mobs:
            m.rect.y -= self.drop_speed

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()

    def update(self):
        self.move()
        self.choose_bomber()


# Game helper functions
def show_title_screen():
    title_text = FONT_XL.render("Space War!", 1, WHITE)
    screen.blit(title_text, [WIDTH/3 - 130, HEIGHT/2 - 100])

def show_end_screen_1():
    end_text = FONT_XL.render("You died!",1,WHITE)
    end_text2 = FONT_MD.render("Press space to restart", 1, WHITE)
    screen.blit(end_text, [WIDTH/3 - 90, HEIGHT/2 - 100])
    screen.blit(end_text2, [WIDTH/3 +50 , HEIGHT/2 + 65])

def show_end_screen_2():
    end_text = FONT_XL.render("You won!!",1,WHITE)
    end_text2 = FONT_MD.render("Press space to restart", 1, WHITE)
    screen.blit(end_text, [WIDTH/3 - 90, HEIGHT/2 - 100])
    screen.blit(end_text2,[WIDTH/3 + 50, HEIGHT/2 + 65])

def show_stats():
    if shield.health >= 0:
        shield_text = FONT_LG.render(str(shield.health), 1, WHITE)
        screen.blit(shield_text, [10,10])

def show_pause():
    pause_text = FONT_XL.render("Paused",1, WHITE)
    pause_text2 = FONT_LG.render("Press P to unpause", 1, WHITE)
    screen.blit(pause_text, [WIDTH/3 - 30, HEIGHT/2 - 100])
    screen.blit(pause_text2, [WIDTH/3 - 35, HEIGHT/2 + 65])

def setup():
    global stage, done
    global player,ship, lasers , mobs , fleet , bombs , shield

    ''' Make game objects '''
    ship = Ship(ship_img)
    ship.rect.centerx = WIDTH / 2
    ship.rect.bottom = HEIGHT
    shield = Shield(shield_img)
    shield.rect.x = ship.rect.x - 25
    shield.rect.y = HEIGHT - 100

    ''' Make sprite groups '''
    player = pygame.sprite.Group()
    player.add(ship,shield)

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()


    mob1 = Mob(100,0,enemy_img)
    mob2 = Mob(300,0,enemy_img)
    mob3 = Mob(500,0,enemy_img)
    mob4 = Mob(700,0,enemy_img)
    mob5 = Mob(900,0,enemy_img)
    mob7 = Mob(200,100,enemy_img)
    mob8 = Mob(400,100,enemy_img)
    mob9 = Mob(600,100,enemy_img)
    mob10 = Mob(800,100,enemy_img)
    mob11 = Mob(100,200,enemy_img)
    mob12 = Mob(300,200,enemy_img)
    mob13 = Mob(500,200,enemy_img)
    mob14 = Mob(700,200,enemy_img)
    mob15 = Mob(900,200,enemy_img)
    mobs = pygame.sprite.Group()
    mobs.add(mob1,mob2,mob3,mob4,mob5,mob7,mob8,mob9,mob10,mob11,mob12,mob13,mob14,mob15)

    fleet = Fleet(mobs)

    ''' set stage '''
    stage = START
    done = False

def draw_grid(width, height, scale):
    '''
    Draws a grid that can overlay your picture.
    This should make it easier to figure out coordinates
    when drawing pictures.
    '''
    for x in range(0, width, scale):
        pygame.draw.line(screen, WHITE, [x, 0], [x, height], 1)
    for y in range(0, height, scale):
        pygame.draw.line(screen, WHITE, [0, y], [width, y], 1)

def draw_meter():
    for m in meters:
        pygame.draw.rect(screen,WHITE,m)

def draw_hits():
    for h in hits:
        pygame.draw.rect(screen, GREEN, h)
# Game loop
setup()

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING

            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
                if event.key == pygame.K_p:
                    stage = PAUSE

            elif stage == PAUSE:
                if event.key == pygame.K_p:
                    stage = PLAYING

            elif stage == END:
                if event.key == pygame.K_SPACE:
                    setup()



    pressed = pygame.key.get_pressed()

    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()


    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update()
        lasers.update()
        bombs.update()
        fleet.update()
        mobs.update()

        if not ship.is_alive:
            stage = END

        if len(mobs) == 0:
            stage = END




    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.blit(star_Background_img, (0,0))
    if stage == PLAYING:
        lasers.draw(screen)
        bombs.draw(screen)
    draw_meter()
    draw_hits()
    player.draw(screen)
    mobs.draw(screen)
    show_stats()


    if stage == START:
        show_title_screen()

    if stage == END:
        if ship.is_alive == False:
            show_end_screen_1()

        elif len(mobs) == 0:
            show_end_screen_2()

    if stage == PAUSE:
        show_pause()

    draw_grid(WIDTH,HEIGHT,100)
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
