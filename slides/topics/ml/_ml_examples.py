#%%
import pandas as pd
from matplotlib import pyplot as plt
from scipy.cluster import hierarchy
import numpy as np
import seaborn as sns
 
# Data set
iris = sns.load_dataset('iris')


df = iris.iloc[:,:4]

# Calculate the distance between each sample
Z = hierarchy.linkage(df, 'average')
ind = hierarchy.cut_tree(Z,3)

#%% 
# Plot with Custom leaves
hierarchy.set_link_color_palette(['m','b','g'])
hierarchy.dendrogram(Z, leaf_rotation=90, leaf_font_size=8, color_threshold=1.8, above_threshold_color='grey');
plt.show()
# %%
hierarchy.set_link_color_palette(['m','b','g'])
hierarchy.dendrogram(Z, orientation="left", color_threshold=1.8, above_threshold_color='grey' );
plt.show()

## Unsupervised learning
# %%
from sklearn.decomposition import PCA
pca = PCA()

prcomp = pca.fit_transform(df)

out = pd.DataFrame(prcomp, columns = ['PCA1','PCA2','PCA3','PCA4'])
out = pd.concat((out, iris.species), axis=1)

fig,ax = plt.subplots(1,3, sharex=False, sharey=False)
sns.scatterplot(data=out, x='PCA1',y='PCA2', hue='species', ax=ax[0])
ax[0].set_ylabel('')
ax[0].set_xlabel('')
ax[0].set_title('PCA')


from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, perplexity=5, n_iter=300)
out = pd.DataFrame(tsne.fit_transform(df), columns = ['TSNE1','TSNE2'])
out = pd.concat((out, iris.species), axis=1)

sns.scatterplot(data = out, x = 'TSNE1', y = 'TSNE2', hue='species', ax=ax[1])
ax[1].set_ylabel('')
ax[1].set_xlabel('')
ax[1].set_title('t-SNE')

from umap import UMAP
u = UMAP()
embedding = pd.DataFrame(u.fit_transform(df), columns = ['UMAP1','UMAP2'])
embedding = pd.concat((embedding, iris.species), axis=1)
sns.scatterplot(data=embedding, x='UMAP1', y='UMAP2', hue='species', ax=ax[2])
ax[2].set_ylabel('')
ax[2].set_xlabel('')
ax[2].set_title('UMAP')

plt.show()
# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix, plot_precision_recall_curve, plot_roc_curve
from sklearn.inspection import plot_partial_dependence
from sklearn.calibration import calibration_curve
from yellowbrick.model_selection import FeatureImportances

brca = pd.read_csv('data/brca.csv').dropna()
y = brca.pop('Class').astype('category').cat.codes.values
X = brca.values

rfc = RandomForestClassifier();
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=44)
rfc.fit(X_train, y_train);

#%%
fi = pd.DataFrame({'features': brca.columns, 'importance': rfc.feature_importances_})
sns.barplot(data = fi, x = 'importance', y = 'features', color='blue')
plt.show()

viz = FeatureImportances(RandomForestClassifier());
viz.fit(brca,y);
viz.show();
# %%
plot_roc_curve(rfc, X_test, y_test);
plt.plot([0,1],[0,1], '--')
plt.show()

#%%
plot_precision_recall_curve(rfc, X_test, y_test);
plt.show()

# %%
