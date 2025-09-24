from paho.mqtt import client as mqtt_client
import time
import board 
import adafruit_dht

MQTT_PORT = 1883 # Std MQTT-Port
MQTT_ADDRESS = "141.22.36.124" # IP-Adresse Broker - Andere: 127.0.0.1
MQTT_CLIENT_NAME = "Test_PiSubbi2" # Client name
MQTT_TOPIC = "Gruppe2" # MQTT-Topic
TICK_RATE_HZ = 2 # Refresh rate
TICK_RATE = 1/TICK_RATE_HZ # Berechnung Zeit zwischen Aktualisierungen

dhtDevice = adafruit_dht.DHT11(board.D23) # Für die Kombination mit dem DHT11/22-Sensor

# board.D23 ist der Pin 16 (GPIO 23) des Raspberry Pi
# konfiguriert den Sensor auf GPIO 23(Pin 16) des Raspberry Pi

#temperature_c = 25.0  # Simulierter Temperaturwert
#humidity = 50.0       # Simulierter Feuchtigkeitswert

# Liste für die Nachrichten
message_queue = []

# Funktion die beim eintreffen einer Nachricht diese in eine Liste packt
def on_message(client, userdata, msg): # Callback Funktion
    message=msg.payload.decode()
    message_queue.append(message)

# Verbinden mit MQTT
client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1,MQTT_CLIENT_NAME)
client.connect(MQTT_ADDRESS,MQTT_PORT) #Verbindung zum Broker

# Subscribe zum Thema und Funktion "on_message" hinzufügen
client.subscribe(MQTT_TOPIC) #Abonnieren des Topics
client.on_message = on_message

# Starten die Netzwerkskommunikation für den MQTT-Client im Hintergrund
client.loop_start()

# Ständig ausführen
while (True): # Ruft regelmäßig Nachrichten aus der Liste ab, speichert sie und gibt sie aus

    try:
        # Drucken der Werte über die serielle Schnittstelle
        temperature_c = dhtDevice.temperature # Temperatur in Celsius wird in der Variable temperature_c gespeichert
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity # Luftfeuchtigkeit wird in der Variable humidity gespeichert
        if temperature_c is not None and humidity is not None:
            message = f"Temp: {temperature_c:.1f} C, Humidity: {humidity}%"
            print (message)
            
            client.publish(MQTT_TOPIC, message)
        else:
            print("Failed to read sensor data.")

    except RuntimeError as error: # Falls der Sensor nicht gelesen werden kann
        # Fehler kommt oft vor, DHT's sind schwer zu lesen - einfach weitermachen
        print("Sensorfehler:", error.args[0])
        time.sleep(2.0)
        continue

    except Exception as error:
        dhtDevice.exit() # Sorgt dafür, dass der Sensor sauber beendet wird
        raise error
    
    time.sleep(2.0) # Wartezeit zwischen Messungen
            
    last_value = ""
    value_queue = []

    #Kurz warten
    time.sleep(TICK_RATE)

    # Wenn es weitere Nachrichten gibt...
    while len(message_queue) > 0:
        # ...dann kopiere diese von der Empfangsliste in die Anzeige-Liste
        last_value = message_queue.pop()
        value_queue.append(last_value)
        print(last_value) 