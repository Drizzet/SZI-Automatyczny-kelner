D_COST = 99999999999999999  # diagonal
V_COST = 0  # vertical
COLS = 25
ROWS = 25


class Cell():
    def __init__(self, inx, iny):
        self.hCost = 0
        self.fCost = 0
        self.x = inx
        self.y = iny
        self.parent = self


grid = [[Cell for x in range(COLS)] for y in range(ROWS)]
open = []
closed = [[False for x in range(COLS)] for y in range(ROWS)]
startx = 0
starty = 0
endx = 0
endy = 0


def setBlocked(x, y):
    grid[x][y] = None


def setStart(x, y):
    global startx
    startx = x
    global starty
    starty = y


def setEnd(x, y):
    global endx
    endx = x
    global endy
    endy = y


def updateCost(current, next, cost):
    if (next == None):
        return;
    if (closed[next.x][next.y]):
        return;
    next_f_cost = next.hCost + cost
    inopen = (next in open)
    if (not inopen) or (next_f_cost < next.fCost):
        next.fCost = next_f_cost
        next.parent = current
        if (not inopen):
            open.append(next)


def aStar():
    open.append(grid[startx][starty])
    grid[startx][starty].parent = None
    while (True):
        if not open:
            return
        current = open.pop(0)
        if (current == None):
            break;
        closed[current.x][current.y] = True

        next = None
        # warunek koncowy
        if (current == grid[endx][endy]):
            print("return")
            return;

        # poruszanie sie
        if (current.x - 1 >= 0):
            next = grid[current.x - 1][current.y]
            updateCost(current, next, current.fCost + V_COST)

           # if (current.y - 1 >= 0):
              #  next = grid[current.x - 1][current.y - 1]
              #  updateCost(current, next, current.fCost + D_COST)

           # if (current.y + 1 < len(grid[0])):
              #  next = grid[current.x - 1][current.y + 1]
              #  updateCost(current, next, current.fCost + D_COST)

        if (current.y - 1 >= 0):
            next = grid[current.x][current.y - 1]
            updateCost(current, next, current.fCost + V_COST)

        if (current.y + 1 < len(grid[0])):
            next = grid[current.x][current.y + 1]
            updateCost(current, next, current.fCost + V_COST)

        if (current.x + 1 < len(grid)):
            next = grid[current.x + 1][current.y]
            updateCost(current, next, current.fCost + V_COST)

          #  if (current.y - 1 >= 0):
            #    next = grid[current.x + 1][current.y - 1]
            #    updateCost(current, next, current.fCost + D_COST)

          #  if (current.y + 1 < len(grid[0])):
            #    next = grid[current.x + 1][current.y + 1]
            #    updateCost(current, next, current.fCost + D_COST)


def Test(x, y, sx, sy, ex, ey, blocked):
    global grid
    grid = [[Cell for i in range(x)] for j in range(y)]
    setStart(sx, sy)
    setEnd(ex, ey)
    for i in range(0, x):
        for j in range(0, y):
            grid[i][j] = Cell(i, j)
            grid[i][j].hCost = abs(i - ex) + abs(j - ey)

    grid[sx][sy].fCost = 0
    for i in range(0, len(blocked)):
        setBlocked(blocked[i][0], blocked[i][1])

    aStar()
    if (closed[endx][endy]):
        print("Path:")
        current = grid[endx][endy]
        print(current.x, current.y)
        while (current.parent != None):
            print("->", current.parent.x, current.parent.y)
            current = current.parent
    else:
        print("No path found")


print("START")
# Test(wielkosc mapy x, wielkosc mapy y, start x, start y, cel x, cel y, lista wspl przeszkod)
Test(5, 5, 0, 0, 3, 2, [[0, 4], [2, 2], [3, 1], [3, 3]])
#Test(5, 5, 0, 0, 4, 3, [[0, 4], [2, 2], [3, 1], [3, 3]])
#Test(7, 7, 2, 1, 5, 4, [[4, 1], [4, 3], [5, 3], [2, 3]])
#Test(5, 5, 0, 0, 4, 4, [[3, 4], [3, 3], [4, 3]])

print("KONIEC")
