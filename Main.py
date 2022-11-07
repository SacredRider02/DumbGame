import pygame as py

py.init()

win = py.display.set_mode((500,500))

class Player:
    def __init__(self, x, y):
        x = self.x
        y = self.y
        dr = 1
    
    def draw(self, win):
        py.draw.rect(win, (255,0,0), (20, 40, 50, 50))

run = True

while run:
    for event in py.event.get():
        if event.type==py.QUIT:
            py.quit()
