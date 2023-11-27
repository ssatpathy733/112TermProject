from cmu_graphics import *
from PIL import *
from random import *

# flood fill
# 3 difficulties

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# BUILT-IN APP FUNCTIONS
# ---------------------------------------------------------------------------------------------
def onAppStart(app):
    app.rows = 6
    app.cols = 5
    app.boardLeft = 75 
    app.boardTop = 50
    app.boardWidth = 250
    app.boardHeight = 300
    app.cellBorderWidth = 2
    app.numMines = (app.rows * app.cols * 2) // 5
    app.mineLocations = []
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.field = dict()
    app.flagging = False
    app.uncover = False
    app.gameover = False
    minePlacement(app)
    createField(app)


def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill="blue")
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight, fill="purple")
    drawBoard(app)
    drawBoardBorder(app)
    drawField(app)
    # determineNumber(app, 2, 2)

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
            if (row, col) in app.field:
                label = determineNumber(app, row, col)
                

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
    while len(app.mineLocations) < app.numMines:
        randRow = randrange(0, app.cols)
        randCol = randrange(0, app.rows)
        if not (randRow, randCol) in app.mineLocations:
            (app.mineLocations).append((randRow, randCol))
    print(app.mineLocations)
    return app.mineLocations

def createField(app):
    for locationY, locationX in app.mineLocations:
        app.field[(locationX, locationY)] = Mine(locationX, locationY)
    for row in range(app.rows):
        for col in range(app.cols):
            if not (row, col) in app.mineLocations:
                app.field[(col, row)] = Safe(col, row)
    print(app.field)

def drawField(app):
    for row in range(app.rows):
        for col in range(app.cols):
            # print((app.field[(row, col)]).getState())
            if (app.field[(col, row)]).getState() == ("flagged"):
                label = "F"
            elif (app.field[(col, row)]).getState() == ("covered"):
                label = "X"
            else:
                if isinstance(app.field[(row, col)], Mine):
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

def determineNumber(app, currRow, currCol):
    directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    count = 0
    for dX, dY in directions:
        if isLegalDirection(app, dX, dY, currRow, currCol):
            locationX, locationY = currRow + dX, currCol + dY
            if (locationX, locationY) in app.field and isinstance(app.field[(locationX, locationY)], Mine):
                count += 1
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
    if app.gameover == False:
        if (mouseX > app.boardLeft and mouseX < app.boardLeft + app.boardWidth and mouseY > app.boardTop and mouseY < app.boardTop + app.boardHeight):
            xVal, yVal = getBoxToClick(app, mouseX, mouseY)
            print(xVal, yVal)
            if app.flagging == True:
                print(app.field[(xVal, yVal)])
                (app.field[(xVal, yVal)]).setState("flagged")
                print((app.field[(xVal, yVal)]).getState())
                app.flagging = False
            if app.uncover == True:
                (app.field[(xVal, yVal)]).setState("uncovered")
                app.uncover == False
                if (xVal, yVal) in app.mineLocations:
                    app.gameover = True
                    print("oops")


def onKeyHold(app, keys):
    if app.gameover == False:
        if len(keys) == 1 and "f" in keys:
            app.uncover = False
            app.flagging = True
        elif len(keys) == 1 and "u" in keys:
            app.uncover = True
        #     app.flagging = False
        # print(app.flagging)

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

def main():
    runApp()
    print(app.mineLocations)
    

main()
