"""
A pandoc filter that aims to:
    Turn the abstracts in metadata into paragraphs;  
    Ignore comments, math mode, images and tables.

Note: The return of an action is either:
    None: this means that the object should remain unchanged
    a pandoc object: this will replace the original object
    a list of pandoc objects: these will replace the original object; the list is merged with the neighbors of the original objects (spliced into the list the original object belongs to); returning an empty list deletes the object

"""

from pandocfilters import toJSONFilters, Math, Image, Emph, Cite, Table
import re

def meta2para(k, v, fmt, meta): # Exctract the abstract from metadata
  return None

def no_math(k, v, fmt, meta):
  if k=='Math':
    return []

# def no_comment(k, v, fmt, meta):
#   return None

def no_table(k, v, fmt, meta):
  if k=='Table':
    return []

def no_image(k, v, fmt, meta):
  if k=='Image':
    return None

def no_cite(k, v, fmt, meta):
  if k=='Cite' and fmt=='Latex':
    return []

actions = [no_math, no_table, no_image, no_cite]

if __name__ == "__main__":
  toJSONFilters(actions)