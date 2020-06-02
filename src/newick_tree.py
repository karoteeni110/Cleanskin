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

def computeNewick(df):
    g = getCluster(df)
    tree, ll = getTree(g)
    leaf_names = getLeafnames(df,ll)
    newick = getNewick(tree, "", leaf_names)
    return newick

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

def show_ensemble_dist_plot(csvpath):
    df = pd.read_csv(csvpath)
    m = df.groupby(['N']).mean()
    df = df.rename(columns={'dist':'RF distance'})
    m = m.rename(columns={'dist':'Mean distance'})

    ax = df.plot.hexbin(x='N',y='RF distance',gridsize=30)
    m.plot(ax=ax)
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

def avg_n_secvec(vec_path_list):
    finalvec = 0
    for vec_path in vec_path_list:
        vec_df = getDf(vec_path)

        if type(finalvec) == int:
            finalvec = vec_df
        else:
            finalvec += vec_df
    
    # print()
    return finalvec.div(len(vec_path_list))

def sample_n(l, n, replace=False):
    shuffle(l)
    return l[:n]

def vec2newick(vec,dst):
    g = getCluster(vec)
    tree, ll = getTree(g)
    leaf_names = getLeafnames(vec,ll)
    newick = getNewick(tree, "", leaf_names)
    with open(dst,'w') as f:
        f.write(newick)
    plt.close('all')

def get_rf(secvec1,secvec2):
    tree_dir = data_path
    t1path, t2path = join(tree_dir,'t1.tree'), join(tree_dir,'t2.tree') 
    vec2newick(secvec1, t1path)
    vec2newick(secvec2, t2path)

    #cmd = 'rf -a %s %s ' % (t1path, t2path)
    cmd = 'rf %s %s' % (t1path, t2path)
    dist = run(cmd, shell=True, stdout=PIPE, text=True).stdout.replace('\n','')

    return dist

def n_ensemble_treepair(all_vec_path, n, repeat=1000):
    dists = []
    
    for i in range(repeat):
        ensemble1 = avg_n_secvec(sample_n(all_vec_path, n)) 
        ensemble2 = avg_n_secvec(sample_n(all_vec_path, n))
        dist = get_rf(ensemble1, ensemble2) 
        dists.append(dist)

        if (i+1) % 10 == 0:
            print(n,':',i+1,'/',repeat)

    df = pd.DataFrame(data={'N':[n]*len(dists), 'dist':dists})
    return df

def get_ensembles():
    dist_dfs = []
    all_vec_path = [join('/Users/Karoteeni/coooode/Cleanskin/data/cs_kld/130kdoc_secvec',i) 
                    for i in listdir('/Users/Karoteeni/coooode/Cleanskin/data/cs_kld/130kdoc_secvec')
                    if i[-3:] == 'txt']
    for N in range(1,51):
        dist_dfs.append(n_ensemble_treepair(all_vec_path,N))
    all_dist_df = pd.concat(dist_dfs)
    all_dist_df.to_csv(join(data_path,'ensemble_n.csv'),index=False)

if __name__ == "__main__":
    # srcdir = data_path+'/cs_kld/6kdoc_secvec'
    # for fn in listdir(srcdir):
    #     src = srcdir + '/' + fn
    #     dst = join(data_path, 'newickTrees/' + fn[:-3] + 'tree')
    #     # print(dst)
    #     saveNewicktree(src, dst)

    # src = '/Users/Karoteeni/coooode/Cleanskin/data/130kdoc_30x100_secvec.txt'
    # dst = join(data_path, '130kavg_newick.tree')
    # saveNewicktree(src, dst)

    # rfcsv = join(data_path, '6kdoc_rfdist.csv')
    # computeRf(join(data_path, '6kdoc_newickTrees'), rfcsv, absolute=False)
    # show_bootstrap_kde(rfcsv)

    # rfcsv = join(data_path, 'CHIIR_vs_130k.csv')
    # CHIIRvs100_Rf(join(data_path, '6kdoc_newickTrees'), rfcsv, absolute=False)
    # show_kde(rfcsv)

    # # d1 = pd.read_csv(join(data_path, '6kdoc_rfdist.csv')).dist
    # d2 = pd.read_csv(join(data_path, '130kdoc_rfdist.csv')).dist
    # # d1 = pd.read_csv(join(data_path, 'CHIIR_vs_6k.csv')).dist
    # # d2 = pd.read_csv(join(data_path, 'CHIIR_vs_130k.csv')).dist
    # # df = pd.DataFrame({
    # # '6k data set': d1,
    # # '130k data set': d2,
    # # })
    # ax = d2.plot.hist()
    # plt.show()

    # get_ensembles()
    show_ensemble_dist_plot('/Users/Karoteeni/coooode/Cleanskin/data/ensemble_n.csv')


