from cmu_graphics import *
from PIL import Image, ImageOps
import os, pathlib

players = {'mario':'sprites/mario-3.gif','luigi':1,'peach':1,'toad':1,'yoshi':1,'bowser':1,'dk':1,'wario':1}

class Sprite():
    
    def __init__(self,character,sx,sy):


        self.spriteStrip = Image.open(players[character])
        self.frames = []
        
        w,h = self.spriteStrip.size
        unit = w//9
        for i in range(9):
            # Split up the spritestrip into its separate sprites
            # then save them in a list
            frame = self.spriteStrip.crop((unit*i,0, unit*(i+1), h))
            resizeframe = frame.resize((sx,sy))
            sprite = CMUImage(resizeframe)
            self.frames.append(sprite)

    def chooseCharacter(self):
        if self.px == 111 and self.py == 158:
            self.character = 'mario'
        elif self.firstpx == 223 and self.firstpy == 158:
            self.character = 'luigi'
        elif self.firstpx == 335 and self.firstpy == 158:
            self.character = 'peach'
        elif self.firstpx == 447 and self.firstpy == 158:
            self.character = 'toad'
        elif self.firstpx == 111 and self.firstpy == 320:
            self.character = 'yoshi'
        elif self.firstpx == 223 and self.firstpy == 320:
            self.character = 'bowser'
        elif self.firstpx == 335 and self.firstpy == 320:
            self.character = 'dk'
        elif self.firstpx == 447 and self.firstpy == 320:
            self.character = 'koopa'
    

    def draw(self,x,y,frame):
        sprite = self.frames[frame]
        drawImage(sprite,x,y,align = 'center')

