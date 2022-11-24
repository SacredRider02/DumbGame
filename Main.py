import pygame as py
import random

py.init()

win = py.display.set_mode((720,390))

font = py.font.SysFont("Comicsans", 30, True)

bg = py.image.load("dungeonBackground.png").convert_alpha()

idle = py.image.load("commando.png").convert_alpha()
knight = py.image.load("knight.png").convert_alpha()
gunny = py.image.load("gun_monster.png").convert_alpha()
blast = py.image.load("blast_effect.png").convert_alpha()

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
        self.type = "knight"
        self.x = x
        self.dr = dr
        self.y = 250

    def draw(self, win):
        win.blit(py.transform.flip(knight, self.dr, False), (self.x, self.y))

class Enemy2:
    global r
    def __init__(self, x, dr, r):
        self.type = "gunny"
        self.x = x
        self.y = 250
        self.dr = dr
        self.r = r
        self.rate = random.randint(80, 200)
    
    def draw(self, win):
        win.blit(py.transform.flip(gunny, self.dr, False), (self.x, self.y))
        
class EnemyBullet:
    def __init__(self, x, dr):
        self.x = x
        self.dr = dr
        self.y = 260

    def draw(self, win):
        py.draw.rect(win, (0,255, 50), (self.x, self.y, 15, 5))

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
enemy_bullets = []
shoot = False
hp, r, effectlasts = 10, 1, 0

enemies = []

def makeScreen():
    global jump, upspeed, hp, effectlasts
    win.blit(bg, (0,0))
    
    for bullet in bullets:
        bullet.x -= 20
        if bullet.dr == False:
            bullet.x += 40
        bullet.draw(win)

    for enemy in enemies:

        if (jump == False and player.x in range(enemy.x-27, enemy.x) and enemy.dr == True and enemy.type == "knight") or (jump == False and enemy.type == "knight" and player.x in range(enemy.x, enemy.x+23) and enemy.dr == False):
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
                elif enemy.x in range(bullet.x-20, bullet.x+20) and enemy.dr != bullet.dr and enemy.type == "knight":
                    bullets.remove(bullet)
                else:
                    bullets.remove(bullet)
                    enemies.remove(enemy)

        else:enemy.draw(win)

        if enemy.type == "gunny" and (r - enemy.r) % enemy.rate == 0:
            enemy_bullets.append(EnemyBullet(enemy.x, enemy.dr))
            print('shoot')
    for bullet in enemy_bullets:
        bullet.x -= 12
        if not bullet.dr:
            bullet.x += 24
        if bullet.x in range(player.x, player.x + 33) and bullet.y in range(player.y, player.y+44) and shield == False:
            hp -= 1
            enemy_bullets.remove(bullet)
        elif bullet.x in range(player.x, player.x + 33) and bullet.y in range(player.y, player.y+44) and shield == True:
            enemy_bullets.remove(bullet)
        else: bullet.draw(win)
    if effectlasts > 0:
        win.blit(py.transform.flip(blast,player.dr,False), (player.x-4 if player.dr else player.x+33, player.y+27))
        effectlasts-=1

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
        enemies.append(random.choice([Enemy1(pos, True if pos > player.x else False), Enemy2(pos, True if pos > player.x else False, r)]))

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
        effectlasts = 3
        shoot = False
    
    if keys[py.K_SPACE] and shield == False:
        shoot = True
    
    r += 1

    makeScreen()
    for event in py.event.get():
        if event.type==py.QUIT:
            py.quit()
            run = False
