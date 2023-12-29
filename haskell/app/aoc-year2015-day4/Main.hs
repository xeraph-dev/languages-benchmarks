module Main (main) where

import Control.Concurrent (forkIO, newEmptyMVar, putMVar, takeMVar)
import Control.Monad (when)
import Crypto.Hash (MD5 (MD5), hashFinalize, hashInitWith, hashUpdate)
import Data.ByteArray (Bytes)
import qualified Data.ByteArray as BA
import qualified Data.ByteString.Char8 as BS
import System.Environment (getArgs)
import System.Exit (exitSuccess)

chunkSize :: Int
chunkSize = 1000

main :: IO ()
main = do
  args <- getArgs
  exitSignal <- newEmptyMVar

  let secret = BS.pack $ head args
      zeros_count = read $ args !! 1 :: Int
      bytes_count = ceiling $ fromIntegral zeros_count / 2
      zeros = BA.snoc (BA.replicate (div zeros_count 2) 0 :: Bytes) 0xF
      hash = hashUpdate (hashInitWith MD5) secret

      chunks = [take chunkSize xs | xs <- iterate (drop chunkSize) [1 ..]]

      compute i = do
        let num = BS.pack $ show (i :: Int)
            digest = hashFinalize . hashUpdate hash $ num
            bytes = BA.take bytes_count $ BA.convert digest :: Bytes
         in ( when (bytes <= zeros) $ do
                print i
                putMVar exitSignal ()
            )

      predicate is = do
        forkIO $ mapM_ compute is

  _ <- forkIO $ mapM_ predicate chunks

  takeMVar exitSignal
  exitSuccess
