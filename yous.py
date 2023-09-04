import datetime  # Importing the datetime library
import telepot   # Importing the telepot library
from telepot.loop import MessageLoop    # Library function to communicate with telegram bot
import RPi.GPIO as GPIO     # Importing the GPIO library to use the GPIO pins of Raspberry pi
import time    # Importing the time library to provide the delays in program
from picamera2 import Picamera2
import os
import json
import random
import paho.mqtt.client as mqtt
from roboflow import Roboflow
import cv2
rf = Roboflow(api_key="wjIbFI5jUqWpxDPE9U8j")
project = rf.workspace().project("pendeteksi-tikus-rumah-xqpyq")
model = project.version(1).model

UBIDOTS_TOKEN = "BBFF-eFMbNcrOkgjt0ITr7RPNXYU71mzBy1"
DEVICE_LABEL = "lokaping"

MQTT_BROKER = "industrial.api.ubidots.com"
MQTT_PORT = 1883
MQTT_USERNAME = UBIDOTS_TOKEN
MQTT_PASSWORD = ""

# Callback when the MQTT client connects
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/v1.6/devices/" + DEVICE_LABEL)
    
path = path=os.getenv("HOME")
trig_pin = 21
echo_pin = 20
trig_pin2 = 16
echo_pin2 = 26
trig_pin3 = 19
echo_pin3 = 13
relay = 14
buzzer = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)
GPIO.setup(trig_pin2, GPIO.OUT)
GPIO.setup(echo_pin2, GPIO.IN)
GPIO.setup(trig_pin3, GPIO.OUT)
GPIO.setup(echo_pin3, GPIO.IN)
GPIO.setup(relay, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
now = datetime.datetime.now()
client = mqtt.Client(client_id=DEVICE_LABEL)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()
def ultrasonik():
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin, GPIO.LOW)
    while GPIO.input(echo_pin) == GPIO.LOW:
        pulse_start_time = time.time()

    while GPIO.input(echo_pin) == GPIO.HIGH:
        pulse_end_time = time.time()
#
    pulse_duration = pulse_end_time-pulse_start_time

    distance_cm = (pulse_duration * 34300) / 2
    distance_cm = round(distance_cm, 2)
    #
    hasil_sensor = distance_cm
    print(distance_cm)
    #print("ultrasonik 1", distance_cm)
    return hasil_sensor

def ultrasonik2():
    GPIO.output(trig_pin2, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin2, GPIO.LOW)

    while GPIO.input(echo_pin2) == GPIO.LOW:
        pulse_start_time = time.time()

    while GPIO.input(echo_pin2) == GPIO.HIGH:
        pulse_end_time = time.time()
#
    pulse_duration = pulse_end_time-pulse_start_time

    distance_cm = (pulse_duration * 34300) / 2
    distance_cm = round(distance_cm, 2)
    #
    hasil_sensor = distance_cm
    print(distance_cm)
    #print("ultrasonik 2",distance_cm)
    return hasil_sensor

def ultrasonik3():
    GPIO.output(trig_pin3, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin3, GPIO.LOW)

    while GPIO.input(echo_pin3) == GPIO.LOW:
        pulse_start_time = time.time()

    while GPIO.input(echo_pin3) == GPIO.HIGH:
        pulse_end_time = time.time()
#
    pulse_duration = pulse_end_time-pulse_start_time

    distance_cm = (pulse_duration * 34300) / 2
    distance_cm = round(distance_cm, 2)
    #
    hasil_sensor = distance_cm
    print(distance_cm)
    #print("ultrasonik 3",distance_cm)
    return hasil_sensor
def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print ('Received:')
    print(command)

    if command == '/hi':
        bot.sendMessage (chat_id, str("Hi! MakerPro"))
    elif command == '/time':
        bot.sendMessage(chat_id, str("Time: ") + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second))
    elif command == '/date':
        bot.sendMessage(chat_id, str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))
    elif command == '/RELAYON':
        bot.sendMessage(chat_id, str("Relay Nyala"))
        GPIO.output(relay, GPIO.LOW)
    elif command == '/RELAYOFF':
        bot.sendMessage(chat_id, str("Relay Mati"))
        GPIO.output(relay, GPIO.HIGH)
    elif command == '/BUZZERON':
        bot.sendMessage(chat_id, str("Buzzer Nyala"))
        GPIO.output(buzzer, GPIO.HIGH)
    elif command == '/BUZZEROFF':
        bot.sendMessage(chat_id, str("Buzzer Mati"))
        GPIO.output(buzzer, GPIO.LOW)

# Insert your telegram token below
bot = telepot.Bot('6042159900:AAFFx5fpvbbgR1eYfTjgW7DRxqn0b9VzA5A')
print (bot.getMe())

# Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
MessageLoop(bot, handle).run_as_thread()
print ('Listening....')
"""def get_camera():
    kamera=Picamera2()
    kamera.preview_configuration.main.size=(1920, 1080)
    kamera.preview_configuration.main.format="RGB888"
    kamera.preview_configuration.align()
    kamera.configure("preview")
    kamera.start()
    time.sleep(1)
    kamera.capture_file('pic.jpg')
    metadata = kamera.capture_file('pic.jpg')
    kamera.close()
    model.predict('pic.jpg', confidence=40, overlap=30).save("prediction.jpg")
    return metadata"""
def get_camera():
    cap = cv2.VideoCapture(0)  # 0 represents the default camera (usually the USB webcam)
    ret, frame = cap.read()
    cv2.imwrite("pic.jpg", frame)
    cap.release()
    model.predict('pic.jpg', confidence=40, overlap=30).save("prediction.jpg")
    metadata=cv2.imwrite("pic.jpg", frame)
    return metadata
count_tikus = 0
while 1:
    ultrasonic_value = ultrasonik()
    ultrasonic_value2 = ultrasonik2()
    ultrasonic_value3 = ultrasonik3()
    payload = {"ultrasonik1": ultrasonic_value,
               "ultrasonik2": ultrasonic_value2,
               "ultrasonik3": ultrasonic_value3,
               "tikus": count_tikus,
               }
    client.publish("/v1.6/devices/" + DEVICE_LABEL, json.dumps(payload), qos=0)
    #time.sleep(1)
    if ultrasonic_value <23 :
        metadata = get_camera()
        counter_sensor = 0
        print(metadata)
        chat_id = 6393037362
        bot.sendPhoto(chat_id, open(path + '/Downloads/prediction.jpg', 'rb'))
        count_tikus = count_tikus + 1
        bot.sendMessage(chat_id, str(f"Sensor 1 Mendeteksi, Tikus Masuk Perangkap {count_tikus}"))
    if ultrasonic_value2 <23 :
        metadata = get_camera()
        print(metadata)
        chat_id = 6393037362
        bot.sendPhoto(chat_id, open(path + '/Downloads/prediction.jpg', 'rb'))
        count_tikus = count_tikus + 1
        bot.sendMessage(chat_id, str(f"Sensor 2 Mendeteksi, Tikus Masuk Perangkap: {count_tikus}"))
    if ultrasonic_value3 <23 :
        metadata = get_camera()
        print(metadata)
        chat_id = 6393037362
        bot.sendPhoto(chat_id, open(path + '/Downloads/prediction.jpg', 'rb'))
        count_tikus = count_tikus + 1
        bot.sendMessage(chat_id, str(f"Sensor 3 Mendeteksi, Tikus Dalam Perangkap: {count_tikus}"))
    time.sleep(1)