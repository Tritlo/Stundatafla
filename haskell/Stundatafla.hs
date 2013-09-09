{-# LANGUAGE DeriveDataTypeable #-}
import System.Console.CmdArgs
import Network.Curl
import Text.HTML.TagSoup
import qualified Data.Map as M

{-- Matthías Páll Gissurarson (C) 2013 --}



data Args = Edit { infile  :: String
                 , courses :: String}
          | New  { courses :: String}
            deriving (Show, Data, Typeable)


edit = Edit{ infile = def &= help "Table to work from"
           , courses = def &= args &= typ "COURSES"}
new = New{ courses = def &= args &= typ "COURSES"}

vonLink = "https://von.hi.is/von/stundat/haust/namskeid_toflur_haust.htm"

getTags url = do
  (resp, body) <- curlGetString vonLink []
  return (parseTags body)



between :: (a -> Bool) -> (a -> Bool) -> [a] -> [[a]]
between a b xs = betweenH a b ([],xs)

betweenH :: (a -> Bool) -> (a -> Bool) -> ([[a]],[a]) -> [[a]]
betweenH a b (ys,[]) = ys
betweenH a b (ys,xs)
  | (a $ head xs) = betweenH a b (ys ++ [t ++ [head d]],d)
  | otherwise = betweenH a b (ys, tail xs)
  where (t,d) = span (\x -> not (b x)) xs


      


getAs = between (isTagOpenName "a") (isTagCloseName "a")
aTagToLink tag = fromAttrib "href" (head tag)
aTagToName tag = fromTagText $ head $filter isTagText tag
aTagToNameLink tag = (aTagToName tag, aTagToLink tag)

linkToDict vonLink = do
    tags <- getTags vonLink
    return (M.fromList $ map aTagToNameLink $ getAs tags)


main = do
  --print $ between (== 2) (== 3) [0,1,2,3,4,5]
  dict <- linkToDict vonLink
  print $ M.lookup "TÖL101G" dict
  --print $ aTagToNameLink $ head $ getAs tags



  
