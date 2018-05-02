from flask import Flask, render_template
from pyecharts import Bar, Line, Overlap

from Data import Data


app = Flask(__name__)


REMOTE_HOST = "https://cdn.bootcss.com/echarts/4.0.4/"


data = Data('~/Downloads/WA_Fn-UseC_-Telco-Customer-Churn.csv')


@app.route('/')
def index():
    graph = get_graph()
    return render_template('index.html',
                           myechart=graph.render_embed(),
                           host=REMOTE_HOST,
                           script_list=graph.get_js_dependencies())


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
