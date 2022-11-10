import pygame as py

py.init()

win = py.display.set_mode((720,390))

bg = py.image.load("dungeonBackground.png")
py.Surface.convert_alpha(bg)

idle = py.image.load("knight.png")


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dr = 1
    
    def draw(self, win):
        win.blit(idle, (self.x, self.y))

player = Player(50,250)

run = True

def makeScreen():
    win.blit(bg, (0,0))
    player.draw(win)
    py.display.update()

while run:
    makeScreen()
    for event in py.event.get():
        if event.type==py.QUIT:
            py.quit()
            run = False
