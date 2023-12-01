from cmu_graphics import *
from PIL import *
from random import *

# flood fill
# 3 difficulties
# fix determine number tomorrow!

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# BUILT-IN APP FUNCTIONS
# ---------------------------------------------------------------------------------------------
def onAppStart(app):
    app.rows = 12
    app.cols = 10
    app.boardLeft = 75 
    app.boardTop = 80
    app.boardWidth = 650
    app.boardHeight = 650
    app.width = 800
    app.height = 800
    app.cellBorderWidth = 2
    app.numMines = (app.rows * app.cols * 2) // 5
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
    app.oppositeBoundCoords = (-1, -1)
    # minePlacement(app)
    # createField(app)

def firstClick(app, clickX, clickY):
    firstMineX = None
    firstMineY = None
    while firstMineX == None:
        toAddX = randrange(-1*(app.cols // 3), app.cols // 3)
        if isLegalCol(app, toAddX, clickX):
            firstMineX = clickX + toAddX
    while firstMineY == None:
        toAddY = randrange(-1*(app.rows // 3), app.rows // 3)
        if isLegalCol(app, toAddY, clickY):
            firstMineY = clickY + toAddY
    # print(firstMineX, firstMineY)
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
    app.OppositeMineCoords = (otherMineX, otherMineY)
    print(app.firstMineCoords)
    print(app.OppositeMineCoords)
    minePlacement(app)
    createField(app)
    app.gameStart = True

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=rgb(151, 182, 232))
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight, fill=rgb(77, 63, 107))
    drawLabel("MINESWEEPER!", app.width // 2, 20, align="center", size = 45, fill="white", border=rgb(77, 63, 107))
    drawLabel(f"Flags left: {app.flagsLeft}", app.width // 2, 55, align="center", fill="white", size = 25)
    drawBoard(app)
    drawBoardBorder(app)
    if app.gameStart == True:
        drawField(app)
    if app.gameWon == True:
        winCondition(app)
    if app.gameOver == True:
        lossCondition(app)

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
# CREATING THE FIELD
# ---------------------------------------------------------------------------------------------
def minePlacement(app):
    firstX, firstY = app.firstMineCoords 
    otherX, otherY = app.oppositeBoundCoords 
    while len(app.mineLocations) < app.numMines:
        randRow = randrange(0, app.cols)
        randCol = randrange(0, app.rows)
        if (((randRow < firstX and randRow > otherX) or (randRow > firstX and randRow < otherX)) 
            and ((randCol < firstY and randCol > otherY) or (randCol > firstY and randCol < otherY))): 
            if not (randRow, randCol) in app.mineLocations:
                (app.mineLocations).append((randRow, randCol))
    print(app.mineLocations)
    return app.mineLocations

def createField(app):
    for locationX, locationY in app.mineLocations:
        app.field[(locationX, locationY)] = Mine(locationX, locationY)
    for row in range(app.cols):
        for col in range(app.rows):
            if not (row, col) in app.field:
                app.field[(row, col)] = Safe(row, col)
    print(app.field)

def drawField(app):
    for row in range(app.rows):
        for col in range(app.cols):
            # print((app.field[(row, col)]).getState())
            if (app.field[(col, row)]).getState() == ("flagged"):
                label = "F"
            elif (app.field[(col, row)]).getState() == ("covered"):
                label = ""
            else:
                if (col, row) in app.mineLocations:
                    label = "No"
                else:
                    label = determineNumber(app, row, col)
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellWidth, cellHeight = getCellSize(app)
            drawLabel(f"{label}", cellLeft + (cellWidth / 2), cellTop + (cellHeight / 2), align = "center", fill="white")
    
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
                # print(f"the locations {(locationX, locationY)}")
    return count
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
# ---------------------------------------------------------------------------------------------
# SAFE CLASS
# ---------------------------------------------------------------------------------------------
class Safe:
    def __init__(self, locX, locY):
        self.locX = locX
        self.locY = locY
        self.state = "covered"

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
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# MOUSE/KEY FUNCTIONS
# ---------------------------------------------------------------------------------------------
def onMousePress(app, mouseX, mouseY):
    if app.gameOver == False:
        if (mouseX > app.boardLeft and mouseX < app.boardLeft + app.boardWidth and mouseY > app.boardTop and mouseY < app.boardTop + app.boardHeight):
            xVal, yVal = getBoxToClick(app, mouseX, mouseY)
            if app.gameStart == False:
                firstClick(app, xVal, yVal)
                app.gameStart = True
            # print(xVal, yVal)
            if app.flagging == True:
                print(app.field[(xVal, yVal)])
                (app.field[(xVal, yVal)]).setState("flagged")
                print((app.field[(xVal, yVal)]).getState())
                (app.flagsPlaced).add((xVal, yVal))
                app.flagging = False
            if app.uncover == True:
                if (app.field[(xVal, yVal)]).getState() == "flagged":
                    app.flagsPlaced.remove((xVal, yVal))
                (app.field[(xVal, yVal)]).setState("uncovered")
                app.uncover == False
                if (xVal, yVal) in app.mineLocations:
                    app.gameOver = True
                    print("oops")
            app.flagsLeft = app.numMines - len(app.flagsPlaced) 
        count = 0
        for theX, theY in set(app.mineLocations):
            if (theX, theY) in set(app.flagsPlaced):
                count += 1
        if count == app.numMines:
            app.gameWon = True

def onKeyHold(app, keys):
    if app.gameOver == False:
        if len(keys) == 1 and "f" in keys:
            app.uncover = False
            app.flagging = True
        elif len(keys) == 1 and "u" in keys:
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

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# WIN/LOSS/INFO CARD FUNCTIONS
# ---------------------------------------------------------------------------------------------
def winCondition(app):
    drawRect(app.width // 2, app.height // 2, app.width*3 // 4, app.height*3 // 4, fill = "purple", opacity = 75, align = "center")
    drawLabel("yaey u won have this kitty", app.width // 2, app.height // 2, fill = "white", size = 20, align = "center")

def lossCondition(app):
    drawRect(app.width // 2, app.height // 2, app.width*3 // 4, app.height*3 // 4, fill = "blue", opacity = 75, align = "center")
    drawLabel("oopsie poopsie u lost", app.width // 2, app.height // 2, fill = "white", size = 20, align = "center")

def aboutGame(app):
    pass

def howToPlay(app):
    pass
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

def main():
    runApp()
    print(app.mineLocations)
    

main()
