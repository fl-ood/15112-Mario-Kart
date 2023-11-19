from cmu_graphics import *
from PIL import Image
import os, pathlib
import numpy, math

#See: https://pillow.readthedocs.io/en/stable/reference/Image.html 

def onAppStart(app):
    app.drawTransform = True

    # Open image from local directory
    app.image = Image.open("marioKart.png")
    
    # If the above line displays the error
    # FileNotFoundError: [Errno 2] No such file or directory: 'images/Caaaaat.jpg'
    # it is because PIL is looking for the file
    # in the directory Python is installed in.
    # Instead, either use absolute file path 
    # or comment out the line above and use the line below.
    
    #app.image = Image.open(os.path.join(pathlib.Path(__file__).parent,"marioKart.png"))
    
    # Note that you need to "import os, pathlib" for this to work!
    # If this is the solution that works on your operating system,
    # I recommend defining a custom function to open images as such:
    
    # def openImage(fileName):
    #     return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))
    # app.image = openImage("marioKart.png")

    app.image = app.image.resize((app.width, app.height))

    xShift = 10000
    yShift = 0
    x = 725
    y = 600

    #This correction seems necessary for some reason, but I'm not doing the math particularly well
    x = app.width/2-x
    y = app.height-y

    
    angle = 0
    #See https://stackoverflow.com/questions/53032270/perspective-transform-with-python-pil-using-src-target-coordinates
    #This function takes 8 points: four starting points and four destination points
    coeffs = find_coeffs(
        [(0-x, 0-y), (app.width-x, 0-y), (app.width-x, app.height-y), (0-x, app.height-y)],
        [(0, 0-yShift), (app.width, 0-yShift), (app.width+xShift, app.height), (0-xShift, app.height)])
    
    #rotationcoeffs = find_rotation_coeffs(30,x,y)
    
    #newcoeffs = find_coeffs(
        #[(0-x, 0-y), (app.width-x, 0-y), (app.width-x, app.height-y), (0-x, app.height-y)], rotationcoeffs)
    
    app.transformedImage = app.image.transform((800, 800), Image.PERSPECTIVE,
        coeffs, Image.BICUBIC)
    
    # app.transformedImage2 = app.image.transform((800, 800), Image.PERSPECTIVE,
        # newcoeffs, Image.BICUBIC)
    # Cast image type to CMUImage to allow for faster drawing
    app.image = CMUImage(app.image)

    app.transformedImage = CMUImage(app.transformedImage)
    # app.transformedImage2 = CMUImage(app.transformedImage2)

def find_coeffs(source_coords, target_coords):
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0]*t[0], -s[0]*t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1]*t[0], -s[1]*t[1]])
    A = numpy.matrix(matrix, dtype=float)
    B = numpy.array(source_coords).reshape(8)
    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

def find_rotation_coeffs(theta, x0, y0):
    ct = math.cos(theta)
    st = math.sin(theta)
    return numpy.array([ct, -st, x0*(1-ct) + y0*st, st, ct, y0*(1-ct)-x0*st,0,0])

def onMousePress(app, x, y):
    app.drawTransform = not app.drawTransform

def onKeyPress(app, key):
    pass
    # app.drawTransform = not app.drawTransform

def redrawAll(app):
    if app.drawTransform:
        drawImage(app.transformedImage,app.width/2, app.height/2, align='center')
    else:
        pass
        #drawImage(app.transformedImage2,app.width/2, app.height/2, align='center')
        drawImage(app.image,app.width/2, app.height/2, align='center')

def main():
    runApp(width=800,height=800)

if __name__ == '__main__':
    main()