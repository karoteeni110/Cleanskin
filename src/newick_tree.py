import seaborn as sns
import pandas as pd
from pandas.plotting import bootstrap_plot
import matplotlib.pyplot as plt
from os.path import join, basename
from os import listdir
from scipy.cluster import hierarchy
from itertools import combinations
from random import shuffle
import string 
import numpy as np
from subprocess import run, PIPE

from paths import data_path
from kldiv import get_acro2cate_dict

acro2cate = get_acro2cate_dict()
name2acro = {acro2cate[k]:k for k in acro2cate}

def getDf(fpath):
    #df = pd.read_csv('paper_topic_vectors.txt')
    df = pd.read_csv(fpath)
    df = df.set_index('name')
    df = df.sort_index()
    return df

def getNewick(node, newick, leaf_names):
    if node.is_leaf():
        # return "%s:%.2f%s" % (leaf_names[node.id], parentdist - node.dist, newick)
        return "%s%s" % (leaf_names[node.id], newick)
    else:
        if len(newick) > 0:
            # newick = "):%.2f%s" % (parentdist - node.dist, newick)
            newick = ")%s" % newick
        else:
            newick = ");"
        newick = getNewick(node.get_left(), newick, leaf_names)
        newick = getNewick(node.get_right(), ", %s" % (newick), leaf_names)
        newick = "(%s" % (newick)
        return newick

def getCluster(df):
    sns.set()
    sns.set(font_scale=0.6)
    g = sns.clustermap(df, metric='euclidean', method='complete', linewidths=.25, col_cluster=True, square=True, cmap="mako", robust=True)
    #plt.show()
    return g

def getTree(g):
    Z = g.dendrogram_row.linkage
    tree = hierarchy.to_tree(Z,False)
    leaveslist = hierarchy.leaves_list(Z)
    return tree, leaveslist

def getLeafnames(df,leaveslist):
    leaf_names = {leafid:name2acro[df.index[leafid]] for leafid in leaveslist}
    # leaf_names = {leafid:df.index[leafid] for leafid in leaveslist}
    return leaf_names

def saveNewicktree(src, dst):
    df = getDf(src)
    g = getCluster(df)
    tree, ll = getTree(g)
    leaf_names = getLeafnames(df,ll)
    newick = getNewick(tree, "", leaf_names)
    with open(dst,'w') as f:
        f.write(newick)
    plt.close('all')

def computeRf(tree_dir, dst, absolute=False):
    fn = listdir(tree_dir)
    tpairs = combinations(fn,2)
    
    # shuffle(fn)
    # tpairs = [(fn[i], fn[i+1]) for i in range(0,len(fn),2)]
    
    rows_list = []
    c = 1
    for t1,t2 in tpairs:
        t1path, t2path = join(tree_dir,t1), join(tree_dir,t2)
        if absolute:
            cmd = 'rf -a %s %s ' % (t1path, t2path)
        else:
            cmd = 'rf %s %s' % (t1path, t2path)
        dist = run(cmd, shell=True, stdout=PIPE, text=True).stdout.replace('\n','')
        
        row = {'t1':t1,'t2':t2,'dist':dist}
        rows_list.append(row)

        if c % 10 == 0:
            print(c,'/', 4950)
        c+=1

        # if c == 100:
        #     break

    print('RF Computation done.')
    dist_df = pd.DataFrame(rows_list)
    dist_df.to_csv(dst,index=False)

def CHIIRvs100_Rf(tree_dir, dst, absolute=False):
    fn = listdir(tree_dir)
    
    rows_list = []
    c = 1
    for t1 in fn:
        t2 = 'CHIIR_newick.tree'
        t1path, t2path = join(tree_dir,t1), join(data_path, t2)
        
        if absolute:
            cmd = 'rf -a %s %s ' % (t1path, t2path)
        else:
            cmd = 'rf %s %s' % (t1path, t2path)
        dist = run(cmd, shell=True, stdout=PIPE, text=True).stdout.replace('\n','')
        
        row = {'t1':t1,'t2':t2,'dist':dist}
        rows_list.append(row)

        if c % 10 == 0:
            print(c,'/', len(fn))
        c+=1

        # if c == 100:
        #     break

    print('RF Computation done.')
    dist_df = pd.DataFrame(rows_list)
    dist_df.to_csv(dst,index=False)

def show_kde(csvpath):
    df = pd.read_csv(csvpath)
    ax = df.dist.plot.kde()
    plt.show()

def show_bootstrap_kde(csvpath):
    df = pd.read_csv(csvpath)
    
    sampling = []
    repeat_n = 1000
    for i in range(repeat_n):
        sample = df.dist.sample(n=len(df.dist), replace=True)
        sampling.append(sample.mean())
    sampling = pd.Series(sampling)
    
    # Sanity check
    ax = sampling.plot.hist()
    plt.show()

    bootstrap_plot(sampling, size=len(df.dist), samples=repeat_n)
    plt.show()


if __name__ == "__main__":
    # srcdir = data_path+'/cs_kld/6kdoc_secvec'
    # for fn in listdir(srcdir):
    #     src = srcdir + '/' + fn
    #     dst = join(data_path, 'newickTrees/' + fn[:-3] + 'tree')
    #     # print(dst)
    #     saveNewicktree(src, dst)

    # src = '/Users/Karoteeni/coooode/scilit_graphs/section_structure_vectors.txt'
    # dst = join(data_path, 'CHIIR_newick')
    # saveNewicktree(src, dst)

    # rfcsv = join(data_path, '6kdoc_rfdist.csv')
    # computeRf(join(data_path, '6kdoc_newickTrees'), rfcsv, absolute=False)
    # show_bootstrap_kde(rfcsv)

    rfcsv = join(data_path, 'CHIIR_vs_130k.csv')
    CHIIRvs100_Rf(join(data_path, '130kdoc_newickTrees'), rfcsv, absolute=False)


    # show_bootstrap_sample(join(data_path, '130kdoc_rfdist_a.csv'))
    

