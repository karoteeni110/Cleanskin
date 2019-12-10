import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('my_secvec.txt')
#df = pd.read_csv('paper_topic_vectors.txt')
df = df.set_index('name')


sns.set()
sns.set(font_scale=0.6)
#g = sns.clustermap(df, metric='euclidean', method='average', linewidths=.25, col_cluster=False, square=True, cmap="mako", robust=True)
g = sns.clustermap(df, metric='euclidean', method='complete', linewidths=.25, col_cluster=True, square=True, cmap="mako", robust=True)
#g = sns.clustermap(df, metric='euclidean', method='complete', linewidths=.25, col_cluster=True, square=False, cmap="mako", robust=True)

ax = g.ax_heatmap
ax.set_ylabel('')    
ax.set_xlabel('')
plt.setp(ax.yaxis.get_majorticklabels(), rotation=0)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)

g.ax_col_dendrogram.set_visible(False)

g.savefig("my_tree.pdf")

plt.show()

