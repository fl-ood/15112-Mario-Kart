from cmu_graphics import *
from PIL import Image
from PIL import ImageFilter
import math
import random
import time
from sprites import Sprite


###DIRECTIONS:
# When app starts, UI hasnt been fully scaled/configured yet so press space twice
# When on the track the map will do a 360 then wait 3 seconds and the game will start, you move with your mouse and must cross the finsih line forward 3 times to win


def onAppStart(app):

    app.width = 600
    app.height = 600

#---Map Stuff------------------------------------------------
    #Open map and scale to canvas size (could scale to some other size though)
    app.map = Image.open('images/marioKart.png') # from the spriters resource
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

    #Camera position
    app.x, app.y = 539.3464291081129, 346.7310349918769
    app.angle = 0
    app.cameraHeight = 20

    #We can't quite go this fast, but we can try
    app.select_stepsPerSecond = 30
    app.stepsPerSecond = 10
    app.speed = 10
    # list of the rgb values on the edges of the map 
    app.barrierList = [(232,232,0),(152,152,0),(0, 32, 248),
                       (104,104,248),(232,0,0),(248,72,72),(0,128,0),
                       (0, 136, 0),(0,168,0),(0,208,0),(120,0,0),(0,232,0),
                       (248,248,144),(96,248,96),(0,0,96)]
    #lsit of rgb values that will slow the player down
    app.slowTerrain = [(176, 160, 112),(144, 128, 88),(160, 144, 96)]
    #Calculate the initial view
    makePerspective(app)

#--Game Screen-------------------------------------------------
    app.gameStart = False
    app.lap = 0
    app.laptime = 0
    app.go = False
    app.count = 0
    app.endgame = False
    
#--Selection Screen-------------------------------------------------
    app.select = Image.open('images/selectionscreen.png') # title screen image is from google https://tcrf.net/images/8/8c/Smk_title_bg_us.png
    app.shift = 0
    app.stepsPerSecond = 10
    app.message = "Choose your driver.... "
    app.paused = True
    app.countdown = False

#--Title Screen---------------------------------------------
    app.titlescreen = Image.open('images/title.png')
    app.start = False
    app.opacity = 0
    app.title_stepsPerSecond = 1
    app.fiftycc = False
    app.hundredcc = False
    app.highlight50 = 'white'
    app.highlight100 = 'white'

