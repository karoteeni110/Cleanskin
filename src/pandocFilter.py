"""
A pandoc filter that aims to:
    Ignore comments (automatically), math mode, cites,
    images, lists (itemize), tables; 
    Turn emphasized text into ALL CAPS.
"""

from pandocfilters import Math, toJSONFilters, Cite, Para, \
  Emph, Str, walk, Table, Image, OrderedList, BulletList, DefinitionList

def no_math(k, v, fmt, meta):
  if k == 'Math':
    return []

def no_emph(k, v, fmt, meta):
  def strs(key, value, format, meta):
    if key == 'Str':
      return Str(value)
  if k == 'Emph':
    return walk(v, strs, fmt, meta)

def no_table(k, v, fmt, meta):
  if k == 'Table':
    return []

def no_image(k, v, fmt, meta):
  if k == 'Image':
    return []

def no_cite(k, v, fmt, meta):
  if k == 'Cite' or fmt == 'Latex':
    return []

def delist(k, v, fmt, meta):  
  if k == 'OrderedList':
    return v[1]
  elif k == 'BulletList': # This is ugly but working
    paragraphs = v[0]
    for i in v[1:]:
      paragraphs += i
    return paragraphs

actions = [no_math, no_cite, no_emph, no_table, no_image, delist]

if __name__ == "__main__":
  toJSONFilters(actions)