from math import sqrt
COLORS = {
    "R": -1,
    "-": 0,
    "B": 1,
    -1: "R",
    0: "-",
    1: "B"
}

class Grid(object):
    def __init__(self, clist):
        super(Grid, self).__init__()
        self.size = int(sqrt(len(clist)))
        self.clist = clist
        self.grid = []
        self.genGrid(clist)
    def genGrid(self, clist):
        row = []
        for c in clist:
            row.append(COLORS[c])
            if len(row) == self.size:
                self.grid.append(row)
                row = []
    def isSolved(self):
        for row in self.grid:
            if not isRowSolved(row):
                return False
        return True
    def solve(self):
        while not self.isSolved():
            tempGrid = self.grid[:]
            gridCopy = []
            for row in self.grid:
                gridCopy.append(parseRow(row))
            self.grid = gridCopy[:]
            tGrid = []
            for row in transposeGrid(self.grid):
                tGrid.append(parseRow(row))
            self.grid = transposeGrid(tGrid)
            if tempGrid == self.grid:
                for i in range(2):
                    self.checkDupRows()
                    self.grid = transposeGrid(self.grid)
                break
    def checkDupRows(self):
        for i in range(self.size):
            row = self.grid[i]
            if sum(row) == 0 and not isRowSolved(row):
                for j in range(self.size):
                    if i == j:
                        continue

    def __repr__(self):
        rstring = ""
        for row in self.grid:
            rstring += " ".join([COLORS[i] for i in row]) + "\n"
        return rstring

def compareRows(r1, r2):
    # r1 is solved
    for i in len(r1):
        pass

def isRowSolved(row):
    return COLORS['-'] not in row

def transposeGrid(grid):
    tgrid = []
    size = len(grid)
    for x in range(size):
        row = []
        for y in range(size):
            row.append(grid[y][x])
        tgrid.append(row)
    return tgrid

def fillSolve(row, fillNum):
    for i in range(len(row)):
        if row[i] == COLORS['-']:
            row[i] = fillNum
    return row

def parseRow(row):
    rcopy = row[:]
    if rcopy.count(COLORS['-']) == 1:
        blankIndex = rcopy.index(COLORS['-'])
        rcopy[blankIndex] = -1 * sum(rcopy)
        return rcopy
    elif rcopy.count(COLORS['R']) == len(row) // 2:
        return fillSolve(rcopy, COLORS['B'])
    elif rcopy.count(COLORS['B']) == len(row) // 2:
        return fillSolve(rcopy, COLORS['R'])
    for i in range(1, len(row) - 1):
        if row[i - 1] == COLORS['-'] and row[i] == row[i + 1]:
            rcopy[i - 1] = -1 * row[i]
        elif row[i + 1] == COLORS['-'] and row[i - 1] == row[i]:
            rcopy[i + 1] = -1 * row[i]
        elif row[i] == COLORS['-'] and row[i - 1] == row[i + 1]:
            rcopy[i] = -1 * row[i - 1]
    if rcopy == row:
        return rcopy
    return parseRow(rcopy)

def isRowSolved(row):
    return sum(row) == 0 and COLORS['-'] not in row

def main():
    clist = "-RR---RBR-------"
    test = Grid(clist)
    test.solve()

if __name__ == '__main__':
    main()
