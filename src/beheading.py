"""
Pandoc filter to convert LaTeX code to XML format.
"""

from pandocfilters import toJSONFilter, Emph, Para

def behead(key, value, format, meta):
    if key == 