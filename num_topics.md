## How to select the number of topics

### 1 Check perpelexity

Gist: Split data into training & held-out sets. Train model & test its perplexity on the held-out set.

**BUT**: Isn't it the same with our KL divergence measurement? It's equavalent to training multiple models and choose the one that yields lowest KLD?

> See: [Selecting model parameters (Stanford Topic Modeling Toolbox)](https://nlp.stanford.edu/software/tmt/tmt-0.4/)

### 2 Check coherence value

Gist: Plot the topic coherence value over number of topics and choose the elbow point.

Topic coherence evaluates topics (with "the confirmation measure" like PMI), then combines the results into one number. 

> See: 
[Gensim: How to find the optimal number of topics for LDA?](https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/#17howtofindtheoptimalnumberoftopicsforlda), [What is topic coherence?](https://rare-technologies.com/what-is-topic-coherence/)

### 3 Nonparametric model: HDP (Hierachical dirichlet process)

Tunes the number automatically during the training process. **BUT**:

> Even in such models, some parameters remain to be tuned, such as the topic smoothing and term smoothing parameters.

> See: https://people.eecs.berkeley.edu/~jordan/papers/hierarchical-dp.pdf 
