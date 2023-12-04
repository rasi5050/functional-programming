Demo code for CIS 623 Fall 2020.
Modify from the following source:
_________________________________________________________


A Simple Sudoku Solver
27th September, 2007
In Chapter 05


The Sudoku game: an introduction

The game of Sudoku is played on a 9 by 9 grid, though 
other sizes are also possible. Given a matrix, such as 
that in Bird Figure 5.1 (refer as *example51* in 
section 0 below):

the idea is to fill in the empty cells (represented by 
the 0's) with the digits 1 to 9 so that for each 
row, column and 3 × 3 box contains the numbers 1 to 9.

In general there may be any number of solutions, though 
in a good Sudoku puzzle there should always be a unique 
solution.

_________________________________________________________
0. Basic data types

> type Matrix a = [Row a]
> type Row a    = [a]

> type Grid     = Matrix Digit
> type Digit    = Char

> digits  :: [Digit]
> digits  =  ['1'..'9']

> blank   :: Digit -> Bool
> blank   =  (== '0')


The Sudoku puzzle given in Figure 5.1 (Bird): 

> example51 :: Grid
> example51 = 
>     ["004005700",
>      "000009400",
>      "360000008",
>      "720060000",
>      "000402000",
>      "000080093",
>      "400000056",
>      "005300000",
>      "006100900"]


> example51a :: Grid
> example51a = 
>     ["000005700",
>      "000009400",
>      "300000008",
>      "720060000",
>      "000400000",
>      "000080093",
>      "400000006",
>      "000300000",
>      "006100000"]

> exampleHard :: Grid
> exampleHard =
>     ["083090750", 
>      "500000002",
>      "000700006",
>      "300100870",
>      "000000600",
>      "001020000",
>      "000000005",
>      "800200130",
>      "090004000"]


_________________________________________________________
1. Specification

a. Specification for a functional program

Define a function solve to compute a list of all the ways 
a given grid may be completed. When only one solution is 
wanted, then we can take the head of the list. Lazy 
evaluation means that only the first result will then be 
computed.

Regarding the specification, please note the following
remarks:

1. Write down the simplest and clearest specification 
without regard to how efficient the result might be. 

2. Always begin with a clear and simple, though possibly 
extremely inefficient definition of solve

3. Use the laws of functional programming to massage the
computation into one that takes acceptable time and 
space. This form of program construction, base on
the laws of functional programming, is a key difference 
between functional programming paradigm and other 
programming paradigms. 


b. Specification for the Sudoku puzzle


Given a partially filled Sudoku grid:

1. Complete it by filling in every possible choice for 
the blank entries and the result will be a list of 
filled grids, say L.

2. Filter the list L to eliminate those choices that 
contain duplicates in any row, box or column.

This two step specification can be stated as the 
function *solve1*:

> solve0 :: Grid -> [Grid]
> solve0 = filter valid . completions

The step 1 is implemented using the function 
completions:

> completions :: Grid -> [Grid]
> completions = expand . choices

and step 2 is implemented using the function
valid of type: valid :: Grid -> Bool. We will
first focus on step 1.

We subdivide step 1 into two sub steps:

1.1 (step 1.1) function choices

Given a Grid, it will apply the function 
*choice* to each entry of the Grid (a matrix) to 
display all the possible choices. That is, for
a digit d:

choice d ="123456789"    if d is blank
choice d =[d]            otherwise

1.2 (step 1.2) function expand

Given a matrix of choices (type Matrix Choices)
the expand function will create a list of of all
possible grids where each entry from each of these 
grids is obtained from making a definite choice 
of digits when choices are available.

The function expand relies on the function cartesian 
product *cp*. Note that this function is similar
but not identical to the mathematical definition of 
cartesian product of sets.




> type Choices = [Digit]

> choices :: Grid -> Matrix Choices
> choices = map (map choice)
>  where choice d | blank d   = digits
>                 | otherwise = [d]

> expand :: Matrix Choices -> [Grid]
> expand = cp . map cp

> cp :: [[a]] -> [[a]]
> cp []       = [[]]
> cp (xs:xss) = [x:ys | x <- xs, ys <- cp xss]


The step 2 of our specification is to eliminate 
those choices that contain duplicates in any row, 
box or column. It can be stated as the conjunction
of the three Boolean conditions as below:

> valid  :: Grid -> Bool
> valid g = all nodups (rows g) &&
>           all nodups (cols g) &&
>           all nodups (boxs g)

> nodups       :: Eq a => [a] -> Bool
> nodups []     = True
> nodups (x:xs) = x `notElem` xs && nodups xs

> rows :: Matrix a -> [Row a]
> rows = id

> cols          :: Matrix a -> [Row a]
> cols [xs]     = [[x] | x <- xs]
> cols (xs:xss) = zipWith (:) xs (cols xss)

> boxs :: Matrix a -> [Row a]
> boxs = map ungroup . ungroup . map cols .
>        group . map group

> ungroup          = concat
> group []         = []
> group (x:y:z:xs) = [x,y,z]:group xs

_________________________________________________________
2. Pruning

> prune :: Matrix Choices -> Matrix Choices
> prune =
>  pruneBy boxs . pruneBy cols . pruneBy rows
>  where pruneBy f = f . map pruneRow . f

> pruneRow :: Row Choices -> Row Choices
> pruneRow row = map (remove ones) row
>  where ones = [d | [d] <- row]

> remove :: Choices -> Choices -> Choices
> remove xs [d] = [d]
> remove xs ds  = filter (`notElem` xs) ds

_________________________________________________________
3. Intermediate solutions

> many :: (Eq a) => (a -> a) -> a -> a
> many f x = if x == y then x else many f y
>     where y = f x 


> solve1 = filter valid . expand . many prune . choices 

_________________________________________________________
4. Single-cell expansion

> expand1   :: Matrix Choices -> [Matrix Choices]
> expand1 rows =
>  [rows1 ++ [row1 ++ [c]:row2] ++ rows2 | c <- cs]
>  where
>  (rows1,row:rows2) = break (any smallest) rows
>  (row1,cs:row2)    = break smallest row
>  smallest cs       = length cs == n
>  n                 = minimum (counts rows)

> counts = filter (/=1) . map length . concat

_________________________________________________________
5. Final algorithm

> solve2 :: Grid -> [Grid]
> solve2 =  search . choices

> search :: Matrix Choices -> [Grid]
> search cm
>  |not (safe pm)  = []
>  |complete pm    = [map (map head) pm]
>  |otherwise      = (concat . map search . expand1) pm
>  where pm = prune cm

> complete :: Matrix Choices -> Bool
> complete = all (all single)

> single [_] = True
> single _   = False

> safe :: Matrix Choices -> Bool
> safe cm = all ok (rows cm) &&
>           all ok (cols cm) &&
>           all ok (boxs cm)

> ok row = nodups [d | [d] <- row]

_________________________________________________________


testcases

> validSudoku1 = [
>       "534678912"
>     , "672195348"
>     , "198342567"
>     , "859761423"
>     , "426853791"
>     , "713924856"
>     , "961537284"
>     , "287419635"
>     , "345286179"
>     ]

replace0With5 on top left for validSudoku1

> oneOffValidSudoku1 = [
>       "034678912"
>     , "672195348"
>     , "198342567"
>     , "859761423"
>     , "426853791"
>     , "713924856"
>     , "961537284"
>     , "287419635"
>     , "345286179"
>     ]

> multipleOffValidSudoku1 = [ 
>      "000000912"
>    , "072195348"
>    , "198342567"
>    , "850761423"
>    , "426853791"
>    , "713924856"
>    , "961537284"
>    , "287419635"
>    , "345286179"
>    ]

> validSudoku2 = [
>     "123467895",
>     "689351427",
>     "475289361",
>     "591723648",
>     "238614759",
>     "764895213",
>     "942138576",
>     "317546982",
>     "856972134"]
> 
> have2Solutions = [ 
>       "000000000"
>     , "600000000"
>     , "198342567"
>     , "859761423"
>     , "426853791"
>     , "713924856"
>     , "961537284"
>     , "287419635"
>     , "345286179"
>     ]

> haveMultipleSolutions = [ 
>       "000000000"
>     , "600000000"
>     , "198342567"
>     , "000000023"
>     , "426800000"
>     , "713924856"
>     , "961000000"
>     , "287419635"
>     , "345286179"
>     ]
