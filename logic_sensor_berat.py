import random
import time
import paho.mqtt.client as mqtt
import json
import os
import telepot
from telepot.loop import MessageLoop
import datetime
import socket
import time

# Set up GPIO

def check_network():
    try:
        # Try to connect to Google's DNS server
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return 1
    except OSError:
        return 0

now = datetime.datetime.now()
chat_id = 6393037362
path = path=os.getenv("HOME")
tikus_besar = 0
tikus_kecil = 0
sensor1= 0
sensor2= 0
sensor3=0

def handle(msg):
    command = msg['text']

    print ('Received:')
    print(command)

    if command == '/hi':
        bot.sendMessage (chat_id, str("Hi! MakerPro"))
    elif command == '/time':
        bot.sendMessage(chat_id, str("Time: ") + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second))
    elif command == '/date':
        bot.sendMessage(chat_id, str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))
    elif command == '/quotes':
        bot.sendMessage (chat_id, str(""))
    elif command == '/photo':
        bot.sendPhoto(chat_id, photo=open('gunung.jpg', 'rb'))
    elif command == '/image':
        bot.sendMessage(chat_id, str("gambar tidak dapat terkirim"))
    elif command == "/CEK":
        bot.sendMessage(chat_id, str(f"tikus dalam perangkap{jumlah_tikus}"))
UBIDOTS_TOKEN = "BBFF-Sg22jjSNyKzxWF0FgEnny9zim4rxP4"
DEVICE_LABEL = "raspi_tim12"

MQTT_BROKER = "industrial.api.ubidots.com"
MQTT_PORT = 1883
MQTT_USERNAME = UBIDOTS_TOKEN
MQTT_PASSWORD = ""

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/v1.6/devices/" + DEVICE_LABEL)

client = mqtt.Client(client_id=DEVICE_LABEL)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

def sensor_berat():
    berat=random.randint(0,100)
    return berat
def ultrasonic1():
    y = random.randint(0,100)
    return y
def ultrasonic2():
    y = random.randint(0,100)
    return y
def ultrasonic3():
    y = random.randint(0,100)
    return y

bot = telepot.Bot('6435430348:AAEvjhuMP9sfhqrc-C-qCyT-0j_ZFzIoM7o')
print (bot.getMe())

MessageLoop(bot, handle).run_as_thread()
print ('Listening....')
while True:
    value1 = sensor_berat()
    value2 = ultrasonic1()
    value3 = ultrasonic2()
    value4 = ultrasonic3()
    hoi = check_network()
    if value2 >=50:
        sensor1 = sensor1 + 1
        if value2 >=50:
            tikus_besar = tikus_besar + 1
        elif value2 <=50:
            tikus_kecil = tikus_kecil + 1
        print("Sensor 1", sensor1)
        time.sleep(1)        
    if value3 >=50:
        sensor2 = sensor2 + 1
        if value2 >=50:
            tikus_besar = tikus_besar + 1
        elif value2 <=50:
            tikus_kecil = tikus_kecil + 1
        print("Sensor 2", sensor2)
        time.sleep(1)
    if value4 >=50:
        sensor3 = sensor3 + 1
        if value2 >=50:
            tikus_besar = tikus_besar + 1
        elif value2 <=50:
            tikus_kecil = tikus_kecil + 1
        print("Sensor 3", sensor3)
        time.sleep(1)
    jumlah_tikus = sensor1 + sensor2 + sensor3
    print(jumlah_tikus)
    payload = {"tikus_kecil": tikus_kecil,
               "tikus_besar": tikus_besar,
               "jumlah_tikus": jumlah_tikus,
               "sensor1": sensor1,
               "sensor2": sensor2,
               "sensor3": sensor3,
               "nopl": hoi,
               }
    client.publish("/v1.6/devices/" + DEVICE_LABEL, json.dumps(payload), qos=0)
    time.sleep(1)