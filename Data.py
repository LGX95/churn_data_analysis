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

    def get_churn(self, churn, num=False):
        """返回一个以churn分开的df

        Args:
            churn: (string) 'Yes' 或者 'No'
        """
        assert (churn == 'Yes' or churn == 'No'), \
            'churn must be "Yes" or "No", not "{}"'.format(churn)
        if num:
            # churn = int(churn == 'Yes')
            return self.df_num[self.df_ori['Churn'] == churn]
        else:
            return self.df_ori[self.df_ori['Churn'] == churn]

    def get_sorted_and_proportion(self, col, ascending=False):
        """返回一个排序好的Series即其累计比例

        Args:
            col: (string) 列名 eg: 'TotalCharges'
            ascending: (bool) 是否从小到大，默认从大到小

        Return:
            sorted_s: 排序完成的Series
            proportion: 排序完成的Series的累计比例
        """
        series = self.df_ori[col]
        sorted_s = series.sort_values(ascending=ascending)
        proportion = sorted_s.cumsum() / sum(series) * 100
        return sorted_s, proportion

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
