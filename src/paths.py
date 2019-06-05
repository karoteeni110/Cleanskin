# Get paths to the data and results directories.
from os.path import dirname, join, realpath
src_path = dirname(realpath(__file__))
repo_path = dirname(src_path)
data_path = join(repo_path,'data')
results_dir = join(repo_path, 'results')

tester_tex_path = join(data_path, '/tester.tex')

if __name__ == "__main__":
    # Check that we are reading the correct file
    with open(data_path) as texfiles:
        print(texfiles.readline())