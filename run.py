import numpy as np
from flask import Flask, render_template
from pyecharts import Line


app = Flask(__name__)


REMOTE_HOST = "https://cdn.bootcss.com/echarts/4.0.4/"


@app.route('/')
def index():
    line = relu()
    return render_template('index.html',
                           myechart=line.render_embed(),
                           host=REMOTE_HOST,
                           script_list=line.get_js_dependencies())


def relu():
    x = np.arange(-5, 6, 1)
    y = np.maximum(0, x)
    line = Line('ReLU')
    line.add('', x, y, )
    return line


if __name__ == '__main__':
    app.run(debug=True)
