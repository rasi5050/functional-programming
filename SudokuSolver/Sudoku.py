#Ported code from Haskell(attached) to Python
"""
A simple Sudoku Solver; 
ported from haskell(Bird, chap 05) to python
11/23-27/2023
Rasi
"""

"""
there are three algorithms here,
solve1: #Main idea: brute force all potential matrix choices, filter out valid matrix from those (naive)
solve1WithPruning: #Main idea: prune matrices to discard invalid choices and filter valid matrices (intermediate)
solve2: #Main idea: prune matrices, single cell expansion to discard invalid choices (advanced)

to run algorithm,
sample input format is as below
validSudoku1 = [
      "534678912"
    , "672195348"
    , "198342567"
    , "859761423"
    , "426853791"
    , "713924856"
    , "961537284"
    , "287419635"
    , "345286179"
    ]
algorithm should be executed as solve1(validSudoku1), solve1WithPruning(validSudoku1), solve1(validSudoku1)

Few testcases will be automatically run executing the program

Syntax for defining type in Python(reffered as "type hinting" in python)
https://docs.python.org/3/library/typing.html

example: 
Matrix = List[Row] 
should be read as
Matrix is a List of Row's


The below code is developed and tested on python3.11
-if you dont have, install python3.11 by executing 
on Ubuntu
`sudo apt update
sudo apt install python3.11`

OR
on Mac
`
brew install python@3.11
`

> How to run code?
python3 -i Sudoku.py
"""
from typing import TypeVar, List

# 0. Basic data types

#defining arbitrary type T
T = TypeVar('T')

#Row is list of type T
Row = List[T]
#Matrix is list of Row's
Matrix = List[Row]

#Digit is a charecter; ie. string of length 1 in python
Digit = str
#Grid is a Matrix of Digit's
Grid = Matrix[Digit]

#return list of possible digits 1 to 9
def digits() -> str:
    return ''.join([str(i) for i in range(1,10)])

#return true if a digit is zero
def blank(d: Digit) -> bool:
    return d == '0'

# 1. Specification

# Choices = List[Digit]
#Choices is changed as string, as list of char is string
Choices = str

#choices of each position in the grid
#if digit==0, replace with "123456789", representing that possible values at that positions, 
# else current digit
def choices(grid: Grid) -> Matrix[Choices]:
    def choice(d: Digit) -> Choices:
        return digits() if blank(d) else d
    return [list(map(choice, row)) for row in grid]


#cartesian product
"""
needed to expand choices to each possible matrices
[["123456789", "1"],["2","3"]] on cartesian product will expand to 9 matrices
ie. [["1", "1"],["2","3"]], [["2", "1"],["2","3"]], ..., [["9", "1"],["2","3"]],  
"""
def cp(lst: List[List[T]]) -> List[List[T]]:
    if not lst:
        return [[]]
    else:
        return [[x] + ys for x in lst[0] for ys in cp(lst[1:])]

#expand to cartesian products all possible matrixes; output format is different, instead of rows as string, its array of characters
def expand(mat: Matrix[Choices]) -> List[Grid]:
    # Apply cp to the matrix of all possible rows
    return cp([cp(row) for row in mat])

#check if no duplicates in a list 'lst', return True if no duplicates, else False
def nodups(lst: List[T])->bool:
    if not lst: return True
    return lst[0] not in lst[1:] and nodups(lst[1:])

#return rows of matrix as list
def rows(mat: Matrix) -> List[Row]:
    return mat

#return columns of matrix as list, found by transposing matrix and taking rows
def cols(mat: Matrix) -> List[Row]:
    return list(map(list, zip(*mat)))

"""not currently used
#alternate implementation of "group"
# def group(lst: List[T]) -> List[List[T]]:
    return [lst[i:i + 3] for i in range(0, len(lst), 3)]

def ungroup(groups: List[List[T]]) -> List[T]:
    return [item for group in groups for item in group]

#alternate implementation of "ungroup"
# def ungroup(lst: List[List[T]]) -> List[T]:
#     return [item for sublist in lst for item in sublist]
"""

