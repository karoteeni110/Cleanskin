# NEVER MOVE THIS FILE!!!!!!
from os.path import dirname, join, realpath, basename
src_path = dirname(realpath(__file__))
repo_path = dirname(src_path)
data_path = join(repo_path,'data')
results_path = join(repo_path, 'results')

data0001 = join(data_path, '/0001')
data0002 = join(data_path, '/0002')
data1701 = join(data_path, '/1701')


if __name__ == "__main__":
    # Check that we are reading the correct file
    print('src', src_path)
    print('repo', repo_path)
    print('data', data_path)
    print('results', results_path)
    print('datapath basename:', basename(data_path))