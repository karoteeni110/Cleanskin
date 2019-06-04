# Get paths to the data and results directories.
from os.path import dirname, join
src_path = dirname(os.path.realpath(__file__))
repo_path = dirname(src_path)
data_dir = join(repo_path,'data')
results_dir = join(repo_path, 'results')