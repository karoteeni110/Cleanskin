"""
A pandoc filter that aims to:
    Ignore comments (automatically), math mode, cites,
    images, lists (itemize), tables; 
    Turn emphasized text into ALL CAPS.
"""

from pandocfilters import Math, toJSONFilters, Cite, Para, Span, \
  Emph, Str, walk, Table, Image, OrderedList, BulletList, DefinitionList

def no_math(k, v, fmt, meta):
  if k == 'Math':
    return []

def no_emph(k, v, fmt, meta):
  def strs(key, value, format, meta):
    if key == 'Str':
      return Str(value)
  if k == 'Emph' or 'Strong':
    return walk(v, strs, fmt, meta)

def no_table(k, v, fmt, meta):
  if k == 'Table':
    return []
  # elif k == 'Para':
  #   sp = v[0] 
  #   if v[0]['t'] == 'Span' and v[0]['c'][1][0]['t'] == 'Str' and 'l' in v[0]['c'][1][0]['c'].

def no_image(k, v, fmt, meta):
  if k == 'Image':
    return []

def no_cite(k, v, fmt, meta):
  if k == 'Cite' or fmt == 'Latex':
    return []

def delist(k, v, fmt, meta):  
  '''Illustrative:
  >>> v == [[elt('Para', 1)], [elt('Para', 1)], ... ] 
  True
  '''
  paras = []
  if k == 'OrderedList':
    _, lstOflsts = v
    for i in lstOflsts:
      paras += i
    return paras
  elif k == 'BulletList':
    lstOflsts = v
    for i in lstOflsts:
      paras += i
    return paras


actions = [no_math, no_cite, no_emph, no_table, no_image, delist]

if __name__ == "__main__":
  toJSONFilters(actions)


# NOTE:
# {
# "t":"BulletList",
# "c":[
#   [{"t":"Para","c":[{"t":"Str","c":"guidelines"},{"t":"Space"},{"t":"Str","c":"for"},{"t":"Space"}],
#   [{"t":"Para","c":[{"t":"Str","c":"model"}],{"t":"Space"},{"t":"Str","c":"and"},{"t":"Space"}]
# ]
# }