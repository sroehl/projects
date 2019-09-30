import paho.mqtt.client as mqtt
import json
import time
import sqlite3 as lite


def insertToDB(location, device, vals):
  epoch = int(time.time())
  for key in vals:
    stmt = 'insert into sensor VALUES ("{}", "{}", "{}", {}, {})'.format(location, device, key, epoch, vals[key])
    print(stmt)
    c.execute(stmt)
  conn.commit()

def on_connect(client, userdata, flags, rc):
  client.subscribe("/sensors/#")

def on_message(client, userdata, msg):
  print("topic: {}".format(msg.topic))
  print("{}".format(str(msg.payload)))
  data = str(msg.payload)
  location = msg.topic.split('/')[-2]
  device = msg.topic.split('/')[-1]
  vals = json.loads(msg.payload.decode("utf-8"))
  insertToDB(location, device, vals)

# Set up database
conn = lite.connect('sensor.db')
c = conn.cursor()
c.execute('''create table if not exists sensor(location text, sensor text, name text, time integer, value real)''')


client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect

client.connect("192.168.0.109", 1883, 60)
client.loop_forever()
