## How to select the number of topics

### 1 Check perpelexity

Gist: Split data into training & held-out sets. Train model & test its perplexity on the held-out set.

(What if we check KLD on different sets?)

> See: [Selecting model parameters (Stanford Topic Modeling Toolbox)](https://nlp.stanford.edu/software/tmt/tmt-0.4/)

### 2 Check coherence

Gist: Plot the topic coherence value over number of topics and choose the elbow point.

Topic coherence evaluates topics (with "the confirmation measure" such as PMI), then combines the results into one number. 

> See: 
[Gensim: How to find the optimal number of topics for LDA?](https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/#17howtofindtheoptimalnumberoftopicsforlda), [What is topic coherence?](https://rare-technologies.com/what-is-topic-coherence/)

### 3 Cluster measurements

Take each topic as a cluster and evaluate the effectiveness of different number of them.

Metrics:

1. [The elbow method](https://en.wikipedia.org/wiki/Elbow_method_(clustering)): plots the percentage of variance explained by the clusters against the number of clusters, and take the elbow point.

2. Akaike information criterion ([AIC_wikipedia](https://en.wikipedia.org/wiki/Akaike_information_criterion)) or Bayesian information criterion ([BIC_wikipedia](https://en.wikipedia.org/wiki/Bayesian_information_criterion)) for x-means clustering

3. [Silhouette Method](https://en.wikipedia.org/wiki/Silhouette_(clustering)): measures how closely it is matched to data within its cluster and how loosely it is matched to data of the neighbouring cluster, i.e. the cluster whose average distance from the datum is lowest.

4. Other confusing methods in ↓

> See:
[Determining the number of clusters in a data set - Wikipedia](https://en.wikipedia.org/wiki/Determining_the_number_of_clusters_in_a_data_set)

### 4 Nonparametric model: HDP (Hierachical dirichlet process)

Tunes the number automatically during the training process; topics' interpretability not gauranteed. 

**BUT**:

> Even in such models, some parameters remain to be tuned, such as the topic smoothing and term smoothing parameters.

> See: https://people.eecs.berkeley.edu/~jordan/papers/hierarchical-dp.pdf 
