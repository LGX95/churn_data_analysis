import numpy as np
import pandas as pd
from flask import Flask, render_template
from flask.templating import Environment
from pyecharts import Bar, Line, Overlap, Scatter, Radar, Pie
from pyecharts.engine import ECHAERTS_TEMPLATE_FUNCTIONS
from pyecharts.conf import PyEchartsConfig

from Data import Data


class FlaskEchartsEnvironment(Environment):
    def __init__(self, *args, **kwargs):
        super(FlaskEchartsEnvironment, self).__init__(*args, **kwargs)
        self.pyecharts_config = PyEchartsConfig(jshost='/static/js')
        self.globals.update(ECHAERTS_TEMPLATE_FUNCTIONS)


class MyFlask(Flask):
    jinja_environment = FlaskEchartsEnvironment


app = MyFlask("/")


data = Data('~/Downloads/WA_Fn-UseC_-Telco-Customer-Churn.csv')
colors = ['#C23531', '#2F4554', '#61A0A8', '#D48265']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/all')
def all():
    return render_template('all.html')


@app.route('/clusters')
def clusters():
    tsne_graph = get_tsne_graph()
    net_service_radar = get_internet_services_radar()
    number_bar = get_number_bar()
    charges_scatter = get_charges_scatter()
    tenure_bar = get_tenure_bar()
    return render_template('clusters.html',
                           tsne=tsne_graph,
                           number_bar=number_bar,
                           tenure_bar=tenure_bar,
                           net_service_radar=net_service_radar,
                           charges_scatter=charges_scatter,
                           )


def get_tsne_graph():
    """得到所有分类数据二维化的图
    """
    scatter = Scatter('所有数据二维化后的分类图', width="100%")
    clusters = np.load('sorted_clusters.npy')
    unique_cluster = np.unique(clusters)
    X_tsne = np.load('X_tsne.npy')
    for i in unique_cluster:
        X = X_tsne[clusters == i]
        scatter.add(str(i), X[:, 0], X[:, 1])
    return scatter


def get_charges_scatter():
    """聚类后 MonthlyCharges 和 TotalCharges 的散点图
    """
    scatter = Scatter('MonthlyCharges 和 TotalCharges 的散点图')
    for i in range(len(data.clusters)):
        scatter.add(str(i), data.clusters[i]['MonthlyCharges'].values,
                    data.clusters[i]['TotalCharges'].values,
                    legend_pos='right')
    return scatter


def get_number_bar():
    """聚类结果的数量柱状图
    """
    attr = [str(i) for i in range(4)]
    bar = Bar('分类数量图')
    for i in range(len(data.clusters)):
        value = [None] * 4
        value[i] = len(data.clusters[i])
        bar.add(str(i), attr, value, is_stack=True, is_label_show=True)
    return bar


def get_number_pie():
    """聚类结果的数量饼图
    """
    attr = [str(i) for i in range(4)]
    value = [len(data.clusters[i]) for i in range(len(data.clusters))]
    pie = Pie('分类数量图')
    pie.add('', attr, value, is_label_show=True, label_formatter="{c}")
    return pie


def get_tenure_bar():
    """tenure 柱状图
    """
    bar = Bar("Tenure")
    series0 = pd.Series([0] * 72, index=range(1, 73))
    for i in range(len(data.clusters)):
        value_count = data.clusters[i]['tenure'].value_counts().sort_index()
        bar.add(str(i), series0.index, series0.add(value_count, fill_value=0),
                is_stack=True, is_datazoom_show=True, datazoom_type='both',
                datazoom_range=[0, 100])
    return bar


def get_internet_services_radar():
    """与internet service 相关的服务的雷达图
    """
    internet_service_columns = ['OnlineSecurity', 'OnlineBackup',
                                'DeviceProtection', 'TechSupport',
                                'StreamingTV', 'StreamingMovies']
    schema = [(col, 1) for col in internet_service_columns]
    radar = Radar('与 Internet Service 相关的服务')
    radar.config(schema)
    for i in range(len(data.clusters)):
        yes = data.clusters[i].loc[:, internet_service_columns] == 'Yes'
        result = yes.sum(0) / len(data.clusters[i])
        radar.add(str(i), [result.values], item_color=colors[i])
    return radar


def get_graph():
    """得到 Total Charges 的图

    return:
        overlap: Overlap 实例，添加了柱状图和折线图
    """
    total_charges, charges_proportion = \
        data.get_sorted_and_proportion('TotalCharges')
    # 区域缩放的选项，同时用于 bar 和 line
    dataroom_opt = {
        'is_datazoom_show': True,
        'datazoom_type': 'both',
        'datazoom_range': [0, 50],
    }
    bar = Bar('Total Charges')
    bar.add('Total Charges', list(range(len(total_charges))), total_charges,
            xaxis_name='cumtomer number', yaxis_name='total charges',
            yaxis_name_gap=50, yaxis_max=10000, **dataroom_opt)
    line = Line()
    line.add('Cumulative Proportion', list(range(len(charges_proportion))),
             charges_proportion, yaxis_name='cumulative proportion',
             yaxis_formatter="%", yaxis_name_gap=50, yaxis_max=100,
             **dataroom_opt)
    # 结合 bar 和 line 叠加画在同张图上
    overlap = Overlap()
    overlap.add(bar)
    overlap.add(line, yaxis_index=1, is_add_yaxis=True)
    return overlap


if __name__ == '__main__':
    app.run(debug=True)
