import time
import network
import dht
from machine import Pin
from umqtt.simple import MQTTClient

# Wi-Fi credentials
SSID = "Galaxy A52 5G665E"
PASSWORD = "fmnn7937"

# ThingsBoard server details
THINGSBOARD_SERVER = "demo.thingsboard.io"  # Replace with your ThingsBoard server address
ACCESS_TOKEN = "oyFqe987yyKtLYmYTmza"  # Replace with your device's access token

# GPIO pin assignments
DHT_SENSOR_PIN = 13  # Pin connected to the DHT sensor

# Initialize the DHT sensor
dht_sensor = dht.DHT11(Pin(DHT_SENSOR_PIN))

# Connect to Wi-Fi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)

    print("Connected to Wi-Fi", wlan.ifconfig())

# Publish sensor readings to ThingsBoard
def publish_to_thingsboard(client):
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        # Prepare telemetry payload
        payload = '{"temperature": %d, "humidity": %d}' % (temperature, humidity)
        print(f"Publishing to ThingsBoard: {payload}")

        # Publish to the telemetry topic
        client.publish("v1/devices/me/telemetry", payload)

    except Exception as e:
        print("Error reading sensor or publishing data:", e)

# Main client code
def main():
    connect_to_wifi()

    # Connect to ThingsBoard MQTT broker
    client = MQTTClient("client_id", THINGSBOARD_SERVER, user=ACCESS_TOKEN, password="")
    try:
        client.connect()
        print("Connected to ThingsBoard")

        while True:
            publish_to_thingsboard(client)
            time.sleep(5)  # Wait 5 seconds before sending the next reading

    except Exception as e:
        print("Connection error:", e)

    finally:
        client.disconnect()
        print("Disconnected from ThingsBoard")

if __name__ == "__main__":
    main()
