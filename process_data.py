import numpy as np
import pandas as pd
from kmodes.kprototypes import KPrototypes


data_root = '~/Downloads/WA_Fn-UseC_-Telco-Customer-Churn.csv'
N_CLASS = 4


if __name__ == '__main__':
    # read csv data
    df = pd.read_csv(data_root, na_values={'TotalCharges': ' '})
    df.dropna(inplace=True)
    # k-prototypes
    X = df.iloc[:, 1:].copy()
    kproto = KPrototypes(n_clusters=N_CLASS, init='Cao', verbose=2)
    cate = [i for i, t in enumerate(X.dtypes) if t == np.object]
    clusters = kproto.fit_predict(X.values, categorical=cate)
    np.save('clusters.npy', arr=clusters)
