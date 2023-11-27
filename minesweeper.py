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

def redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)
    minePlacement(app)
    createField(app)
    determineNumber(app, 2, 2)

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
            print((row, col))
            if (row, col) in app.field:
                print(True)
                label = determineNumber(app, row, col)
                

def drawBoardBorder(app):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
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
    return app.mineLocations

def createField(app):
    for locationX, locationY in app.mineLocations:
        app.field[(locationX, locationY)] = Mine(locationX, locationY)
       # print(app.field[(locationX, locationY)])
    for row in range(app.rows):
        for col in range(app.cols):
            if not (row, col) in app.mineLocations:
                app.field[(row, col)] = Safe(row, col)
    print(app.field)

def drawField(app):
    for row in range(app.rows):
        for col in range(app.cols):
            label = determineNumber(app, row, col)
            print
            drawLabel(f"{label}", 50, 50)
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellWidth, cellHeight = getCellSize(app)
            drawLabel(f"{label}", cellLeft + (cellWidth / 2), cellTop + (cellHeight / 2), align = "center")
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

    def __repr__(self):
        return (f"Mine - {self.locX, self.locY}")

    def __eq__(self, other):
        if not (isinstance(other, Safe) or isinstance(other, Mine)):
            return False
        return (self.locX == other.locX) and (self.locY == other.locY)

    def __hash__(self):
        return hash(str(self))

# ---------------------------------------------------------------------------------------------
# SAFE CLASS
# ---------------------------------------------------------------------------------------------
class Safe:
    def __init__(self, locX, locY):
        self.locX = locX
        self.locY = locY

    def __repr__(self):
        return (f"Safe - {self.locX, self.locY}")

    def __eq__(self, other):
        if not (isinstance(other, Safe) or isinstance(other, Mine)):
            return False
        return (self.locX == other.locX) and (self.locY == other.locY)

    def __hash__(self):
        return hash(str(self))
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------

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
            if isinstance(app.field[(locationX, locationY)], Mine):
                count += 1
    return count

def main():
    runApp()
    print(app.mineLocations)
    

main()

print(determineNumber(app, 2, 2))