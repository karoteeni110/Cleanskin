# Get paths to the data and results directories.
from os.path import dirname, join, realpath
src_path = dirname(realpath(__file__))
repo_path = dirname(src_path)
data_path = join(repo_path,'data')
results_dir = join(repo_path, 'results')

tester_tex_path = join(data_path, 'paper.tex')

if __name__ == "__main__":
    # Check that we are reading the correct file
    print('src', src_path)
    print('repo', repo_path)
    print('data', data_path)
    print('results', results_dir)
    print('tester', tester_tex_path)