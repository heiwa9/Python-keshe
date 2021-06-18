import json
import random

from paho.mqtt import client as mqtt_client

import gui_mod

broker = 'xxxx'
port = xxxx
topic = "temp_hum"
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        gui_mod.mongo.save_data(json.loads(msg.payload))

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    # client.loop_start()


if __name__ == '__main__':
    run()
