import os

f = '/home/yzan/Desktop/try/cluster/1701_001/haha.txt'
with open(f, 'r') as haha:
    # sizes = [float(line.split()[4][:-1]) for line in haha.readlines()]
    tex_article = set(line.split()[-1].split('/')[1] for line in haha.readlines())
    # totalsize = sum(sizes)
    # print(totalsize)
    print(len(tex_article))

    print(276.2 * 413)  