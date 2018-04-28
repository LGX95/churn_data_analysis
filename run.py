import numpy as np
import pandas as pd
from flask import Flask, render_template
from pyecharts import Bar


app = Flask(__name__)


REMOTE_HOST = "https://cdn.bootcss.com/echarts/4.0.4/"


@app.route('/')
def index():
    bar = get_bar()
    return render_template('index.html',
                           myechart=bar.render_embed(),
                           host=REMOTE_HOST,
                           script_list=bar.get_js_dependencies())


def get_total_charges():
    customer_df = pd.read_csv(
        '~/Downloads/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    total_charges = customer_df['TotalCharges']
    total_charges = total_charges.replace(' ', np.nan)
    total_charges.dropna(inplace=True)
    total_charges = total_charges.map(float)
    total_charges = total_charges.sort_values(ascending=False)
    return total_charges


def get_bar():
    total_charges = get_total_charges()
    bar = Bar('Total Charges')
    bar.add('Total Charges', total_charges.index, total_charges,
            xaxis_name='customer id', is_datazoom_show=True,
            datazoom_type='both', datazoom_range=[0, 75])
    return bar


if __name__ == '__main__':
    app.run(debug=True)
