#Attempting to mimic pygame using cmu graphics, pil and numpy

from cmu_graphics import *
from PIL import Image
import numpy, math
import math
from numba import njit

def onAppStart(app):
    #Open map and scale to canvas size (could scale to some other size though)
    app.perspective = True

    app.map = Image.open('marioKart.png')
    app.map = app.map.resize((app.width, app.height))
    app.map = app.map.convert('RGB')

    app.hres = 120 # horizontal resolution
    app.vres = 100 # vertical resolution


    #Make a new image with a scaled down resolution
    
    app.frame = numpy.random.uniform(0,1,(app.hres,app.vres*2,3))

    app.sky = #pg.surfarray.array3d(pg.transform.scale(sky, (360, halfvres*2)))/255
                #if i can figure out a way to convert this into a 3d array of the pixels in the skybox
    app.track = #pg.surfarray.array3d(pg.image.load('marioKart.jpg'))/255
                # similarly here

    #Set some values
    app.fov = 60

    #Car position
    app.x, app.y, app.rot = 0,0,0
    # app.rot will act as the "angle" now

    

    #We can't quite go this fast, but we can try
    #not sure where steps will fit into this
    app.stepsPerSecond = 30

    # list of the rgb values of the walls
    app.barrierList = [(232,232,0),(0, 32, 248),(104,104,248),(232,0,0),(248,72,72),(0,128,0),(0,168,0),(0,208,0),(248,248,144),(96,248,96)]

    #Calculate the initial view
    makePerspective(app)
    
    
    
#This function finds a pixel on the map along a line of sight
def makePerspective(app):
    newFrame(app)
# according to the video using numba should optimize the game and make it much more clear and runnable which is what we ahve been struggling with

@njit()
def newFrame(app):
    # Goes through all the lines in the bottom half of the screen
    for i in range(app.hres):
        rotationi = app.rot + numpy.deg2rad(i/app.fov - 30)
        sin, cos = numpy.sin(rotationi), numpy.cos(rotationi)
        # Calculates the difference from that point to the car
        # adding skybox pixels to array of pixels
        app.frame[i][:] = app.sky[int(numpy.rad2deg(rotationi)%359)][:]
        for j in range(app.vres):
            n = app.vres/(app.vres - j)
            x,y = app.x + cos*n, app.y + sin*n
            # texture coordinates size of the mariokart png is 1024 x 1024
            xx,yy = int(x/(3%1*1024)),int(y/(3%1*1024))
            # theoretically, should be able to use to list of pixels to transform
            app.frame[i][app.vres*2 - j -1] = app.track[xx][yy]/255 #seperating the frames

# after doing research on pygame, there are funtions like surfarray that 

frames = numpy.#function that can create an array similar to surfarray(app.frame *255)

#then we can transform the image and i think it should work if i am thinking about this right
app.transformedImage = app.track.transform((800, 800), Image.PERSPECTIVE,
        frames, Image.BICUBIC)

def onMousePress(app,mouseX,mouseY):
    app.perspective = not app.perspective
                
# using keyhold to theoretically make it so that it moves as I hold the key
def onKeyHold(app,keys):
    movement(app.x,app.y,app.rot,keys)

# in the video the movement function takes in another paramete called "et" 
# i don't know how to implemet "et", it seems to be time related 
def movement(x,y,rot,keys):
    currPix = app.map.getpixel(app.x,app.y)
    if currPix not in app.barrierList:
        # Check if the new position would be on a barrier
        if 'up' in keys:
            newPix = app.map.getpixel((app.x, app.y + 5))
            if newPix not in app.barrierList:
                app.x, app.y = app.x + numpy.cos(app.rot)*0.005, app.y + numpy.sin(app.rot)*0.005
        elif 'down' in keys:
            newPix = app.map.getpixel((app.x, app.y - 5))
            if newPix not in app.barrierList:
                app.x, app.y = app.x - numpy.cos(app.rot)*0.005, app.y - numpy.sin(app.rot)*0.005
        elif 'left' in keys:
            newPix = app.map.getpixel((app.x - 5, app.y))
            if newPix not in app.barrierList:
                app.rot = app.rot - 0.001
        elif 'right' in keys:
            newPix = app.map.getpixel((app.x + 5, app.y))
            if newPix not in app.barrierList:
                app.rot = app.rot + 0.001
    """in the original video the updated positions and coordinates are returned 
    however since we are using CMU graphics, the app updates values on the spot."""



    



def onStep(app):
    makePerspective(app)
    print("You are on this color: ", app.map.getpixel((app.x,app.y)))
    

def redrawAll(app):
    if app.perspective:
        ## Draw the perspective view.  
        ## Unsure whether resizing with pil or cmuImage is faster
        
        drawImage(CMUImage(app.transformedImage),0,0)

    else:
        drawImage(CMUImage(app.map),0,0)
        drawCircle(app.x, app.y, 10, fill='red')

def main():
    runApp(width=600, height=600)

if __name__ == '__main__':
    main()