#return the 3x3 grids, returned as a flattened list so that nodups can check duplicates
def boxs(mat: Matrix) -> List[Row]:
        #group into 3, used to identfy 3x3 grid
    def group(lst):
        if not lst: return []
        return [[lst[0], lst[1], lst[2]]] + group(lst[3:])
    # Group the matrix into 3x3 blocks and process each block
    grouped = [group(row) for row in mat]
    boxes = []
    for i in range(0, len(grouped), 3):
        for j in range(3):
            box = grouped[i][j] + grouped[i + 1][j] + grouped[i + 2][j]
            boxes.append(box)
    return boxes


#check valid, check if rows, columns or grids has duplicates., return true if all of them doesnt have duplicates
def valid(g: Grid) -> bool:
    return all(map(nodups, rows(g))) and all(map(nodups, cols(g))) and all(map(nodups, boxs(g)))


#check valid for possible matrix choices using filter
#ie. filter out only valid matrices from the list of all potential solution matrices
def solve1(grid: Grid)->List[Grid]:
    listMat = list(filter(valid, expand(choices(grid))))
    return [[''.join(row) for row in mat] for mat in listMat]




#sample testcases
count=1
def solutionViewer(sudoku, sudoku_name="", algo=solve1):
    global count
    if not sudoku_name: sudoku_name="sample"+str(count)
    print("----------------------------------------------------------")
    print("example", count)
    print(f"{sudoku_name} = ", sudoku)
    print("\nSolution is\n")
    print(algo(sudoku), "\n")
    print("----------------------------------------------------------")
    count+=1

#testcases
validSudoku1 = [
      "534678912"
    , "672195348"
    , "198342567"
    , "859761423"
    , "426853791"
    , "713924856"
    , "961537284"
    , "287419635"
    , "345286179"
    ]

# replace0With5 on top left for validSudoku1

oneOffValidSudoku1 = [
      "034678912"
    , "672195348"
    , "198342567"
    , "859761423"
    , "426853791"
    , "713924856"
    , "961537284"
    , "287419635"
    , "345286179"
    ]

multipleOffValidSudoku1 = [ 
     "000000912"
   , "072195348"
   , "198342567"
   , "850761423"
   , "426853791"
   , "713924856"
   , "961537284"
   , "287419635"
   , "345286179"
   ]

validSudoku2 = [
    "123467895",
    "689351427",
    "475289361",
    "591723648",
    "238614759",
    "764895213",
    "942138576",
    "317546982",
    "856972134"]

have2Solutions = [ 
      "000000000"
    , "600000000"
    , "198342567"
    , "859761423"
    , "426853791"
    , "713924856"
    , "961537284"
    , "287419635"
    , "345286179"
    ]

haveMultipleSolutions = [ 
      "000000000"
    , "600000000"
    , "198342567"
    , "000000023"
    , "426800000"
    , "713924856"
    , "961000000"
    , "287419635"
    , "345286179"
    ]

testCases = [(validSudoku1, "validSudoku1")
,(oneOffValidSudoku1, "oneOffValidSudoku1")
,(multipleOffValidSudoku1, "multipleOffValidSudoku1")
,(validSudoku2, "validSudoku2")]

print("Solve Using solve1")
print("Note: testCase: multipleOffValidSudoku1 will take long time to run as its naive algorithm")
for test_sudoku, test_name in testCases:
    solutionViewer(test_sudoku, test_name)    


# ---------------------------------------------------------
# solve2 starts from here

# 2. Pruning
#identify duplicate choices
def remove(c1: Choices, c2: Choices)->Choices:
    return ''.join([c for c in c2 if c not in c1])

#prune by row
def pruneRow(row: Row[Choices])->Row[Choices]:
    ones = [ choice for choice in row if len(choice)==1]
    return [remove(ones, choice) if len(choice)>1 else choice for choice in row]

