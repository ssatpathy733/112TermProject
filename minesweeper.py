from cmu_graphics import *
from PIL import *
from random import *

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# BUILT-IN APP FUNCTIONS
# ---------------------------------------------------------------------------------------------
def onAppStart(app):
    app.rows = 10
    app.cols = 10
    app.boardLeft = 75 
    app.boardTop = 80
    app.boardWidth = 650
    app.boardHeight = 650
    app.width = 800
    app.height = 800
    app.cellBorderWidth = 2
    app.numMines = (app.rows * app.cols * 2) // 10
    app.flagsPlaced = set()
    app.flagsLeft = app.numMines - len(app.flagsPlaced) 
    app.mineLocations = []
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.field = dict()
    app.flagging = False
    app.uncover = False
    app.gameOver = False
    app.gameWon = False
    app.gameStart = False
    app.firstMineCoords = (-1, -1)
    app.oppositeMineCoords = (-1, -1)
    app.showTitle = True
    app.showAboutGame = False
    app.showHowToPlay = False
    app.firstStart = True
    app.cInfo = 50
    app.cHowTo = app.width - 50
    app.cR = 30
    app.currHelperMove = False
    app.currMode = "NONE"
    app.rButtonLeft = 10
    app.rButtonTop = app.width - 60
    app.sButtonLeft = app.width // 2 - 60
    app.sButtonTop = app.height // 2 + 25
    app.rButtonWidth = 120
    app.rButtonHeight = 50
    app.catImage = Image.open('catPic.PNG') # photo credit - my friend's cat
    app.catImage = CMUImage(app.catImage)

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=rgb(151, 182, 232))
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight, fill=rgb(77, 63, 107))
    drawLabel("MINESWEEPER!", app.width // 2, 20, align="center", size = 45, fill="white", border=rgb(77, 63, 107), font="grenze")
    drawLabel(f"FLAGS LEFT: {app.flagsLeft}", app.width // 2, 55, align="center", fill="white", size = 25, font="script")
    drawBoard(app)
    drawBoardBorder(app)
    drawCurrMode(app)
    if app.gameStart == True and app.showTitle == False:
        drawField(app)
    if app.gameWon == True:
        winCondition(app)
    drawRestartButton(app)
    if app.gameOver == True:
        lossCondition(app)
    if app.showTitle == True:
        drawTitleCard(app)
    if app.showAboutGame == True:
        aboutGame(app)
    if app.showHowToPlay == True:
        howToPlay(app)
    drawCircle(app.cInfo, app.cInfo, app.cR, fill=rgb(77, 63, 107), border="white")
    drawLabel("!", app.cInfo, app.cInfo, fill="white", size = 20)
    drawCircle(app.cHowTo, app.cInfo, app.cR, fill=rgb(77, 63, 107), border="white")
    drawLabel("?", app.cHowTo, app.cInfo, fill="white", size = 20)
    
    

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# DRAWING THE BOARD
# these functions were based on the grid functions we did for Tetris in class
# ---------------------------------------------------------------------------------------------
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            color = app.board[row][col]
            drawCell(app, row, col, color)

def drawBoardBorder(app):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='white',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='white',
             borderWidth=app.cellBorderWidth)
    

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# BOX CLASSES
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# MINE CLASS
# ---------------------------------------------------------------------------------------------
class Mine:
    def __init__(self, locX, locY):
        self.locX = locX
        self.locY = locY
        self.state = "covered"
        self.flagStatus = True

    def __repr__(self):
        return (f"Mine - {self.locX, self.locY}")

    def __eq__(self, other):
        if not (isinstance(other, Safe) or isinstance(other, Mine)):
            return False
        return (self.locX == other.locX) and (self.locY == other.locY)

    def __hash__(self):
        return hash(str(self))

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state
    
    def canFlag(self):
        return self.flagStatus
    
    def changeFlagState(self, status):
        self.flagStatus = status
# ---------------------------------------------------------------------------------------------
# SAFE CLASS
# ---------------------------------------------------------------------------------------------
class Safe:
    def __init__(self, locX, locY):
        self.locX = locX
        self.locY = locY
        self.state = "covered"
        self.flagStatus = True

    def __repr__(self):
        return (f"Safe - {self.locX, self.locY}")

    def __eq__(self, other):
        if not (isinstance(other, Safe) or isinstance(other, Mine)):
            return False
        return (self.locX == other.locX) and (self.locY == other.locY)

    def __hash__(self):
        return hash(str(self))
    
    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state
    
    def canFlag(self):
        return self.flagStatus
    
    def changeFlagState(self, status):
        self.flagStatus = status
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# CREATING THE FIELD
# ---------------------------------------------------------------------------------------------
def minePlacement(app):
    if app.showTitle == False:
        (firstX, firstY) = app.firstMineCoords 
        (otherX, otherY) = app.oppositeMineCoords 
        for col in range(min(firstX, otherX), max(firstX, otherX) + 1):
            for row in range(min(firstY, otherY), max(firstY, otherY) + 1):
                app.field[(row, col)] = Safe(col, row)
        while len(app.mineLocations) < app.numMines:
            randRow = randrange(0, app.cols)
            randCol = randrange(0, app.rows)
            if not (randRow, randCol) in app.field and not (randRow, randCol) in app.mineLocations:
                (app.mineLocations).append((randRow, randCol))
        return app.mineLocations

def createField(app):
    if app.showTitle == False:
        for locationX, locationY in app.mineLocations:
            app.field[(locationX, locationY)] = Mine(locationX, locationY)
        for row in range(app.cols):
            for col in range(app.rows):
                if not (row, col) in app.field:
                    app.field[(row, col)] = Safe(row, col)

def drawField(app):
    if app.showTitle == False:
        for row in range(app.rows):
            for col in range(app.cols):
                theFont = "arial"
                theSize = 60
                color = "white"
                if (app.field[(col, row)]).getState() == ("flagged"):
                    label = "O"
                    color = rgb(239, 56, 245)
                    theSize = 60
                elif (app.field[(col, row)]).getState() == ("covered"):
                    label = ""
                else: # uncovered
                    app.board[row][col] = rgb(163, 110, 204)
                    if (col, row) in app.mineLocations:
                        label = "O"
                        color = "red"
                        theSize = 60
                    else:
                        label = determineNumber(app, row, col)
                        if label == 0:
                            label = ""
                    
                cellLeft, cellTop = getCellLeftTop(app, row, col)
                cellWidth, cellHeight = getCellSize(app)
                drawLabel(label, cellLeft + (cellWidth / 2), cellTop + (cellHeight / 2), align = "center", fill=color, font=theFont, size=theSize)
    
def isLegalDirection(app, dX, dY, originalX, originalY):
    newX = originalX + dX
    newY = originalY + dY
    if ((newX < 0 or newX > app.cols) or (newY < 0 or newY > app.rows)):
        return False
    return True

def isLegalRow(app, dX, originalX):
    newX = originalX + dX
    if newX < 0 or newX > app.cols:
        return False
    return True

def isLegalCol(app, dY, originalY):
    newY = originalY + dY
    if newY < 0 or newY > app.rows:
        return False
    return True

def determineNumber(app, currRow, currCol):
    directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    count = 0
    for dX, dY in directions:
        if isLegalDirection(app, dX, dY, currRow, currCol):
            locationY, locationX = currRow + dX, currCol + dY
            if (locationX, locationY) in app.mineLocations:
                count += 1
    return count
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# FLOOD FILL (BASED HEAVILY ON CS ACADEMY TUTORIAL)
# ---------------------------------------------------------------------------------------------

def floodFill(app, row, col, oldValue, newValue):
    if ((row < 0) or (row >= app.cols) or
        (col < 0) or (col >= app.rows)):
        return
    oldValue = app.field[(col, row)].getState()
    newValue = "uncovered"
    if oldValue == "covered":
        app.field[(col, row)].setState("uncovered")
    else:
        return
    
    if ((row < 0) or (row >= app.cols) or
        (col < 0) or (col >= app.rows) or
        (determineNumber(app, row, col) != 0)):
        app.board[row][col] = rgb(163, 110, 204)
        return 
    else: 
        oldValue = app.field[(col, row)].getState()
        app.board[row][col] = rgb(163, 110, 204)
        newValue = "uncovered"
        floodFill(app, row-1, col, oldValue, newValue)
        floodFill(app, row+1, col, oldValue, newValue) 
        floodFill(app, row, col-1, oldValue, newValue) 
        floodFill(app, row, col+1, oldValue, newValue)
        floodFill(app, row+1, col+1, oldValue, newValue)
        floodFill(app, row-1, col-1, oldValue, newValue)
        floodFill(app, row-1, col+1, oldValue, newValue)
        floodFill(app, row+1, col-1, oldValue, newValue)

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# MOUSE/KEY FUNCTIONS
# ---------------------------------------------------------------------------------------------
def onMousePress(app, mouseX, mouseY):
    if checkIfStart(app, mouseX, mouseY):
        app.showTitle = False
    if checkIfRestart(app, mouseX, mouseY):
        restartGame(app)
    if app.gameOver == False and app.showAboutGame == False and app.showHowToPlay == False:
        if app.firstStart == True:
            restartGame(app)
        if (mouseX > app.boardLeft and mouseX < app.boardLeft + app.boardWidth and mouseY > app.boardTop and mouseY < app.boardTop + app.boardHeight):
            xVal, yVal = getBoxToClick(app, mouseX, mouseY)
            if app.gameStart == False:
                directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
                for dX, dY in directions:
                    if isLegalDirection(app, dX, dY, xVal, yVal):
                        locationY, locationX = xVal + dX, yVal + dY
                        app.field[(locationY, locationX)] = Safe(locationY, locationX)
                firstClick(app, xVal, yVal)
                app.gameStart = True
            if app.flagging == True and app.field[(xVal, yVal)].canFlag():
                if app.field[(xVal, yVal)].getState() == "flagged":
                    (app.field[(xVal, yVal)]).setState("covered")
                    (app.flagsPlaced).remove((xVal, yVal))
                else:
                    (app.field[(xVal, yVal)]).setState("flagged")
                    (app.flagsPlaced).add((xVal, yVal))
                app.flagging = False
                app.currMode = "NONE"
            if app.uncover == True and (app.field[(xVal, yVal)]).getState() != "flagged" :
                app.board[yVal][xVal] = rgb(163, 110, 204)
                if (app.field[(xVal, yVal)]).getState() != "flagged":
                    col, row = yVal, xVal
                    if determineNumber(app, col, row) == 0:
                        oldValue = app.field[(xVal, yVal)].getState()
                        newValue = "uncovered"
                        floodFill(app, col, row, oldValue, newValue)
                    (app.field[(xVal, yVal)]).setState("uncovered")
                    (app.field[(xVal, yVal)]).changeFlagState(False)
                    app.uncover == False
                    if (xVal, yVal) in app.mineLocations:
                        app.gameOver = True
            app.flagsLeft = app.numMines - len(app.flagsPlaced) 
        count = 0
        for theX, theY in set(app.mineLocations):
            if (theX, theY) in set(app.flagsPlaced):
                count += 1
        if count == app.numMines:
            app.gameWon = True
        # app.firstStart = False
    if distance(app.cInfo, app.cInfo, mouseX, mouseY) <= app.cR:
        app.showAboutGame = not app.showAboutGame
    if distance(app.cHowTo, app.cInfo, mouseX, mouseY) <= app.cR:
        app.showHowToPlay = not app.showHowToPlay
    

def onKeyHold(app, keys):
    if app.gameOver == False:
        if app.showTitle == True:
            restartGame(app)
        if len(keys) == 1 and "f" in keys:
            app.uncover = False
            app.currMode = "FLAGGING!"
            app.flagging = True
        elif len(keys) == 1 and "u" in keys:
            app.flagging = False
            app.currMode = "UNCOVERING!"
            app.uncover = True

def onKeyPress(app, key):
    if app.gameOver == False:
        if app.firstStart == True:
            restartGame(app)
            app.firstStart = False
    if "f" == key:
            app.uncover = False
            app.currMode = "FLAGGING!"
            app.flagging = True
    elif "u" == key:
            app.flagging = False
            app.currMode = "UNCOVERING!"
            app.uncover = True

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# MOUSE HELPER FUNCTIONS
# ---------------------------------------------------------------------------------------------
def getBoxToClick(app, mouseX, mouseY):
    xVal = (mouseX - app.boardLeft) // (app.boardWidth // app.cols)
    yVal = (mouseY - app.boardTop) // (app.boardHeight  // app.rows)
    return xVal, yVal

def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# EXTRA FUNCTIONS
# ---------------------------------------------------------------------------------------------

def firstClick(app, clickX, clickY):
    if app.showTitle == False:
        firstMineX = None
        firstMineY = None
        while firstMineX == None:
            toAddX = randrange(-1*(app.cols // 5), app.cols // 5)
            if toAddX != 0 and isLegalCol(app, toAddX, clickX):
                firstMineX = clickX + toAddX
        while firstMineY == None:
            toAddY = randrange(-1*(app.rows // 5), app.rows // 5)
            if toAddY != 0 and isLegalCol(app, toAddY, clickY):
                firstMineY = clickY + toAddY
        app.firstMineCoords = (firstMineX, firstMineY)
        otherMineX = None
        otherMineY = None
        if (clickX + (-1 * firstMineX)) < 0:
            otherMineX = 0
        elif (clickX + (-1 * firstMineX)) > app.cols:
            otherMineX = 0
        else:
            otherMineX = clickX + (-1 * firstMineX)
        if (clickX + (-1 * firstMineX)) < 0:
            otherMineY = 0
        elif (clickX + (-1 * firstMineX)) > app.rows:
            otherMineY = 0
        else:
            otherMineY = (clickX + (-1 * firstMineX))
        app.oppositeMineCoords = (otherMineX, otherMineY)
        minePlacement(app)
        createField(app)
        app.gameStart = True

def drawCurrMode(app):
    drawLabel(f"CURRENT MODE: {app.currMode}", app.width // 2, app.height - 40, fill = "white", size = 20, align = "center")

def drawRestartButton(app):
    drawRect(app.rButtonLeft, app.rButtonTop, app.rButtonWidth, app.rButtonHeight, fill=rgb(77, 63, 107), border="white")
    drawLabel("RESTART", (app.rButtonLeft + app.rButtonWidth // 2), (app.rButtonTop + app.rButtonHeight // 2), align = "center", fill="white", size = 20)

def checkIfRestart(app, xValue, yValue):
    if (xValue >= app.rButtonLeft and xValue <= (app.rButtonLeft + app.rButtonWidth)):
        if (yValue >= app.rButtonTop and yValue <= (app.rButtonTop + app.rButtonHeight)):
            return True
    return False

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# WIN/LOSS/INFO CARD FUNCTIONS
# ---------------------------------------------------------------------------------------------
def winCondition(app):
    drawImage(app.catImage,app.width/2,app.height/2, align='center')
    drawRect(app.width // 2, app.height // 4, app.width*3 // 4, app.height*1 // 4, fill = "purple", opacity = 75, align = "center")
    drawLabel("yaey u won have this pic of sparky", app.width // 2, app.height // 4, fill = "white", size = 20, align = "center")
    

def lossCondition(app):
    drawRect(app.width // 2, app.height // 2, app.width*3 // 4, app.height*3 // 4, fill = "blue", opacity = 75, align = "center")
    drawLabel("oopsie poopsie u lost", app.width // 2, app.height // 2, fill = "white", size = 20, align = "center")

def aboutGame(app):
    labelLines = ["this game was brought to you by", "BLOOD, SWEAT & TEARS", 
                  "also known as", "BACKTRACKING,", "OOP &", "CMU_GRAPHICS", 
                  "(jk it wasn't actually thaaaaat bad)", 
                  "anyway i put a lot of time and effort into this", 
                  "pls enjoy", "pls don't poop on the project", "have fun!!!"]
    
    drawRect(app.width // 2, app.height // 2, app.width*3 // 4, app.height*3 // 4, fill = "purple", opacity = 90, align = "center")
    for label in range(len(labelLines)):
        drawLabel(labelLines[label], app.width // 2, (app.height // 2 - 200) + (label * 40), fill = "white", size = 30, align = "center", font="cursive", bold=True)

def howToPlay(app):
    labelLines = ["minesweeper is super fun!", "but how do you play you ask?", 
                  "you must place flags on all of the mines", 
                  "so you know not to click on them", 
                  "don't blow up the field pls :(", 
                  "the numbers tell you how many mines are in", 
                  "the boxes immediately surrounding a box", 
                  "press 'u' to uncover boxes", "press and hold 'f' to flag", 
                  "you must unflag before uncovering", "have fun!!!"]
    drawRect(app.width // 2, app.height // 2, app.width*3 // 4, app.height*3 // 4, fill = "purple", opacity = 90, align = "center")
    for label in range(len(labelLines)):
        drawLabel(labelLines[label], app.width // 2, (app.height // 2 - 200) + (label * 40), fill = "white", size = 30, align = "center", font="cursive", bold=True)

def drawTitleCard(app):
    drawRect(0, 0, app.width, app.height, fill=rgb(151, 182, 232))
    drawLabel("MINESWEEPER!", app.width // 2, app.height // 2 - 30, align="center", size = 80, fill="white", border=rgb(77, 63, 107), font="grenze")
    drawStartButton(app)

def drawStartButton(app):
    drawRect(app.sButtonLeft, app.sButtonTop, app.rButtonWidth, app.rButtonHeight, fill=rgb(77, 63, 107), border="white")
    drawLabel("START",  app.width // 2, app.height // 2 + 50, align = "center", fill="white", size = 20)

def checkIfStart(app, xValue, yValue):
    if (xValue >= app.sButtonLeft and xValue <= (app.sButtonLeft + app.rButtonWidth)):
        if (yValue >= app.sButtonTop and yValue <= (app.sButtonTop + app.rButtonHeight)):
            return True
    return False

def restartGame(app):
    app.flagsPlaced = set()
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.field = dict()
    app.flagging = False
    app.uncover = False
    app.gameOver = False
    app.gameWon = False
    app.gameStart = False
    app.firstMineCoords = (-1, -1)
    app.oppositeMineCoords = (-1, -1)
    app.showAboutGame = False
    app.showHowToPlay = False
    app.hintCount = 0
    app.currHelperMove = False
    app.currMode = "NONE"
    app.numMines = (app.rows * app.cols * 2) // 10
    app.flagsPlaced = set()
    app.flagsLeft = app.numMines - len(app.flagsPlaced) 
    app.mineLocations = []

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

def main():
    runApp()
    

main()
