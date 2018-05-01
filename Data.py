import numpy as np
import pandas as pd


class Data():
    """加载数据并清洗

    Args:
        path: csv 文件的路径
    """

    def __init__(self, path):
        self.df_ori = self._read_data(path)

    def _read_data(self, path):
        df = pd.read_csv(path)
        df.replace(' ', np.nan, inplace=True)
        df.dropna(inplace=True)
        df['TotalCharges'] = df['TotalCharges'].map(float)
        return df