#prune by matrix to discard invalid choices
def prune(mat: Matrix[Choices])->Matrix[Choices]:
    def pruneBy(f, mat1): return f(list(map(pruneRow, f(mat1))))
    prunedByRows = pruneBy(rows, mat)
    prunedByCols = pruneBy(cols, prunedByRows)
    prunedByBoxs = pruneBy(boxs, prunedByCols)
    return prunedByBoxs
#solve with pruning algorithm
def solve1WithPruning(grid: Grid)->List[Grid]:
    listMat = list(filter(valid, expand(prune(choices(grid)))))
    return [[''.join(row) for row in mat] for mat in listMat]

print("Solve Using solve1WithPruning")
for test_sudoku, test_name in testCases:
    solutionViewer(test_sudoku, test_name, solve1WithPruning)    
# ------------------------end of prune------------------------


# --------------------------------------------------------
# 3. Single-cell expansion

# concat entire matrix as a single list to identify smallest choice length
def concat(rows: Matrix[Choices])->Row[Choices]:
        if not rows: return []
        return rows[0] + concat(rows[1:])

#find length of choices in concat matrix
def counts(rows: Matrix[Choices])->List[int]:
    return [count for count in list(map(len, concat(rows))) if count!=1]

#differnt approach to expand the matrix, earlier all the matrix was exapnded, here the expansion starts from matrix with smallest choice length
def expand1(rows: Matrix[Choices])->List[Matrix[Choices]]:
    def n(rows): return min(counts(rows))

    #break the row with smallest choice length as (row[:c], row[c], row[c+1:])
    def breakRow(row, c=0):
        if c==len(row): return None
        if len(row[c]) == n(rows): return (row[:c], row[c], row[c+1:])
        return breakRow(row, c+1)
    
    #break the rows with smallest row with smallest choice length ato obtain (rows1, (row1, cs, row2), rows2)
    def breakRows(rows, c=0):
        if c==len(rows): return None
        if breakRow(rows[c]): return (rows[:c], breakRow(rows[c]), rows[c+1:])
        return breakRows(rows, c+1)
    
    (rows1, (row1, cs, row2), rows2) = breakRows(rows)

    return [rows1 + [row1 + [c] + row2] + rows2 for c in cs]


# 4. Final algorithm

#check duplicates
def ok(row: Row[Choices])->bool:
    return nodups([cs for cs in row if len(cs)==1])

#check duplicates on rows, cols and boxs
def safe(cm: Matrix[Choices])->bool:
    return all(map(ok, rows(cm)) and map(ok, cols(cm)) and map(ok, boxs(cm)))

#check if a cell has only single charecter
def single(cs: Choices)->bool:
    return True if len(cs)==1 else False

#check if the matrix has only single charecters in all cells
def complete(mat: Matrix[Choices])->bool:
    return all([single(cs) for row in mat for cs in row])

#concatinate the rows of matrix 
def concat1(mats: Matrix[Choices])->List[Grid]:
        if not mats: return [[]]
        return mats[0] + concat(mats[1:])

#search for valid matrix from the possibilities
def search(cm: Matrix[Choices])->List[Grid]:
    pm=prune
    if not safe(pm(cm)): return []
    #in haskell code; its to join cells in a row to a string
    if complete(pm(cm)): return pm(cm)
    #skipped concat here, for output consistency
    return [r for r in concat1(list(map(search, expand1(pm(cm))))) if r]

#solve2 final algorithm
def solve2(grid: Grid)->List[Grid]:
    out = list(search(choices(grid)))
    listMat = [out[i:i+9] for i in range(0,len(out),9)]  
    return [[''.join(row) for row in mat] for mat in listMat]

testCases += [(haveMultipleSolutions, "haveMultipleSolutions")]

print("Solve Using solve2")
for test_sudoku, test_name in testCases:
    solutionViewer(test_sudoku, test_name, solve2)    