import paho.mqtt.client as mqtt


ticks = 0
topic = "/sensors/outside/energy"


def on_connect(client, userdata, flags, rc):
    print("subscribing to {}".format(topic))
    client.subscribe(topic)


def on_message(client, userdata, msg):
    global ticks
    data = msg.payload.decode("utf-8")
    if data == 'tick':
        ticks += 1
        print("Ticks is {} power is {}kWh".format(ticks, ticks*0.1))

client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect

client.connect("192.168.0.109", 1883, 60)
client.loop_forever()