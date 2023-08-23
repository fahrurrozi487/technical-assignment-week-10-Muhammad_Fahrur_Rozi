import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

# Set the GPIO mode and pin number
GPIO.setmode(GPIO.BCM)
PIR_PIN = 17

# Initialize the PIR sensor pin
GPIO.setup(PIR_PIN, GPIO.IN)

# MQTT settings
MQTT_BROKER = "industrial.api.ubidots.com"
MQTT_PORT = 1883
MQTT_USERNAME = "YOUR_UBIDOTS_TOKEN"
DEVICE_LABEL = "your-device-label"
VARIABLE_LABEL = "your-variable-label"

client = mqtt.Client(client_id="")
client.username_pw_set(username=MQTT_USERNAME, password="")

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with code " + str(rc))
    client.subscribe("/v1.6/devices/" + DEVICE_LABEL)

client.on_connect = on_connect

def send_data_to_ubidots(value):
    payload = f'{{"{VARIABLE_LABEL}": {value}}}'
    topic = "/v1.6/devices/" + DEVICE_LABEL
    client.publish(topic, payload=payload)
    print("Data sent to Ubidots:", payload)

try:
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_start()

    print("PIR Module Test (CTRL+C to exit)")
    time.sleep(2)
    print("Ready")

    while True:
        if GPIO.input(PIR_PIN):
            print("Motion detected!")
            send_data_to_ubidots(1)  # Sending 1 to indicate motion
        else:
            print("No motion")
            send_data_to_ubidots(0)  # Sending 0 when no motion
        time.sleep(1)

except KeyboardInterrupt:
    print("Exit")
    client.disconnect()
    client.loop_stop()
    GPIO.cleanup()
