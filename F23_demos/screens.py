# Screen demo
# mdtaylor 4/18

from cmu_graphics import *
import random

def onAppStart(app):
    print('We recommend only one onAppStart!')
    app.x = 100
    app.y = 200
    app.dx = random.randint(-10, 10)
    app.dy = random.randint(-10, 10)
    app.r = 15

#---------------------------------------------------

def welcome_redrawAll(app):
    drawLabel("Welcome to The Game", app.width/2, app.height/2, size = 24)

def welcome_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('game')

#---------------------------------------------------


def game_onStep(app):
    app.x += app.dx
    app.y += app.dy
    app.x = app.x%app.width
    app.y = app.y%app.height

def game_redrawAll(app):
    drawCircle(app.x, app.y, app.r, fill = 'purple')

def game_onKeyPress(app, key):
    if key == 'r':
        setActiveScreen('welcome')
    elif key == 'p':
        setActiveScreen('pause')
    else:
        app.dx = random.randint(-10, 10)
        app.dy = random.randint(-10, 10)
#---------------------------------------------------

def pause_onKeyPress(app, key):
    if key=='p':
        setActiveScreen('game')

def pause_redrawAll(app):
    drawCircle(app.x, app.y, app.r, fill = 'purple')
    drawLabel('PAUSED!', app.width/2, app.height/2)

#---------------------------------------------------

# Your screen names should be strings
runAppWithScreens(initialScreen='welcome')