from cmu_graphics import *
from PIL import Image
from PIL import ImageFilter
import math

class Map():
    #mapimage will be the path to the map image

    def __init__(self,mapimage,x,y,scale,cameraHeight,angle,fov,barriers):
        #Open map and scale to canvas size (could scale to some other size though)
        self.image = Image.open(mapimage)
        self.image = app.map.resize((app.width, app.height))
        self.image = app.map.convert('RGB')

        #Make a new image with a scaled down resolution
        self.scaleDown = 7 # Lower = better resolution, slower speed
        # perspective will be the 2.5D image
        self.perspective = Image.new(mode='RGB', size=(app.width//app.scaleDown, app.height//app.scaleDown))
        
        #Start in perspective view w/spinning camera
        self.p = True
        self.spin = True

        #Set some values
        self.fov = fov

        #Car position
        self.x, self.y = x, y
        self.angle = angle

        #Camera position
        self.cameraHeight = cameraHeight

        
        self.barriers = barriers
        #Calculate the initial view
        
        

        #This function finds a pixel on the map along a line of sight
    def makePerspective(self):
        #Scan left to right
        
        for x in range(self.perspective.width): 
            yaw = (x/self.perspective.width) * self.fov - (self.fov/2)  #[-30, -29... 0 ... 29 30]
            dxScale = math.cos((self.angle+yaw)*math.pi/180)
            dyScale = math.sin((self.angle+yaw)*math.pi/180)

            #Scan top to bottom
            for y in range(self.perspective.height): 
                pitch = (1 - y/self.perspective.height)*90
                dist = self.cameraHeight * math.tan(pitch*math.pi/180)
                
                dx = dist*dxScale
                dy = dist*dyScale
                fx = self.x + dx
                fy = self.y + dy
                #fx = max(0, min(app.map.width-1, fx))
                #fy = max(0, min(app.map.height-1, fy))
                if 0 <= fx < self.image.width and 0 <= fy < self.mapimage.height:
                    r,g,b = self.image.getpixel((fx,fy))
                    self.perspective.putpixel((x,y),(r,g,b))
                else:
                    ## If we're looking off the map, just make the pixel blue
                    self.perspective.putpixel((x,y),(100,100,255))
        # app.view = app.view.filter(ImageFilter.EMBOSS)

    