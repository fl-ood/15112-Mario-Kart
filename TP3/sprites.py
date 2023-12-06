from cmu_graphics import *
from PIL import Image, ImageOps
import os, pathlib
from PIL import ImageOps

players = {'mario':'sprites/mario.gif',
           'luigi':'sprites/luigi.gif','peach':'sprites/peach.gif',
           'toad':'sprites/toad.gif','yoshi':'sprites/yoshi.gif',
           'bowser':'sprites/bowser.gif','dk':'sprites/dk.gif',
           'koopa':'sprites/koopa.gif','kirby':'sprites/kirby.gif'}

spriteCount = {'mario':9,'luigi':10,'peach':4,'toad':8,'yoshi':6,'bowser':10,'dk':8,'koopa':6,'kirby':12}
turningFrames = {'mario':3,'luigi':2,'peach':3,'toad':3,'yoshi':3,'bowser':3,'dk':2,'koopa':3,'kirby':4}
reverse = {'mario':False,'luigi':False,'peach':False,'toad':True,'yoshi':True,'bowser':False,'dk':False,'koopa':True,'kirby':True}
winSprites = {'mario':'win/mariowin.gif','luigi':'win/luigiwin.gif','peach':'win/peachwin.gif','toad':'win/toadwin.gif','yoshi':'win/yoshiwin.gif','bowser':'win/bowserwin.gif','dk':'win/dkwin.gif','koopa':'win/koopawin.gif','kirby':'win/kirbywin.gif'}
winSpriteCount = {'mario':9,'luigi':10,'peach':10,'toad':4,'yoshi':12,'bowser':10,'dk':8,'koopa':8,'kirby':12}

class Sprite():
    
    def __init__(self, character, sx, sy):
        self.character = character
        self.spriteStrip = Image.open(players[character])
        self.winStrip = Image.open(winSprites[character])
        self.frames = []
        self.winFrames = []
        self.neutralFrame = 0
        self.turningFrames = turningFrames[character]
        self.reverse = reverse[character]
        
        w,h = self.spriteStrip.size
        unit = w//spriteCount[character]

        for i in range(spriteCount[character]):
            # Split up the spritestrip into its separate sprites
            # then save them in a list
            frame = self.spriteStrip.crop((unit*i,0, unit*(i+1), h))
            resizeframe = frame.resize((sx,sy))
            self.frames.append(resizeframe)
        
        winW,winH = self.winStrip.size
        winUnit = winW//winSpriteCount[character]

        for i in range(winSpriteCount[character]):
            # Split up the spritestrip into its separate sprites
            # then save them in a list
            frame = self.winStrip.crop((winUnit*i,0, winUnit*(i+1), winH))
            resizeframe = frame.resize((sx,sy))
            self.winFrames.append(resizeframe)

    def draw(self,x,y,frame):
        sprite = self.frames[frame]
        sprite = CMUImage(sprite)
        drawImage(sprite,x,y,align = 'center')
    
    def drawWin(self,x,y,frame):
        sprite = self.winFrames[frame]
        sprite = CMUImage(sprite)
        drawImage(sprite,x,y,align = 'center')
       
    def drawMirror(self, x, y, frame):
        sprite = self.frames[frame]
        mirrored_sprite = ImageOps.mirror(sprite)
        mirrored_sprite = CMUImage(mirrored_sprite)  # Convert to CMUImage
        drawImage(mirrored_sprite, x, y, align='center')
        
    
