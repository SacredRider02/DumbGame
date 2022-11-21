import pygame as py
import random

py.init()

win = py.display.set_mode((720,390))

font = py.font.SysFont("Comicsans", 30, True)

bg = py.image.load("dungeonBackground.png").convert_alpha()

idle = py.image.load("commando.png").convert_alpha()
knight = py.image.load("knight.png").convert_alpha()


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dr = False
    
    def draw(self, win):
        win.blit(py.transform.flip(idle,self.dr,False), (self.x, self.y))
        if shield == True:
            py.draw.circle(win, (0, 213, 255), (self.x+15, self.y+22), 30, 1)

player = Player(50,248)

class Enemy1:
    def __init__(self, x, dr):
        self.x = x
        self.dr = dr
        self.y = 250

    def draw(self, win):
        win.blit(py.transform.flip(knight, self.dr, False), (self.x, self.y))

class Bullet:
    def __init__(self, x, y, dr):
        self.x = x
        self.y = y
        self.dr = dr
    
    def draw(self, win):
        py.draw.rect(win, (255,0,0), (self.x, self.y, 15, 5))

run = True
global jump, hp
jump = False
bullets = []
shoot = False
hp = 10
r = 1
enemies = []

def makeScreen():
    global jump, upspeed, hp
    win.blit(bg, (0,0))
    
    for bullet in bullets:
        bullet.x -= 20
        if bullet.dr == False:
            bullet.x += 40
        bullet.draw(win)

    for enemy in enemies:

        if jump == False and player.x in range(enemy.x-5, enemy.x):
            hp -= 1
            jump = True
            upspeed = 16
            player.y -= upspeed
            if player.dr:
                player.x += 50
            player.x-= 25

        if len(bullets) > 0:
            for bullet in bullets:
                if enemy.x not in range(bullet.x-20, bullet.x+20):
                    enemy.draw(win)
                elif enemy.x in range(bullet.x-20, bullet.x+20) and enemy.dr != bullet.dr:
                    bullets.remove(bullet)
                else:
                    bullets.remove(bullet)
                    enemies.remove(enemy)

        else:enemy.draw(win)

    health = font.render("Health: "+str(hp), True, (255,0,0))
    win.blit(health, (30, 20))
    
    player.draw(win)
    
    py.display.update()

while run:

    global shield, upspeed
    
    if r % 80 == 0:
        pos = random.randint(0,680)
        while pos in range(player.x-60, player.x+60):
            pos = random.randint(0,680)
        enemies.append(Enemy1(pos, True if pos > player.x else False))

    if r % 160 == 0 and len(enemies) > 3:
        enemies.pop(random.randint(0, len(enemies)-1))
    
    py.time.delay((30))

    keys = py.key.get_pressed()

    if jump and player.y < 248:
        upspeed-=2
        player.y -= upspeed
    else:jump = False
   
    if keys[py.K_RIGHT] and player.x <= 687 and shield == False:
        player.x += 5
        player.dr=False
    
    if keys[py.K_LEFT] and player.x >= 5 and shield == False:
        player.x -= 5
        player.dr = True
    
    if keys[py.K_UP] and not jump and shield == False:
        jump = True
        upspeed = 16
        player.y -= upspeed
    
    if keys[py.K_DOWN]:
        shield = True
    else:shield = False

    if shoot == True and r % 10 == 0:
        bullets.append(Bullet(player.x, player.y+30, player.dr))
        shoot = False
    
    if keys[py.K_SPACE] and shield == False:
        shoot = True
    
    r += 1

    makeScreen()
    for event in py.event.get():
        if event.type==py.QUIT:
            py.quit()
            run = False
