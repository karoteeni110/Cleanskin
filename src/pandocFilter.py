"""
Pandoc filter that makes convertion ignore comments,
math mode, images and tables.

Note: The return of an action is either:

    None: this means that the object should remain unchanged
    a pandoc object: this will replace the original object
    a list of pandoc objects: these will replace the original object; the list is merged with the neighbors of the original objects (spliced into the list the original object belongs to); returning an empty list deletes the object

"""

from pandocfilters import toJSONFilter, Math, Para, Emph
import re

def no_math(k, v, fmt, meta):
  if k =='Math':
    return Math()

if __name__ == "__main__":
  toJSONFilter(no_math)