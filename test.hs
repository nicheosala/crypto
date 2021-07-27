countNegatives :: [[Int]] -> Int
countNegatives = length . filter (<0) . concat