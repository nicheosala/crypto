euclid :: Integral t => t -> t -> t
euclid a 0 = a
euclid a b = euclid b (mod a b)

coprime :: Integral a => a -> a -> Bool
coprime a b = euclid a b == 1

coprimes :: Integral a => a -> [a]
coprimes n = filter (coprime n) [1 .. n]

totient :: Integral a => a -> Int
totient = length . coprimes

factor :: Integral a => a -> a -> Bool
factor n x = mod n x == 0

factors :: Integral a => a -> [a]
factors n = filter (factor n) [1 .. n]

prime :: (Ord a, Integral a) => a -> Bool
prime n = n > 1 && not (any (factor n) [2 .. sqrtint n])

primes :: [Integer]
primes = filter prime [2 ..]

composite :: Integral a => a -> Bool
composite n = n > 1 && not (prime n)

composites :: [Integer]
composites = filter composite [2 ..]

charmichael :: Integer -> Bool
charmichael n = composite n && all (\a -> pow a (n - 1) n == 1) (coprimes n)

charmichaels :: [Integer]
charmichaels = filter charmichael [2 ..]

-- squareAndMultiply base exp n = foldl sqrMul exp 1 where
--   sqrMul x bit = multiply (square x) bit where
--     square x = pow x 2 n
--     multiply x bit = mod (if bit == 1 then base else 1) n


-- https://rosettacode.org/wiki/Modular_exponentiation#Haskell
pow :: Integer -> Integer -> Integer -> Integer
pow b e m = powm b e m 1
  where
    powm b 0 m r = r
    powm b e m r
      | e `mod` 2 == 1 = powm (b * b `mod` m) (e `div` 2) m (r * b `mod` m)
    powm b e m r = powm (b * b `mod` m) (e `div` 2) m r

sqrtint :: (Integral b, Integral a) => a -> b
sqrtint n = floor (sqrt (fromIntegral n))

-- Much better in Python...
eea :: Integral t => t -> t -> (t, t, t)
eea a b = eeahelper a b 1 0 0 1
  where
    eeahelper n m x1 y1 x2 y2
      | m == 0 = (n, x1, y1)
      | otherwise = eeahelper m (mod n m) x2 y2 (x1 - q * x2) (y1 - q * y2)
      where
        q = div n m
