"""

This script publishes fake test temperature data in the mqtt server.
This allows to test the data reception script and the GUI

"""

import time
import random
from paho.mqtt import client as mqtt_client

broker = 'localhost'  # Broker's IP-address
port = 1883 # Standard port for NOT encrypted MQTT-servers: 1883
            # Standard port for ENCRYPTED MQTT-servers: 8883
topic = "sensor/temperature"  # topic for data
client_id = "simulated-sensor"

# Connect to Broker
def connect_mqtt():
    client = mqtt_client.Client(
        client_id = client_id,
        protocol = mqtt_client.MQTTv311
    )
    client.connect(broker, port)
    return client

# Publish simulated data
def publish(client):
    while True:
        temperature = round(random.uniform(20.0, 30.0), 2)  # Simulate temperature meassures
        client.publish(topic, f"{temperature}")
        print(f"Published: {temperature}°C to topic {topic}")
        time.sleep(4)  # Publish interval (2s)

client = connect_mqtt()
publish(client)