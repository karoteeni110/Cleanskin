#!/usr/bin/env runhaskell

import Text.Pandoc.JSON

main = toJSONFilter demath
  where demath (Math x y) = Math x "MATHFORMULA"
        demath x = x