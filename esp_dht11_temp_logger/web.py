from flask import Flask, make_response, request
from sql_to_plot import *
import time
import os

app = Flask(__name__)

last_created = {}

@app.route('/')
def chart():
    chart_path = os.path.join('resources', 'temp.svg')
    if 'temp' not in last_created or (last_created['temp'] + (5 *60)) > time.time():
        days = int(request.args.get('days', 7))
        data_set = load_data_dynamodb(days=days)
        make_line_chart(data_set, chart_path)
        last_created['temp'] = time.time()
    response = make_response(open(chart_path).read())
    response.content_type = 'image/svg+xml'
    return response

if __name__=='__main__':
    app.run(host='0.0.0.0', port=7001, debug=True)
