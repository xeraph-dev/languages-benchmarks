module Main (main) where

import Crypto.Hash (Digest, MD5, hashlazy)
import qualified Data.ByteString.Lazy.Char8 as BL
import Data.List (find)
import System.Environment (getArgs)

main :: IO ()
main = do
  args <- getArgs

  let secret = BL.pack $ head args
  let zeros_count = read $ args !! 1 :: Int
  case find (\i -> take zeros_count (show (hashlazy (secret <> BL.pack (show (i :: Integer))) :: Digest MD5)) == replicate zeros_count '0') [1 ..] of
    Just x -> print x
    Nothing -> putStrLn "wtf"