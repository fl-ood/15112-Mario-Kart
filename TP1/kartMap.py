from cmu_graphics import *
from PIL import Image
from PIL import ImageFilter
import math


def onAppStart(app):
    #Open map and scale to canvas size (could scale to some other size though)
    app.map = Image.open('images/marioKart.png')
    app.map = app.map.resize((app.width, app.height))
    app.map = app.map.convert('RGB')

    #Make a new image with a scaled down resolution
    app.scaleDown = 7 # Lower = better resolution, slower speed
    app.view = Image.new(mode='RGB', size=(app.width//app.scaleDown, app.height//app.scaleDown))

    #-------Sprite Stuff------
    app.sprite = Image.open('sprites/mario-3solo.png') # sprites come from The Spriters Resource
    app.w,app.h = app.sprite.size
    app.unit = app.w

    frame = app.sprite.crop((app.unit,0, app.unit, app.h))
    app.sprite = CMUImage(frame)

#(498,593) = x coord range for finish line
#325 = y value of the finish line
#-------------------
    #Start in perspective view w/spinning camera
    app.perspective = True
    app.spin = True

    #Set some values
    app.fov = 60

    #Car position
    app.x, app.y = 533, 345
    app.angle = 0

    #Camera position
    app.cameraHeight = 20

    #We can't quite go this fast, but we can try
    app.stepsPerSecond = 10
    app.barrierList = [(232,232,0),(0, 32, 248),(104,104,248),(232,0,0),(248,72,72),(0,128,0),(0,168,0),(0,208,0),(248,248,144),(96,248,96)]
    #Calculate the initial view
    makePerspective(app)
    
    
    
    
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


def onKeyPress(app,key):
    currPix = app.map.getpixel((app.x,app.y))
    if key == 'p': #p draws the map
        app.perspective = not app.perspective
    elif key == 'left': #left and right change the angle
        app.angle -= 5
    elif key == 'right':
        app.angle += 5
    elif key == '1': #s spins the camera
        app.spin = not app.spin
    

    elif currPix not in app.barrierList:
        # Check if the new position would be on a barrier
        if key == 's':
            new_pixel = app.map.getpixel((app.x, app.y + 5))
            if new_pixel not in app.barrierList:
                app.y += 5
        elif key == 'w':
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

def onStep(app):
    if app.spin:
        app.angle += 5
        makePerspective(app)
        
    else:
        if app.angle <= 180:
            app.sign = -1
        else:
            app.sign = 1
        
        
        # Update the position based on the mouse direction
        dx = 5 * math.cos(math.radians(app.angle))
        dy = 5 * math.sin(math.radians(app.angle))
        currPix = app.map.getpixel((app.x,app.y))
        if currPix not in app.barrierList:
            new_pixel = app.map.getpixel((app.x +dx, app.y + dy))
            if new_pixel not in app.barrierList:
                app.x += dx
                app.y += dy
    print(f'This is your coord {app.x,app.y}')
    

    makePerspective(app)
   
    


def onMouseMove(app,mouseX,mouseY):
    if app.spin == False:
        app.angle = mouseX
    
    


def redrawAll(app):
    if app.perspective:
        ## Draw the perspective view.  
        ## Unsure whether resizing with pil or cmuImage is faster
        resizedView = app.view.resize((app.width,app.height))
        #drawImage(CMUImage(app.image2),0,0, width = app.width, height = app.height)
        drawImage(CMUImage(resizedView),0,0)
        # drawImage(app.sprite,0, 0, align = 'center')

    else:
        drawImage(CMUImage(app.map),0,0)
        drawCircle(app.x, app.y, 4, fill='red')

def main():
    runApp(width=600, height=600)

if __name__ == '__main__':
    main()

# works but updates the image on the next key hold 
# def onKeyHold(app,keys):
#     currPix = app.map.getpixel((app.x,app.y))
#     if 'left' in keys: #left and right change the angle
#         app.angle -= 5
#     elif 'right' in keys:
#         app.angle += 5
#     if currPix not in app.barrierList:
#         pass
#     if 'up' in keys:
#         app.y += 5
#     elif 'down' in keys:
#         app.y -= 5
#     elif 'a' in keys:
#         app.x -= 5
#     elif 'd' in keys:
#         app.x += 5