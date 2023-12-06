from cmu_graphics import *
from PIL import Image
import os, pathlib

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

def onAppStart(app):
    #Sprite Strip: 'http://www.cs.cmu.edu/~112/notes/sample-spritestrip.png'
    
    spritestrip = Image.open('images/mario.gif')
    
    # Alternatively, if this throw an error,
    # as shown in basicPILMethods.py,
    # comment out the above line and use the following:
    
    #spritestrip = openImage('images/spritestrip.png')
    
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
    app.stepCounter += 1
    if app.stepCounter >= 9:
        app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)
        app.stepCounter = 0 

def redrawAll(app):
    sprite = app.sprites[app.spriteCounter]
    drawImage(sprite,200, 200)

def main():
    runApp(width=400, height=400)

if __name__ == '__main__':
    main()