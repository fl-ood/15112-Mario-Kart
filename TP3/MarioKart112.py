from cmu_graphics import *
from PIL import Image
from PIL import ImageFilter
import numpy
import math
import random
import time
from sprites import Sprite

def onAppStart(app):

    app.width = 600
    app.height = 600

#---Map Stuff------------------------------------------------
    #Open map and scale to canvas size (could scale to some other size though)
    app.map = Image.open('images/marioKart.png') # from the spriters resource
    app.map = app.map.resize((app.width, app.height))
    app.map = app.map.convert('RGB')

    #Make a new image with a scaled down resolution
    app.scaleDown = 3 # Lower = better resolution, slower speed
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
    app.stepsPerSecond = 30
    app.speed = 1
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
    app.lap = -1
    app.laptime = 0
    app.go = False
    app.count = 0
    app.endgame = False
    app.moving = False
    app.movingBack = False
    app.tzero = 0
    app.counter = 0
    app.spriteCount = 0
#--Selection Screen-------------------------------------------------
    app.select = Image.open('images/selectscreen.png') # title screen image is from google https://tcrf.net/images/8/8c/Smk_title_bg_us.png
    app.shift = 0
    app.stepsPerSecond = 10
    app.message = "Choose your driver.... "
    app.paused = True
    app.countdown = False
    app.firstp = Image.open('images/firstplayer.png')
    app.firstpok = Image.open('images/firstplayerok.png')
    app.firstplayerokconfirm = Image.open('images/firstplayerokconfirm.png')
    app.firstpx = 111
    app.firstpy = 158
    app.confirm = 0

#--Title Screen---------------------------------------------
    app.titlescreen = Image.open('images/title.png')
    app.start = False
    app.opacity = 0
    app.fiftycc = False
    app.hundredcc = False
    app.highlight50 = 'white'
    app.highlight100 = 'white'

