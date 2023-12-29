module Main (main) where

import Crypto.Hash (Context, MD5 (MD5), hashFinalize, hashInitWith, hashUpdate)
import qualified Data.ByteArray as BA
import qualified Data.ByteString.Char8 as BL
import Data.List (find)
import System.Environment (getArgs)

compute :: Context MD5 -> Int -> BA.Bytes -> Int -> Bool
compute hash bytes_count zeros i =
  let num = BL.pack $ show (i :: Int)
      digest = hashFinalize . hashUpdate hash $ num
      bytes = BA.take bytes_count $ BA.convert digest :: BA.Bytes
   in bytes <= zeros

main :: IO ()
main = do
  args <- getArgs

  let secret = BL.pack $ head args
      zeros_count = read $ args !! 1 :: Int
      bytes_count = ceiling $ fromIntegral zeros_count / 2
      zeros = BA.snoc (BA.replicate (div zeros_count 2) 0 :: BA.Bytes) 0xF
      hash = hashUpdate (hashInitWith MD5) secret

  case find (compute hash bytes_count zeros) [1 ..] of
    Just x -> print x
    Nothing -> putStrLn "wtf"