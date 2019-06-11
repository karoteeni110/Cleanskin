"""
Pandoc filter that makes convertion ignore comments,
math mode, images, code, tables, bullet/ordered list.
"""

from pandocfilters import toJSONFilter, Math, Para, Emph
import re

def no_math(k, v, fmt, meta):
  if k=='Math':
    print(v)

if __name__ == "__main__":
  toJSONFilter(no_math)