#--Sprite Stuff--------------------------------------------------
    app.mario = Sprite('sprites/mario-3.gif',app.width//4,app.height//4) # sprites come from The Spriters Resource
    
    app.turningLeft = False
    app.turningRight = False
    app.spriteCounter = 0
    app.stepCounter = 0
    
#--Game---------------------------------------------

# starts the race after a full spin
def startRace(app):
    if app.angle == 275 and not app.gameStart:
        app.spin = False
        app.countdown = True
        for i in range(3,0,-1):
            app.count = i
            time.sleep(1)
        app.count = 'GO'
        time.sleep(0.5)
        app.gameStart = True



def passedFinishLine(app,dy):
    if 498 <= app.x <= 593:
        movement = app.y + dy
        print(movement)

        if 323 < app.y < 328:
            if movement > 325:
                return False
            else:
                app.lap += 1
                
    print(app.lap)
#(498,593) = x coord range for finish line
#325 = y value of the finish line

    
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
            fx = app.x + dx # make other variable such as cam.x cam.y when drawing sprite
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

def game_onKeyHold(app,keys):
    app.currKeys = keys
    if "left" in keys:
        app.turningLeft = True
    if "right" in keys:
        app.turningRight = True

def game_onKeyRelease(app,keys):
    if 'left' in keys:
        app.turningLeft = False
    if 'right' in keys:
        app.turningRight = False
    

def game_onKeyPress(app,key):
    currPix = app.map.getpixel((app.x,app.y))
    if key == 'p': #p draws the map
        app.perspective = not app.perspective
    elif key == '1':
        app.gameStart = not app.gameStart

    makePerspective(app)

def game_onStep(app):
    if app.spin:
        app.angle += 5
    if app.gameStart == False:
        startRace(app)

    if app.lap == 3:
        app.endgame = True

    if app.endgame:
        app.gameStart = False
        
    # to convert decimal places
    # def convert(x,decplaces):
    #x *= 10**decimalplaces

    if app.gameStart:
        app.laptime += 1/app.stepsPerSecond # use time.time()
        # Update the position based on the mouse direction
        dx = 5 * math.cos(math.radians(app.angle))
        dy = 5 * math.sin(math.radians(app.angle))
        # checks the  current pixel to see if it is in the list of barriers 
        currPix = app.map.getpixel((app.x,app.y))
        if currPix not in app.barrierList:
            # rechecks the pixel with the added movement to make sure it is legal in order to avoid image crashes
            new_pixel = app.map.getpixel((app.x + dx, app.y + dy))
            if new_pixel not in app.barrierList:
                app.x += dx
                app.y += dy
        # slows down the speed when the camera/car is on the sandy terrain
        if currPix in app.slowTerrain:
            app.slow = True
            if app.slow:
                newSpeed = app.speed // 2
                app.stepsPerSecond = newSpeed
        # if it is back in the grey terrain return speed to normal
        elif currPix == (96,96,96):
            app.slow = False
            app.stepsPerSecond = app.speed

        if app.turningLeft:
            app.angle -= 10
            while app.spriteCounter < 3:
                # if app.stepCounter % app.stepsPerSecond == 0: this line cause program to crash for some reason?
                app.spriteCounter += 1
        elif app.turningRight:
            app.angle += 10
            while app.spriteCounter < 3:
                # if app.stepCounter % app.stepsPerSecond == 0:
                app.spriteCounter += 1
        else:
            app.spriteCounter = 0
        passedFinishLine(app,dy)

    #print("You are on this color: ", app.map.getpixel((app.x,app.y)))
    
    makePerspective(app)

# def game_onMouseMove(app,mouseX,mouseY):
#     if app.gameStart:
#         app.angle = mouseX
        
    

def game_redrawAll(app):
    if app.perspective:
        ## Draw the perspective view.  
        ## Unsure whether resizing with pil or cmuImage is faster

        resizedView = app.view.resize((app.width,app.height))
        #drawImage(CMUImage(app.image2),0,0, width = app.width, height = app.height)
        drawImage(CMUImage(resizedView),0,0)
        drawLabel(app.lap,app.width//2,70,size = 40,bold = True)
        drawLabel(app.laptime,app.width//2,20,size = 40,bold = True)

        if app.turningLeft:
            app.mario.draw(app.width//2, app.height//2, app.spriteCounter)
        else:
            app.mario.draw(app.width//2, app.height//2, 0)
        
        if app.gameStart == False and app.count != 0 and not app.endgame:
            drawLabel(app.count,300,300,size = 40,bold = True)
        if app.endgame:
            drawLabel("YOU WON",app.width//2,app.height//2,size = 40,bold = True)
            drawLabel(f"Your laptime: {app.laptime}",app.width//2,app.height//2 + 50,size = 40,bold = True)
    else:
        drawImage(CMUImage(app.map),0,0)
        drawCircle(app.x, app.y, 10, fill='red')

#--Selection Screen--------------------------------------------
def select_redrawAll(app):
    resizedView = app.select.resize((app.width,app.height))
    drawImage(CMUImage(resizedView),0,0)
    # draws the driver selection text in a scrolling fashion (used scrolling carpe diems from CS Academy)
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
    drawImage(CMUImage(resizedView),0,0,width =app.width,height = app.height)
    # once b is pressed display the 50cc and 100cc options
    if app.start:
        drawRect(app.width/2 - 50,app.height/2,100,60, opacity = app.opacity)
        drawLabel('50 cc', app.width/2,app.height/2 +15,size =20,bold = True, fill = app.highlight50 )
        drawLabel('100 cc', app.width/2,app.height/2 + 45,size =20,bold = True, fill = app.highlight100)
    # else display the press b message
    else:
        drawLabel('press b to start', app.width/2,app.height/2 + 50,size =20,bold = True, opacity = app.opacity % 100)
    
    if app.fiftycc:
        print('yayyyy')
        
        #will add functionally to set different speeds
    elif app.hundredcc:
        print('yayyy 100000')
        
    

def title_onStep(app):
    # createa fading word effect on title screen 
    if not app.start:
        app.opacity += 5
    

def title_onKeyPress(app, key):
    if key == 'b':
        app.start = True 
    if key == 'space':
        app.stepsPerSecond = 10
        setActiveScreen('select')

def title_onMousePress(app,mouseX,mouseY):
    # when clicking the buttons it will set it == to true which will determine the speed, you can't click both buttons
    if 275 < mouseX < 335 and app.start: 
        if 300 < mouseY < 330 and app.hundredcc != True:
            app.fiftycc = True
            #app.speed == TBD
        if 330 < mouseY < 360 and app.fiftycc != True:
            app.hundredcc = True
            # app.speed == TBD


def title_onMouseMove(app,mouseX,mouseY):
    # highlights the options
    if app.start: 
        if 300 < mouseY < 330 and 275 < mouseX < 335:
            app.highlight50 = 'yellow'
            app.highlight100 = 'white'
        elif 330 < mouseY < 360 and 275 < mouseX < 335:
            app.highlight100 = 'yellow'
            app.highlight50 = 'white'
        else:
            app.highlight50 = 'white'
            app.highlight100 = 'white'
        

# Your screen names should be strings
runAppWithScreens(initialScreen='title')
