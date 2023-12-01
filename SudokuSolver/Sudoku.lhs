Original Haskell code to be ported to python(attached)

How to run?
ghci Sudoku.lhs
and invoke function with required inputs


A Simple Sudoku Solver
27th September, 2007
In Chapter 05
_________________________________________________________
0. Basic data types

> type Matrix a = [Row a]
> type Row a    = [a]

> type Grid     = Matrix Digit
> type Digit    = Char

> digits  :: [Digit]
> digits  =  ['1'..'9']

> blank   :: Digit -> Bool
> blank  =  (== '0')

1. Specification

original
solve1 :: Grid -> [Grid]
solve1 = filter valid . expand . choices


> solve1 :: Grid -> [Grid]
> solve1 = filter valid . expand . choices

> solve1WithPruning :: Grid -> [Grid]
> solve1WithPruning = filter valid . expand . prune . choices


[Digit] is replaced as str in python

> type Choices = [Digit]

> choices :: Grid -> Matrix Choices
> choices = map (map choice)
>  where choice d | blank d   = digits
>                 | otherwise = [d]

> checkChoices :: Grid
> checkChoices = [ "12"
>            , "02" ]

> exampleGrid1 :: Grid
> exampleGrid1 = 
>     ["50",
>      "01"]

> expand :: Matrix Choices -> [Grid]
> expand = cp . map cp

> cp :: [[a]] -> [[a]]
> cp []       = [[]]
> cp (xs:xss) = [x:ys | x <- xs, ys <- cp xss]

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

3. Single-cell expansion

> expand1   :: Matrix Choices -> [Matrix Choices]
> expand1 rows =
>  [rows1 ++ [row1 ++ [c]:row2] ++ rows2 | c <- cs]
>  where
>  (rows1,row:rows2) = break (any smallest) rows
>  (row1,cs:row2)    = break smallest row
>  smallest cs       = length cs == n
>  n                 = minimum (counts rows)

> counts = filter (/=1) . map length . concat

4. Final algorithm

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



inputs

> validSudoku1 :: Grid
> validSudoku1 =
>     [ "534678912"
>     , "672195348"
>     , "198342567"
>     , "859761423"
>     , "426853791"
>     , "713924856"
>     , "961537284"
>     , "287419635"
>     , "345286179"
>     ]


 replace0With5

> oneOffValidSudoku1 :: Grid
> oneOffValidSudoku1 =
>     [ "034678912"
>     , "672195348"
>     , "198342567"
>     , "859761423"
>     , "426853791"
>     , "713924856"
>     , "961537284"
>     , "287419635"
>     , "345286179"
>     ]

> multipleOffValidSudoku1 :: Grid
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


> validSudoku2 :: Grid
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
