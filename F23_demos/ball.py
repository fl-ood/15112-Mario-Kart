from cmu_graphics import *
import random

def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

class Ball:
    def __init__(self, x, y):
        #Position
        self.x = x
        self.y = y

        #Velocity
        self.dx = random.randint(-10, 10)
        self.dy = -3

        #Acceleration
        self.ddx = 0
        self.ddy = 0.1

    def draw(self):
        drawCircle(self.x, self.y, 20, fill = 'red')

    def step(self):
        #Integrate position and velocity
        self.x += self.dx
        self.y += self.dy
        self.dx += self.ddx
        self.dy += self.ddy

        #Simple bounce (with some bugs, which you should find and fix)
        if self.x < 0 or self.x > 600: 
            self.dx *= -1

        if self.y < 0 or self.y > 600:
            self.dy *= -1


#---Animation functions---------------------------------
def onAppStart(app):
    app.ballList = [Ball(300, 300)]

def onMousePress(app, mouseX, mouseY):
    app.ballList.append(Ball(mouseX, mouseY))

def onStep(app):
    for ball in app.ballList:
        ball.step()

def redrawAll(app):
    for ball in app.ballList:
        ball.draw()

runApp(width = 600, height = 600)