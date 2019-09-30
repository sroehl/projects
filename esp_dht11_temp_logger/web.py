from flask import Flask, make_response, request
from sql_to_plot import *
import time
import os

app = Flask(__name__)

next_create = 0

@app.route('/')
def chart():
    global next_create
    chart_path = os.path.join('resources', 'temp.svg')
    print('next: {}'.format(next_create))
    print(time.time())
    if time.time() > next_create:
        print('Creating new graph')
        days = int(request.args.get('days', 7))
        data_set = load_data(days=days)
        make_line_chart(data_set, chart_path)
        next_create = time.time() + 60
    response = make_response(open(chart_path).read())
    response.content_type = 'image/svg+xml'
    return response

if __name__=='__main__':
    app.run(host='0.0.0.0', port=7001, debug=True)
