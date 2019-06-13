# Get paths to the data and results directories.
from os.path import dirname, join, realpath
src_path = dirname(realpath(__file__))
repo_path = dirname(src_path)
data_path = join(repo_path,'data')
results_path = join(repo_path, 'results')

def debib_dir(subdirn):
    debib_dir = join(results_path, subdirn)
    return debib_dir

if __name__ == "__main__":
    # Check that we are reading the correct file
    print('src', src_path)
    print('repo', repo_path)
    print('data', data_path)
    print('results', results_path)