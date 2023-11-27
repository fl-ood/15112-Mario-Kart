from cmu_graphics import *
from PIL import Image
import os, pathlib

#See: https://pillow.readthedocs.io/en/stable/reference/Image.html 

def onAppStart(app):
    # Open image from local directory
    app.image = Image.open("images/Caaaaat.jpg")
    app.image = app.image.resize((400, 400))
    
    # Cast image type to CMUImage to allow for faster drawing
    app.image = CMUImage(app.image)
    app.angle = 0

def onStep(app):
    app.angle += 5

def redrawAll(app):
    # drawPILImage takes in a PIL image object and the left-top coordinates
    drawImage(app.image,app.width/2,app.height/2, align = 'center', 
                rotateAngle = app.angle)

def main():
    runApp(width=800,height=800)

if __name__ == '__main__':
    main()