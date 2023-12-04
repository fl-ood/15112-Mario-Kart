import numpy as np
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
    app.scaleDown = 2 # Lower = better resolution, slower speed
    app.view = Image.new(mode='RGB', size=(app.width//app.scaleDown, app.height//app.scaleDown))

    

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
    # Convert the image to a numpy array
    map_array = np.array(app.map)

    # Create a grid of x and y coordinates
    x, y = np.meshgrid(np.arange(app.view.width), np.arange(app.view.height))

    # Calculate yaw and pitch for each pixel
    yaw = (x / app.view.width) * app.fov - (app.fov / 2)
    pitch = (1 - y / app.view.height) * 90

    # Calculate distances and final x and y coordinates
    dist = app.cameraHeight * np.tan(pitch * np.pi / 180)
    dx = dist * np.cos((app.angle + yaw) * np.pi / 180)
    dy = dist * np.sin((app.angle + yaw) * np.pi / 180)
    fx = (app.x + dx).astype(int)
    fy = (app.y + dy).astype(int)

    # Create a mask of valid coordinates
    mask = (0 <= fx) & (fx < app.map.width) & (0 <= fy) & (fy < app.map.height)

    # Use the mask to index into the original image array
    view_array = np.zeros((app.view.height, app.view.width, 3), dtype=int)
    view_array[mask] = map_array[fy[mask], fx[mask]]

    # Handle off-map pixels
    view_array[~mask] = [100, 100, 255]

    # Convert the final array back to an image
    app.view = Image.fromarray(view_array.astype('uint8'), 'RGB')


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
