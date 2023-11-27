from cmu_graphics import *

class Text:
    def __init__(self, label):
        self.label = label
    def draw(self, app):
        drawLabel(self.label, app.width//2, app.height//2)

def onAppStart(app):
    app.text = Text("112 is cool")

def redrawAll(app):
    app.text.draw(app)

runApp()