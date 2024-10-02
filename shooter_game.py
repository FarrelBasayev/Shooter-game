#Create your own shooter

from pygame import *
from random import randint
from time import time as timer

running = True
finish = False
score = 0
lost = 0
max_lost = 3
life = 3

font.init()
font2 = font.Font(None, 36)
win = font2.render('YOU WIN!!!', True, (0,255,0))
lose = font2.render('YOU LOSE!!!', True, (255,0,0))

class Gamesprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(Gamesprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > 500:
            self.rect.x = randint(80,620)
            self.rect.y = 0
            lost = lost + 1

class Bullet(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.play()

window = display.set_mode([700,500])
display.set_caption("Shooter game")
background = transform.scale(image.load('galaxy.jpg'), (700,500))
ship = Player('rocket.png', 5, 400, 80, 100, 10)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy("ufo.png", randint(80,620),0,80,50, randint(1,5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy("asteroid.png", randint(80,620),0,80,50, randint(1,5))
    asteroids.add(asteroid)

bullets = sprite.Group()
num_fire = 0
rel_time = False

while running:

    time.delay(60)

    for e in event.get():
        if e.type == QUIT:
            running = False
    
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    ship.fire()
                    fire_sound.play()
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()

    if not finish:
        window.blit(background,(0,0))
        text = font2.render("Score: " + str(score), 1, (255,255,255))
        window.blit(text, (10,20))
        text_lose = font2.render("Miss: " + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,55))

        ship.update()
        monsters.update()
        asteroids.update()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
        ship.reset()

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reloading...', 1, (150,0,0))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1,5))
            monsters.add(monster)
            if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
                sprite.spritecollide(ship, monsters, True)
                sprite.spritecollide(ship, asteroids, True)
                life = life - 1

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost or life == 0:
            finish = True
            window.blit(lose, (200,200))

        if score > 20:
            finish = True
            window.blit(win, (200,200))

        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150,0,0)

        text_life = font2.render(str(life), 1, life_color)
        window.blit(text_life, (650,10))

        display.update()