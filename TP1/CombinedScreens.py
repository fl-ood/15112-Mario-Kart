from cmu_graphics import *
from PIL import Image
from PIL import ImageFilter
import math
import random

def onAppStart(app):

#---Map Stuff------------------------------------------------
    #Open map and scale to canvas size (could scale to some other size though)
    app.map = Image.open('images/marioKart.png')
    app.map = app.map.resize((app.width, app.height))
    app.map = app.map.convert('RGB')

    #Make a new image with a scaled down resolution
    app.scaleDown = 7 # Lower = better resolution, slower speed
    app.view = Image.new(mode='RGB', size=(app.width//app.scaleDown, app.height//app.scaleDown))
    
    #Start in perspective view w/spinning camera
    app.perspective = True
    app.spin = True

    #Set some values
    app.fov = 60

    #Car position
    app.x, app.y = app.width/2, app.height/2-30
    app.angle = 0

    #Camera position
    app.cameraHeight = 50

    #We can't quite go this fast, but we can try
    app.game_stepsPerSecond = 30
    app.barrierList = [(232,232,0),(0, 32, 248),(104,104,248),(232,0,0),(248,72,72),(0,128,0),(0,168,0),(0,208,0),(248,248,144),(96,248,96)]
    #Calculate the initial view
    makePerspective(app)

#--Selection Screen-------------------------------------------------
    app.select = Image.open('images/selectionscreen.png')
    app.shift = 0
    app.select_stepsPerSecond = 10
    app.message = "Choose your driver.... "
    app.paused = True

#--Title Screen---------------------------------------------
    app.titlescreen = Image.open('images/title.png')
    app.start = False
    app.opacity = 0
    app.title_stepsPerSecond = 1
    app.fiftycc = False
    app.hundredcc = False
#--Game---------------------------------------------

#This function finds a pixel on the map along a line of sight
def makePerspective(app):
    #Scan left to right
    
    for x in range(app.view.width): 
        yaw = (x/app.view.width) * app.fov - (app.fov/2)  #[-30, -29... 0 ... 29 30]
        dxScale = math.cos((app.angle+yaw)*math.pi/180)
        dyScale = math.sin((app.angle+yaw)*math.pi/180)

        #Scan top to bottom
        for y in range(app.view.height): 
            pitch = (1 - y/app.view.height)*90
            dist = app.cameraHeight * math.tan(pitch*math.pi/180)
            
            dx = dist*dxScale
            dy = dist*dyScale
            fx = app.x + dx
            fy = app.y + dy
            #fx = max(0, min(app.map.width-1, fx))
            #fy = max(0, min(app.map.height-1, fy))
            if 0 <= fx < app.map.width and 0 <= fy < app.map.height:
                r,g,b = app.map.getpixel((fx,fy))
                app.view.putpixel((x,y),(r,g,b))
            else:
                ## If we're looking off the map, just make the pixel blue
                app.view.putpixel((x,y),(100,100,255))
    # app.view = app.view.filter(ImageFilter.EMBOSS)


def game_onKeyPress(app,key):
    currPix = app.map.getpixel((app.x,app.y))
    if key == 'p': #p draws the map
        app.perspective = not app.perspective
    elif key == 'space':
        setActiveScreen('title')
    elif key == 'left': #left and right change the angle
        app.angle -= 5
    elif key == 'right':
        app.angle += 5

    elif key == 's': #s spins the camera
        app.spin = not app.spin
    

    elif currPix not in app.barrierList:
        # Check if the new position would be on a barrier
        if key == 'up':
            new_pixel = app.map.getpixel((app.x, app.y + 5))
            if new_pixel not in app.barrierList:
                app.y += 5
        elif key == 'down':
            new_pixel = app.map.getpixel((app.x, app.y - 5))
            if new_pixel not in app.barrierList:
                app.y -= 5
        elif key == 'a':
            new_pixel = app.map.getpixel((app.x - 5, app.y))
            if new_pixel not in app.barrierList:
                app.x -= 5
        elif key == 'd':
            new_pixel = app.map.getpixel((app.x + 5, app.y))
            if new_pixel not in app.barrierList:
                app.x += 5
    makePerspective(app)

def game_onStep(app):
    if app.spin:
        app.angle += 5
        makePerspective(app)
    print("You are on this color: ", app.map.getpixel((app.x,app.y)))
    

def game_redrawAll(app):
    if app.perspective:
        ## Draw the perspective view.  
        ## Unsure whether resizing with pil or cmuImage is faster
        resizedView = app.view.resize((app.width,app.height))
        #drawImage(CMUImage(app.image2),0,0, width = app.width, height = app.height)
        drawImage(CMUImage(resizedView),0,0)

    else:
        drawImage(CMUImage(app.map),0,0)
        drawCircle(app.x, app.y, 10, fill='red')

#--Selection Screen--------------------------------------------
def select_redrawAll(app):
    resizedView = app.select.resize((app.width,app.height))
    drawImage(CMUImage(resizedView),0,0)
    for i in range(25):
        drawLabel(app.message[(i+ app.shift) % len(app.message)],120 + 20*i,200,size = 20,bold = True,fill = 'yellow')

def select_onStep(app):
    app.shift += 1

def select_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('game')
    

#--Title Screen--------------------------------------------

def title_redrawAll(app):
    resizedView = app.titlescreen.resize((app.width,app.height))
    drawImage(CMUImage(resizedView),0,0)
    if app.start:
        drawRect(150,200,100,60, opacity = app.opacity)
        drawLabel('50 cc', 200,215,size =20,bold = True, fill = 'white')
        drawLabel('100 cc', 200,245,size =20,bold = True, fill = 'white')
    else:
        drawLabel('press b to start', 200,200,size =20,bold = True)
    if app.fiftycc:
        print('yayyyy')
    elif app.hundredcc:
        print('yayyy 100000')
    

def title_onStep(app):
    if app.start:
        while app.opacity < 100:
            app.opacity += 1

def title_onKeyPress(app, key):
    if key == 'b':
        app.start = True 
    if key == 'space':
        setActiveScreen('select')

def title_onMousePress(app,mouseX,mouseY):
    if 175 < mouseX < 225 and app.start: 
        if 205 < mouseY < 220 and app.hundredcc != True:
            app.fiftycc = True
        if 235 < mouseY < 250 and app.fiftycc != True:
            app.hundredcc = True
        


# Your screen names should be strings
runAppWithScreens(initialScreen='title')
