from cmu_graphics import *
from PIL import Image, ImageOps
import os, pathlib


class Sprite():
    def __init__(self,spriteStrip,sx,sy):
        self.spriteStrip = Image.open(spriteStrip)
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

    

    def draw(self,x,y,frame):
        sprite = self.frames[frame]
        drawImage(sprite,x,y,align = 'center')

