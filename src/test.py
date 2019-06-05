from reader import Cleaner
from paths import *

# == Loading data ==
data = get_tex(tester_tex_path) # TODO get_tex

# == Initialize ==
detexer = Cleaner()
# 