""" A parser for LaTex code. """

import re
__all__ = ['LTXparser']

# RegEx used for parsing

before_doc = r'(.*^\\begin{document}$)' # all the code before \begin{doccument}
comments = r'%.*?$'


class LTXparser():
    """ Find commands and other macros and call handler functions.

    Usage: Pretty like html.parser.
        p = LTXparser()
        p.feed(data)
        ...
        p.close()

    """
    def __init__(self, clean_precommath=True):
        """
        Initialize and reset the instance.

        If clean_precom is True (the default), all preambles, comments and 
        math mode (e.g. "$k_{\rm ET}$") are automatically deleted from the 
        instance.
        """
        self.clean_precommath = clean_precommath
        self.reset()
    
    def reset(self):
        """Reset the instance such that it loses all unprocessed data."""
        self.rawdata = ''
    
    def feed(self, data):
        """Feed data to the parser. It takes the whole tex document as a single string."""
        self.rawdata = self.rawdata + data
    
    def filter(self):
        rawdata = self.rawdata
        if self.clean_precommath