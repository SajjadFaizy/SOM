from paho.mqtt import client as mqtt_client
import re

# --------------------------------------------------------- Configuration

topic = "Gruppe2"  # Topic to subscribe
client_id = "subscriber"  # Unique client ID

broker = '141.22.36.124'    # Broker's IP address
port = 1883             # 1883: Standard NOT encrypted MQTT port
                        # 8883: Standard ENCRYPTED MQTT port

# Store last 60s of data
temperature_data = []

# --------------------------------------------------------- Functions

def connect_mqtt():
    client = mqtt_client.Client(
        client_id = client_id,
        protocol = mqtt_client.MQTTv311
    )
    client.connect(broker, port)
    return client


def update_temperature_data(client, userdata, message):
    """
    Handles incoming MQTT messages and processes the data.
    This is a standard >>> callback function <<< in Paho MQTT, 
    automatically triggered whenever a subscribed topic receives a message.

    Args:
        client (mqtt.Client): The MQTT client instance that received the message.
        userdata (any): User-defined data passed to the callback (not used here).
        message (mqtt.MQTTMessage): The message object containing topic, payload, etc.

    Returns:
        None
    """

    global temperature_data

    # Extract Data from MQTT ----------------------------------------------

    # Decode message payload
    payload = message.payload.decode()

    # Use regular expression to extract numeric temperature value
    match = re.search(r"Temp:\s*([\d.]+)", payload)
    
    if match:
        temperature = float(match.group(1)) # Convert temperature to float
        print(f"Temperature: {temperature} °C")
    else:
        print("Could not extract temperature from message:", payload)

    # ---------------------------------------------------------------------

    # Store the last 60 seconds of data
    if len(temperature_data) >= 60:
        temperature_data.pop(0) # Remove oldest value
    temperature_data.append(temperature)

    print("Global:", temperature_data)

def start_subscriber():
    client = connect_mqtt()

    client.subscribe(topic)  # Subscribe to the topic
    client.message_callback_add(topic, update_temperature_data)

    client.loop_forever()  # Paho library function to keep listening topic