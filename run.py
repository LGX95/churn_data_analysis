import numpy as np
import pandas as pd
from flask import Flask, render_template
from pyecharts import Bar, Line, Overlap


app = Flask(__name__)


REMOTE_HOST = "https://cdn.bootcss.com/echarts/4.0.4/"


@app.route('/')
def index():
    graph = get_graph()
    return render_template('index.html',
                           myechart=graph.render_embed(),
                           host=REMOTE_HOST,
                           script_list=graph.get_js_dependencies())


def get_data():
    """读取csv文件信息，返回 total_charges 即其累计比例

    Return:
        total_charges: 从大到小排序的 TotalCharges Series
    """
    customer_df = pd.read_csv(
        '~/Downloads/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    total_charges = customer_df['TotalCharges']
    total_charges = total_charges.replace(' ', np.nan)
    total_charges.dropna(inplace=True)
    total_charges = total_charges.map(float)
    total_charges = total_charges.sort_values(ascending=False)
    charges_proportion = total_charges.cumsum() / sum(total_charges) * 100
    return total_charges, charges_proportion


def get_graph():
    """得到 Total Charges 的图

    return:
        overlap: Overlap 实例，添加了柱状图和折线图
    """
    total_charges, charges_proportion = get_data()
    # 区域缩放的选项，同时用于 bar 和 line
    dataroom_opt = {
        'is_datazoom_show': True,
        'datazoom_type': 'both',
        'datazoom_range': [0, 50],
    }
    bar = Bar('Total Charges')
    bar.add('Total Charges', total_charges.index, total_charges,
            xaxis_name='customer id', yaxis_name='total charges',
            yaxis_name_gap=50, **dataroom_opt)
    line = Line()
    line.add('Cumulative Proportion', charges_proportion.index,
             charges_proportion, yaxis_name='cumulative proportion',
             yaxis_formatter="%", yaxis_name_gap=50, **dataroom_opt)
    # 结合 bar 和 line 叠加画在同张图上
    overlap = Overlap()
    overlap.add(bar)
    overlap.add(line, yaxis_index=1, is_add_yaxis=True)
    return overlap


if __name__ == '__main__':
    app.run(debug=True)
