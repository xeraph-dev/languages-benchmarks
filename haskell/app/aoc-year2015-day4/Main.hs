module Main (main) where

import Control.Concurrent (MVar, forkIO, getNumCapabilities, isEmptyMVar, newEmptyMVar, putMVar, swapMVar, takeMVar, tryReadMVar)
import Control.Monad (void, when)
import Crypto.Hash (MD5 (MD5), hashFinalize, hashInitWith, hashUpdate)
import Data.ByteArray (Bytes)
import qualified Data.ByteArray as BA
import qualified Data.ByteString.Char8 as BS
import System.Environment (getArgs)
import System.Exit (exitSuccess)

main :: IO ()
main = do
  args <- getArgs
  candidate <- newEmptyMVar :: IO (MVar Int)
  cpuCount <- getNumCapabilities

  let secret = BS.pack $ head args
      zeros_count = read $ args !! 1 :: Int
      bytes_count = ceiling $ fromIntegral zeros_count / 2
      zeros = BA.snoc (BA.replicate (div zeros_count 2) 0 :: Bytes) 0xF
      hash = hashUpdate (hashInitWith MD5) secret

      mVarIsLowerThan a b = do
        mvar <- tryReadMVar a
        return $ case mvar of
          Just var -> var < b
          Nothing -> False

      updateMVar mvar var = do
        empty <- isEmptyMVar mvar
        if empty
          then putMVar mvar var
          else void $ swapMVar mvar var

      compute i = do
        founded <- mVarIsLowerThan candidate i
        when founded exitSuccess
        let num = BS.pack $ show (i :: Int)
            digest = hashFinalize . hashUpdate hash $ num
            bytes = BA.take bytes_count $ BA.convert digest :: Bytes
            valid = bytes <= zeros
         in when valid $ updateMVar candidate i

      predicate steps = do
        forkIO . mapM_ compute $ enumFromThenTo steps (steps + cpuCount) maxBound

  mapM_ predicate [0 .. cpuCount - 1]

  takeMVar candidate >>= print
