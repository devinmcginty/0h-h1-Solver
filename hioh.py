from math import sqrt
from sys import argv
# Rules:
#   1. No more than 2 of a color in a row / column
#   2. Equal number of color A and B in a row / column
#   3. No two duplicate rows / columns

COLORS = {
    # There's probably a better way to do this, but this works for now.
    'R': -1,    # Red
    '-': 0,     # Blank
    'B': 1,     # Blue
    -1: 'R',
    0: '-',
    1: 'B'
}

class Grid(object):
    def __init__(self, clist):
        # clist is the grid as a string of "R", "B", or "-"
        super(Grid, self).__init__()
        self.size = int(sqrt(len(clist)))
        self.clist = clist
        self.grid = []
        self.genGrid(clist)
    def __repr__(self):
        rstring = ""
        for row in self.grid:
            rstring += ' '.join([COLORS[i] for i in row]) + "\n"
        return rstring
    def genGrid(self, clist):
        # Initialize numeric grid
        row = []
        for c in clist:
            row.append(COLORS[c])
            if len(row) == self.size:
                self.grid.append(row)
                row = []
    def isSolved(self):
        # Check if grid is solved
        for row in self.grid:
            if not isRowSolved(row):
                return False
        return True
    def solve(self):
        # Run solving algorithms
        while not self.isSolved():
            for i in range(2):
                self.parseRows()
                self.checkDupRows()
                self.transposeGrid()
    def parseRows(self):
        # Check for rules 1 and 2
        gridCopy = []
        for row in self.grid:
            if isRowSolved(row):
                gridCopy.append(row)
            else:
                gridCopy.append(parseRow(row))
        self.grid = gridCopy[:]
    def transposeGrid(self):
        # Perform a matrix transposition to check columns
        tGrid = []
        for x in range(self.size):
            tRow = []
            for row in self.grid:
                tRow.append(row.pop(0))
            tGrid.append(tRow)
        self.grid = tGrid[:]
    def checkDupRows(self):
        # chuck rule 3
        for i in range(self.size):
            if self.grid[i].count(COLORS['-']) != 2:
                continue
            for j in range(self.size):
                if i == j:
                    continue
                elif self.grid[j].count(COLORS['-']) == 0:
                    comparison = compareRows(self.grid[i], self.grid[j])
                    self.grid[i] = comparison if comparison else self.grid[i]

def compareRows(incomplete, complete):
    """Compare an incomplete row to a complete row to check for permutability.
    Return a complete permutation of 'complete' if 'incomplete' is a
    permutation of 'complete'. Return False otherwise."""
    retrow = []
    for i in range(len(incomplete)):
        if incomplete[i] == -1 * complete[i]:
            return False
        elif incomplete[i] == COLORS['-']:
            retrow.append(-1 * complete[i])
        else:
            retrow.append(incomplete[i])
    return retrow

def isRowSolved(row):
    """Check if row is solved"""
    return COLORS['-'] not in row

def transposeGrid(grid):
    """Transpose grid using matrix transposition."""
    tgrid = []
    size = len(grid)
    for x in range(size):
        row = []
        for y in range(size):
            row.append(grid[y][x])
        tgrid.append(row)
    return tgrid

def fillSolve(row, fillNum):
    """Fills all blank spaces in 'row' with 'fillNum'"""
    for i in range(len(row)):
        if row[i] == COLORS['-']:
            row[i] = fillNum
    return row

def parseRow(row):
    """Check first two rules:
        No more than 2 of same color in a row
        Equal number of both colors in row
    """
    empty = COLORS['-']
    rcopy = row[:]
    # Rule 2, check if all of one color is filled
    if rcopy.count(COLORS['R']) == len(row) // 2:
        return fillSolve(rcopy, COLORS['B'])
    elif rcopy.count(COLORS['B']) == len(row) // 2:
        return fillSolve(rcopy, COLORS['R'])
    # Rule 1, prevent 3 of one color in a row
    for i in range(1, len(row) - 1):
        if row[i - 1] == empty and row[i] == row[i + 1] != empty:
            # - C C
            rcopy[i - 1] = -1 * row[i]
        elif row[i + 1] == empty and row[i - 1] == row[i] != empty:
            # C C -
            rcopy[i + 1] = -1 * row[i]
        elif row[i] == empty and row[i - 1] == row[i + 1] != empty:
            # C - C
            rcopy[i] = -1 * row[i - 1]
    # Return if nothing changed in row
    if rcopy == row or row.count(empty) == 0:
        return rcopy
    # Recurse self until no more optimizations can be done
    return parseRow(rcopy)

def testCase():
    clist = "-R-R-R-R--"
    clist += "--B-R--RR-"
    clist += "-R---R--B-"
    clist += "R---B---B-"
    clist += "-B----B--R"
    clist += "--R-------"
    clist += "BR----R-BB"
    clist += "--B-----B-"
    clist += "R--R--B-R-"
    clist += "-B---B---B"

    test = Grid(clist)
    print(test)
    test.solve()
    print(test)

def main():
    if len(argv) > 1:
        inGrid = Grid(argv[1])
        print(inGrid)
        inGrid.solve()
        print(inGrid)
    else:
        testCase()


if __name__ == '__main__':
    main()
