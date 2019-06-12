"""
A pandoc filter that aims to:
    Turn the abstracts in metadata into paragraphs;  
    Ignore comments, math mode, images and tables.

Note: The return of an action is either:
    None: this means that the object should remain unchanged
    a pandoc object: this will replace the original object
    a list of pandoc objects: these will replace the original object; the list is merged with the neighbors of the original objects (spliced into the list the original object belongs to); returning an empty list deletes the object

"""

from pandocfilters import Math, toJSONFilters, Cite, Emph, Str, walk, Table, Image, OrderedList, BulletList, DefinitionList

def no_math(k, v, fmt, meta):
  if k == 'Math':
    return []

def no_emph(k, v, fmt, meta):
  def caps(key, value, format, meta):
    if key == 'Str':
      return Str(value.upper())
  if k == 'Emph':
    return walk(v, caps, fmt, meta)

def no_table(k, v, fmt, meta):
  if k == 'Table':
    return []

def no_image(k, v, fmt, meta):
  if k == 'Image':
    return []

def no_cite(k, v, fmt, meta):
  if k == 'Cite' and fmt == 'Latex':
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