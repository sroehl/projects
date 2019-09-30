import pygal
from pygal.style import DarkGreenBlueStyle
import sqlite3
import time


def load_data(start_time=None, end_time=None, days=7, db_name='sensor.db'):
    if start_time is None:
        start_time = round(time.time()) - (60 * 60 * 24 * days)
    if end_time is None:
        end_time = round(time.time())
    dt = []
    vals = []
    conn = sqlite3.connect(db_name)
    rows = []
    cur = conn.cursor()
    print(start_time)
    stmt = 'select time, value from sensor where time >= ? and time <= ? and name="temp"  order by time'
    last_tuple = ()
    last_row = ()
    for row in cur.execute(stmt, (start_time, end_time)):
        last_row = (gmt_to_local(row[0]), row[1])
        if len(rows) == 0 or rows[-1][1] != row[1]:
            if last_tuple != ():
                rows.append(last_tuple)
                last_tuple = ()
            rows.append((gmt_to_local(row[0]), row[1]))
        else:
            last_tuple = (gmt_to_local(row[0]), row[1])
    if rows[-1][0] != last_row[0]:
        rows.append((last_row[0], last_row[1]))
    # print("dataset length: {}".format(len(data_set)))
    return rows


def gmt_to_local(gmt_time):
    return gmt_time - (60 * 60 * 6)


def make_line_chart(data, filename=None):
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
                                    style=DarkGreenBlueStyle,
                                    config=config)
    line_chart.add('Temp', data, show_dots=True)
    if filename is not None:
        line_chart.render_to_file(filename)
    else:
        return line_chart.render()


if __name__ == '__main__':
    data = load_data()
    print(data)
    make_line_chart(data, filename='temp2.svg')
