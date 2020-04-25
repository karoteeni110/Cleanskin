import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from os.path import join
from os import listdir
from scipy.cluster import hierarchy
import string 
import numpy as np

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

if __name__ == "__main__":
    # fn = '6kdoc_70x100_secvec.txt'
    srcdir = data_path+'/cs_kld/6kdoc_secvec'
    for fn in listdir(srcdir):
        src = srcdir + '/' + fn
        dst = join(data_path, 'newickTrees/' + fn[:-3] + 'tree')
        # print(dst)
        saveNewicktree(src, dst)
    

