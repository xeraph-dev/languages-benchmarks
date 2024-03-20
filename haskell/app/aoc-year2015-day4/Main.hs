module Main (main) where

import Control.Concurrent (MVar, forkIO, getNumCapabilities, isEmptyMVar, killThread, modifyMVar_, newEmptyMVar, newMVar, putMVar, swapMVar, takeMVar, tryReadMVar)
import Control.Monad (void, when)
import Crypto.Hash (MD5 (MD5), hashFinalize, hashInitWith, hashUpdate)
import Data.ByteArray (Bytes)
import qualified Data.ByteArray as BA
import qualified Data.ByteString.Char8 as BS
import Data.Map (Map, (!))
import qualified Data.Map as M
import GHC.Conc (ThreadId)
import System.Environment (getArgs)

main :: IO ()
main = do
  args <- getArgs
  candidate <- newEmptyMVar :: IO (MVar Int)
  cpuCount <- getNumCapabilities
  threads <- newMVar M.empty :: IO (MVar (Map Int ThreadId))

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

      compute steps i = do
        founded <- mVarIsLowerThan candidate i
        when founded $ do
          threadsVar <- takeMVar threads
          killThread $ threadsVar ! steps
        let num = BS.pack $ show (i :: Int)
            digest = hashFinalize . hashUpdate hash $ num
            bytes = BA.take bytes_count $ BA.convert digest :: Bytes
            valid = bytes <= zeros
         in when valid $ updateMVar candidate i

      predicate steps = do
        modifyMVar_ threads $ \ts -> do
          let chunks = enumFromThenTo steps (steps + cpuCount) maxBound
          threadId <- forkIO $ mapM_ (compute steps) chunks
          return $ M.insert steps threadId ts

  mapM_ predicate [0 .. cpuCount - 1]

  takeMVar candidate >>= print
