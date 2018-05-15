import numpy as np
import pandas as pd
from kmodes.kprototypes import KPrototypes
from sklearn.manifold import TSNE

from Data import Data


data_root = '~/Downloads/WA_Fn-UseC_-Telco-Customer-Churn.csv'
N_CLASS = 4


def sort_clusters(clusters):
    clusters_series = pd.Series(clusters)
    clusters_to_idx = {clusters: i for i, clusters in enumerate(
        clusters_series.value_counts().index)}
    sorted_clusters_series = clusters_series.map(lambda x: clusters_to_idx[x])
    return sorted_clusters_series.values


if __name__ == '__main__':
    # read csv data
    df = pd.read_csv(data_root, na_values={'TotalCharges': ' '})
    df.dropna(inplace=True)
    # k-prototypes
    X = df.iloc[:, 1:].copy()
    kproto = KPrototypes(n_clusters=N_CLASS, init='Cao', verbose=2)
    cate = [i for i, t in enumerate(X.dtypes) if t == np.object]
    clusters = kproto.fit_predict(X.values, categorical=cate)
    np.save('raw_clusters.npy', arr=clusters)
    # sort cluster result
    sorted_clusters = sort_clusters(clusters)
    np.save('sorted_clusters.npy', arr=sorted_clusters)

    # tsne X
    print('\nStarting tsne X...')
    data = Data(data_root)
    X_num = data.df_num
    tsne = TSNE(n_components=2, init='pca', random_state=0)
    X_tsne = tsne.fit_transform(X_num)
    np.save('X_tsne.npy', arr=X_tsne)
