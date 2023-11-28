from cmu_graphics import *
from PIL import Image
import os, pathlib

def onAppStart(app):
    
    app.turningLeft = False
    spritestrip = Image.open('sprites/mario-3.gif')
    
    
    app.sprites = [ ]
    w,h = spritestrip.size
    unit = w//9
    for i in range(9):
        # Split up the spritestrip into its separate sprites
        # then save them in a list
        frame = spritestrip.crop((unit*i,0, unit*(i+1), h))
        sprite = CMUImage(frame)
        app.sprites.append(sprite)
        
    # app.spriteCounter shows which sprite (of the list) 
    # we should currently display
    app.spriteCounter = 0
    app.stepCounter = 0
    app.stepsPerSecond = 50

def onStep(app):
    if app.turningLeft:
        while app.spriteCounter < 3:
            app.spriteCounter += 1
    else:
        app.spriteCounter = 0

def onKeyHold(app,keys):
    print(keys)
    if "left" in keys:
        app.turningLeft = True

def onKeyRelease(app,keys):
    if 'left' not in keys:
        app.turningLeft = False
        

def redrawAll(app):
    sprite = app.sprites[app.spriteCounter]
    drawImage(sprite,200, 200, align = 'center')

def main():
    runApp(width=400, height=400)

if __name__ == '__main__':
    main()