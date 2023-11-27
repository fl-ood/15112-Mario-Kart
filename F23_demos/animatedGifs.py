#----------------------------------------
# GIF demo v.1.0
#    4/10/2023
#    Ping me at mdtaylor@andrew.cmu.edu
#----------------------------------------

from cmu_graphics import *
from PIL import Image

def onAppStart(app):
    myGif = Image.open('images/mario.gif')
    app.spriteList = []
    for frame in range(myGif.n_frames):
        #Set the current frame
        myGif.seek(frame)
        #Resize the image
        fr = myGif.resize((myGif.size[0]//2, myGif.size[1]//2))
        #Flip the image
        fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
        #Convert to CMUImage
        fr = CMUImage(fr)
        #Put in our sprite list
        app.spriteList.append(fr)

    print(app.spriteList)

    ##Fix for broken transparency on frame 0
    #app.spriteList.pop(0)

    app.spriteCounter = 0
    app.stepsPerSecond = 10

def onStep(app):
    #Set spriteCounter to next frame
    app.spriteCounter = (app.spriteCounter + 1) % len(app.spriteList)

def redrawAll(app):
    x, y = app.width/2, app.height/2
    #drawRect(0, 0, app.width, app.height, fill='palegreen')
    drawImage(app.spriteList[app.spriteCounter], 
              x, y, align = 'center')
    
runApp(width=600, height=600)
