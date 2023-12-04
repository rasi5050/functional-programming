# functional-programming
Functional programming tasks associated with being a Teaching Assistant for "Structured Programming and Formal Methods" during my Masters in Computer Science.

# 1. A* Algorithm
   
## **aStarUsingFunctionalProgramming.py**
  
  How to run?
  
  Python3 -i aStarUsingFunctionalProgramming.py
  
  test cases will automatically run

# 2. Sudoku Solver

## **Sudoku.lhs** (Original Haskell code to be ported to python)
  
  How to run?
  
  ghci Sudoku.lhs
  
  and invoke function/s with required inputs
  
  eg) the input oneOffValidSudoku1 is already added and can be invoked as 
  
  > solve0(oneOffValidSudoku1)
  
  > solve1(oneOffValidSudoku1)
  
  > solve2(oneOffValidSudoku1)
  
## **Sudoku.py** (Ported Python code from above Haskell code)
  
  How to run?
  
  python3 -i Sudoku.py
  
  and invoke function/s with required inputs
  
  eg) the input oneOffValidSudoku1 is already added and can be invoked as 
  
  > solve0(oneOffValidSudoku1)
  
  > solve1(oneOffValidSudoku1)
  
  > solve2(oneOffValidSudoku1)



### Other test cases included, in both Haskell and Python codes (meaning to be understood same as the names)

validSudoku1

oneOffValidSudoku1

multipleOffValidSudoku1

validSudoku2

haveMultipleSolutions


