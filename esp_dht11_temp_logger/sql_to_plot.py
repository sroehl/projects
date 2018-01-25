import pygal
import sqlite3
import time
import math


def load_data(start_time=None, end_time=None, days=7, db_name='sensor.db'):
    if start_time is None:
        start_time = round(time.time()) - (60*60*24*days)
    if end_time is None:
        end_time = round(time.time())
    time = []
    vals = []
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    stmt = 'select time, value from sensor where time >= ? and time <= ? and name="temp"  order by time'
    for row in cur.execute(stmt, (start_time, end_time)):
        time.append(row[0])
        vals.append(row[1])
    #print("dataset length: {}".format(len(data_set)))
    return (time,vals)


def make_line_chart(time, vals, filename=None):
    config = pygal.Config()
    config.defs.append('''<linearGradient id="gradient-3" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="#ffffff" />
        <stop offset="100%" stop-color="#0000ff " />
        </linearGradient>''')
    config.css.append('''inline:
      .color-2 {
        fill: url(#gradient-3    !important;
        stroke: url(#gradient-3) !important;
      }''')
    line_chart = pygal.DateTimeLine(x_label_rotation=35, truncate_label=-1,
                                    x_value_formatter=lambda dt: dt.strftime('%b %d %Y at %I:%M:%S %p'),
                                    stroke_style={'width': 5},
                                    config=config)
    line_chart.add('Temp', vals, show_dots=True)
    if filename is not None:
        line_chart.render_to_file(filename)
    else:
        return line_chart.render()

if __name__ == '__main__':
    make_line_chart(ds, filename='temp.svg')
