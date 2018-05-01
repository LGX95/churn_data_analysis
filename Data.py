from collections import defaultdict
import numpy as np
import pandas as pd


class Data():
    """加载数据并清洗

    Args:
        path: csv 文件的路径
    """

    def __init__(self, path):
        self.df_ori = self._read_data(path)
        self.df_num = self._num_data()

    def _read_data(self, path):
        df = pd.read_csv(path)
        df.replace(' ', np.nan, inplace=True)
        df.dropna(inplace=True)
        df['TotalCharges'] = df['TotalCharges'].map(float)
        return df

    def _num_data(self):
        new_df = self.df_ori.copy()
        non_num_columns = list(self.df_ori.select_dtypes(exclude=[np.number]))
        yes_no_other_columns = [c for c in non_num_columns
                                if 'No' in self.df_ori[c].unique()
                                and 'Yes' in self.df_ori[c].unique()]
        yes_no_other_class_to_idx = {'No': 0, 'Yes': 1, 'Other': 2}
        self.yes_no_other_class_to_idx = yes_no_other_class_to_idx

        def yes_no_other_func(x): return np.where(
            x == 'No', 0, np.where(x == 'Yes', 1, 2))
        new_df.loc[:, yes_no_other_columns] = \
            self.df_ori.loc[:, yes_no_other_columns].apply(yes_no_other_func)
        not_yes_columns = [
            c for c in non_num_columns if c not in yes_no_other_columns]
        not_yes_columns.remove('customerID')
        classes_dict = defaultdict(dict)
        for col in not_yes_columns:
            classes = list(self.df_ori.loc[:, col].unique())
            classes.sort()
            classes_dict[col] = {classes[i]: i for i in range(len(classes))}
            new_df.loc[:, col] = self.df_ori.loc[:, col].map(classes_dict[col])
        self.classes_dict = classes_dict
        return new_df
