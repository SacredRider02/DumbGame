import pygame as py

py.init()

win = py.display.set_mode((720,390))

bg = py.image.load("dungeonBackground.png").convert_alpha()

idle = py.image.load("knight.png").convert_alpha()


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dr = False
    
    def draw(self, win):
        win.blit(py.transform.flip(idle,self.dr,False), (self.x, self.y))

player = Player(50,250)

run = True
jump = False

def makeScreen():
    win.blit(bg, (0,0))
    player.draw(win)
    py.display.update()

while run:
    py.time.delay((30))

    keys = py.key.get_pressed()

    if jump and player.y < 250:
        upspeed-=5
        player.y -= upspeed
    else:jump = False
   
    if keys[py.K_RIGHT] and player.x <= 675:
        player.x += 5
        player.dr=False
    
    if keys[py.K_LEFT] and player.x >= 5:
        player.x -= 5
        player.dr = True
    
    if keys[py.K_SPACE] and not jump:
        jump = True
        upspeed = 25
        player.y -= upspeed

    makeScreen()
    for event in py.event.get():
        if event.type==py.QUIT:
            py.quit()
            run = False