#--Sprite Stuff--------------------------------------------------
    app.character = 'mario'
    app.player = Sprite(app.character,app.width//4,app.height//4) # sprites come from The Spriters Resource
    app.turningLeft = False
    app.turningRight = False
    app.spriteCounter = 0
    app.stepCounter = 0
    app.characters = {'mario':Sprite('mario',70,70),
                      'luigi':Sprite('luigi',70,70),
                      'peach':Sprite('peach',70,70),
                      'toad':Sprite('toad',70,70),
                      'yoshi':Sprite('yoshi',70,70),
                      'bowser':Sprite('bowser',70,70),
                      'dk':Sprite('dk',70,70),
                      'koopa':Sprite('koopa',70,70),
                      'kirby':Sprite('kirby',70,70)}
    

#--Game---------------------------------------------

# starts the race after a full spin
def startRace(app):
    if app.angle == 275 and not app.gameStart:
        app.tzero = time.time()
        app.spin = False
        app.countdown = True
        for i in range(3,0,-1):
            app.count = i
            time.sleep(1)
        app.count = 'GO'
        app.gameStart = True


#(498,593) = x coord range for finish line
#325 = y value of the finish line
def passedFinishLine(app, dy):
    if 498 <= app.x <= 593:
        movement = app.y + dy

        if 323 < app.y < 328:
            if movement > 325 and dy > 0:  # Check if moving forward
                return False
            else:
                app.lap += 1
                
#This function finds a pixel on the map along a line of sight
def makePerspective(app):
    # Convert the image to a numpy array
    mapPixels = numpy.array(app.map)

    # meshgrid creates a grid of x and y coordinates with two even arrays using cartesian indexing
    # will make an array of the all the points of the map 
    x, y = numpy.meshgrid(numpy.arange(app.view.width), numpy.arange(app.view.height))

    # yaw is the horizontal angle of the camera
    yaw = (x / app.view.width) * app.fov - (app.fov / 2)
    # pitch is the vertical angle of the camera
    pitch = (1 - y / app.view.height) * 90

    # Calculate distances and final x and y coordinates
    dist = app.cameraHeight * numpy.tan(pitch * numpy.pi / 180)
    dx = dist * numpy.cos((app.angle + yaw) * numpy.pi / 180)
    dy = dist * numpy.sin((app.angle + yaw) * numpy.pi / 180)
    fx = (app.x + dx).astype(int)
    fy = (app.y + dy).astype(int)

    # Create a mask of valid coordinates
    # a mask contians all the values in an array based on a certain condition
    # this mask filters out the invalid coords from the fx and fy arrays
    mask = (0 <= fx) & (fx < app.map.width) & (0 <= fy) & (fy < app.map.height)

    # Use the mask to index into the original image array
    viewPixels = numpy.zeros((app.view.height, app.view.width, 3), dtype=int)
    viewPixels[mask] = mapPixels[fy[mask], fx[mask]]

    # Handle off-map pixels by making them blue
    # the ~ basically reverses the mask so that it will filter out the invalid coords
    viewPixels[~mask] = [100, 100, 255]

    # Convert pixels to an image
    app.view = Image.fromarray(viewPixels.astype('uint8'), 'RGB')

def game_onKeyHold(app,keys):
    app.currKeys = keys
    if 'a' in keys:
        app.turningLeft = True
    if 'd' in keys:
        app.turningRight = True
    if 'w' in keys:
        app.moving = True
    if 's' in keys:
        app.movingBack = True
    makePerspective(app)

def game_onKeyRelease(app,keys):
    if 'a' in keys:
        app.turningLeft = False
    if 'd' in keys:
        app.turningRight = False
    if 'w' in keys:
        app.moving = False
    if 's' in keys:
        app.movingBack = False
    makePerspective(app)

def game_onStep(app):
    if app.spin:
        app.angle += 5
    if app.gameStart == False:
        startRace(app)

    if app.lap == 3:
        app.endgame = True

    if app.endgame:
        app.stepsPerSecond = 50
        print(app.spriteCounter)
        app.stepCounter += 1
        if app.stepCounter >= app.spriteCount:
            app.spriteCounter = (1 + app.spriteCounter) % len(app.player.winFrames)
            app.stepCounter = 0 
        app.gameStart = False
        

    if app.gameStart:
        app.counter += 1
        t1 = time.time()
        app.laptime = (t1 - app.tzero) - 3  # use time.time()
        # Update the position based on the mouse direction
        if app.moving:
            dx = 5 * math.cos(math.radians(app.angle))
            dy = 5 * math.sin(math.radians(app.angle))
        elif app.movingBack:
            dx = -5 * math.cos(math.radians(app.angle))
            dy = -5 * math.sin(math.radians(app.angle))
        else:
            dx,dy = 0,0
        # checks the  current pixel to see if it is in the list of barriers 
        currPix = app.map.getpixel((app.x,app.y))
        if currPix not in app.barrierList:
            # rechecks the pixel with the added movement to make sure it is legal in order to avoid image crashes
            new_pixel = app.map.getpixel((app.x + dx +10 , app.y + dy + 10))
            if new_pixel not in app.barrierList:
                app.x += dx 
                app.y += dy 
        # slows down the speed when the camera/car is on the sandy terrain
        if currPix in app.slowTerrain:
            app.slow = True
            if app.slow:
                app.x -= dx // 2
                app.y -= dy // 2
        # if it is back in the grey terrain return speed to normal
        elif currPix == (96,96,96):
            app.slow = False
        if app.turningLeft:
            app.angle -= 10
            while app.spriteCounter < app.player.turningFrames:
                app.spriteCounter += 1
        elif app.turningRight:
            app.angle += 10
            while app.spriteCounter < app.player.turningFrames:
                app.spriteCounter += 1
        else:
            app.spriteCounter = 0
        passedFinishLine(app,dy)
    
    makePerspective(app)


def game_redrawAll(app):
    if app.perspective:
        ## Draw the perspective view.  
        ## Unsure whether resizing with pil or cmuImage is faster

        resizedView = app.view.resize((app.width,app.height))
        drawImage(CMUImage(resizedView),0,0)
        drawLabel(f'Lap:{app.lap}',app.width//2,70,size = 40,bold = True)
        drawLabel(f'Lap Time:{int(app.laptime)}',app.width//2,20,size = 40,bold = True)

        if app.turningLeft:
            if app.player.reverse:
                app.player.drawMirror(app.width//2, app.height//2, app.spriteCounter)
            else:
                app.player.draw(app.width//2, app.height//2, app.spriteCounter)
        elif app.turningRight:
            if not app.player.reverse:
                app.player.drawMirror(app.width//2, app.height//2, app.spriteCounter)
            else:
                app.player.draw(app.width//2, app.height//2, app.spriteCounter)
        elif app.endgame:
            app.player.drawWin(app.width//2,app.height//2,app.spriteCounter)
        else:
            app.player.draw(app.width//2, app.height//2, app.player.neutralFrame)
        if app.endgame:
            drawLabel("YOU WON",app.width//2,app.height//2 - 120,size = 40,bold = True)
            drawLabel(f"Your laptime: {int(app.laptime)}",app.width//2,app.height//2 + 120,size = 30,bold = True)
            
    

#--Selection Screen--------------------------------------------

def select_redrawAll(app):
    resizedView = app.select.resize((app.width,app.height))
    drawImage(CMUImage(resizedView),0,0,width =app.width,height = app.height)
    drawImage(CMUImage(app.firstp),app.firstpx,app.firstpy,width = 40, height = 20)
    # draws the driver selection text in a scrolling fashion (used scrolling carpe diems from CS Academy)
    drawSprites(app)
    if app.confirm == 1:
        drawImage(CMUImage(app.firstpok),355,480,width = 80, height = 25)
    elif app.confirm == 2:
        drawImage(CMUImage(app.firstplayerokconfirm),355,480,width = 80, height = 25)
    for i in range(11):
        drawLabel(app.message[(i+ app.shift) % len(app.message)],(195 + 20*i),80,size = 20,bold = True,fill = 'yellow')

def select_onStep(app):
    app.shift += 1
    app.stepCounter += 1
    chooseCharacter(app)
    

    
def updateCharacter(app):
    app.player = Sprite(app.character,app.width//4,app.height//4)
    app.spriteCount = app.player.getWinSpriteCount(app.character)


    
def select_onKeyPress(app,key):
    if key == 'space':
        setActiveScreen('game')
    elif key == 'left' and app.confirm != 1:
        if app.firstpx > 111:
            app.firstpx -= 112
    elif key == 'right' and app.confirm != 1:
        if app.firstpx < 447:
            app.firstpx += 112
    elif key == 'up' and app.confirm != 1:
        if app.firstpy > 158:
            app.firstpy -= 162
    elif key == 'down' and app.confirm != 1:
        if app.firstpy < 316:
            app.firstpy += 162
    elif key == 'enter':
        app.confirm += 1
        if app.confirm == 2:
            if app.fiftycc:
                app.stepsPerSecond = 10
            elif app.hundredcc:
                app.stepsPerSecond = 20
            app.stepCounter = 0
            setActiveScreen('game')
    elif key == 'k':
        if app.fiftycc:
            app.stepsPerSecond = 10
        elif app.hundredcc:
            app.stepsPerSecond = 20

        app.stepCounter = 0
        app.player = Sprite('kirby',app.width//4,app.height//4)
        setActiveScreen('game')
    elif key == 'backspace':
        if app.confirm != 0:
            app.confirm -= 1
    elif key == 1:
        app.start = False
        app.opacity = 0
        app.fiftycc = False
        app.hundredcc = False
        app.highlight50 = 'white'
        app.highlight100 = 'white'
        app.firstpx = 111
        app.firstpy = 158
        setActiveScreen('title')
        
        
def chooseCharacter(app):
    characterPositions = {
        (111, 158): 'mario',
        (223, 158): 'luigi',
        (335, 158): 'peach',
        (447, 158): 'toad',
        (111, 320): 'yoshi',
        (223, 320): 'bowser',
        (335, 320): 'dk',
        (447, 320): 'koopa'
    }
    
    selectedPosition = (app.firstpx, app.firstpy)
    app.character = characterPositions[selectedPosition]
    updateCharacter(app)
    playSelectAnimation(app,app.player)

# draws all the animations on the select screen (warning lengthy function)
def drawSprites(app):
    characterPositions = {
                'mario': (132, 235),
                'luigi': (132 + 115, 235),
                'peach': (132 + 115 * 2, 235),
                'toad': (132 + 115 * 3, 235),
                'yoshi': (132, 400),
                'bowser': (132 + 115, 400),
                'dk': (132 + 115 * 2, 400),
                'koopa': (132 + 115 * 3, 400)
            }
            
    selectedCharacter = app.character
    selectedPosition = characterPositions[selectedCharacter]
    # . items python method
    for character, position in characterPositions.items():
        if character == selectedCharacter:
            if app.spriteCounter < len(app.characters[character].winFrames):
                app.characters[character].drawWin(position[0], position[1], app.spriteCounter)
            else:
                app.characters[character].drawWin(position[0], position[1], 0)
        else:
            app.characters[character].draw(position[0], position[1], 0)

def playSelectAnimation(app, character):
    if app.stepCounter >= app.spriteCount:
        app.spriteCounter = (1 + app.spriteCounter) % len(character.winFrames)
        app.stepCounter = 0 

def select_onMouseMove(app,mouseX,mouseY):
    pass

#--Title Screen--------------------------------------------

def title_redrawAll(app):
    resizedView = app.titlescreen.resize((app.width,app.height))
    drawImage(CMUImage(resizedView),0,0,width =app.width,height = app.height)
    # once b is pressed display the 50cc and 100cc options
    if app.start:
        drawRect(app.width/2 - 50,app.height/2,100,60, opacity = 100)
        drawLabel('50 cc', app.width/2,app.height/2 +15,size =20,bold = True, fill = app.highlight50)
        drawLabel('100 cc', app.width/2,app.height/2 + 45,size =20,bold = True, fill = app.highlight100)
    # else display the press b message
    else:
        drawLabel('press b to start', app.width/2,app.height/2 + 50,size =20,bold = True, opacity = app.opacity % 100)
    
        
    

def title_onStep(app):
    # creates a fading word effect on title screen 
    if not app.start:
        app.opacity += 5
    

def title_onKeyPress(app, key):
    if key == 'b':
        app.start = True 
    if key =='space':
        setActiveScreen('select')

def title_onMousePress(app,mouseX,mouseY):
    # when clicking the buttons it will set it == to true which will determine the speed, you can't click both buttons
    if 275 < mouseX < 335 and app.start: 
        if 300 < mouseY < 330 and app.hundredcc != True:
            app.fiftycc = True
            app.stepsPerSecond = 30
            setActiveScreen('select')
        if 330 < mouseY < 360 and app.fiftycc != True:
            app.hundredcc = True
            app.stepsPerSecond = 30
            setActiveScreen('select')

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


