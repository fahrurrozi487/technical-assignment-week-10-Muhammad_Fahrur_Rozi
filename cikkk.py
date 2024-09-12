import pyrebase
import random
import time
import Adafruit_DHT
import datetime
import requests
import RPi.GPIO as gpio

"""relay1 =20
relay2 =19
relay3=26
buzzer =21
gpio.setmode(gpio.BCM)
gpio.setup(relay1, gpio.OUT)
gpio.setup(relay2, gpio.OUT)
gpio.setup(relay3, gpio.OUT)
gpio.setup(buzzer, gpio.OUT)
gpio.output(relay1, False)
gpio.output(relay2, False)
gpio.output(relay3, False)
gpio.output(buzzer, False)
sensor = Adafruit_DHT.DHT11
pin = 4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)"""
pin=4
sensor = Adafruit_DHT.DHT11
config = {
  "apiKey": "AIzaSyDOAexY2dAs4tuZzMaPw327eXCdOFHcK0U",
  "authDomain": "scawmon.firebaseapp.com",
  "databaseURL": "https://scawmon-default-rtdb.firebaseio.com",
  "projectId": "scawmon",
  "storageBucket": "scawmon.appspot.com",
  "messagingSenderId": "364445818829",
  "appId": "1:364445818829:web:d085c6979eab9e87b8ae84",
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
database = firebase.database()

#def baca_ph():
def baca_kelembaban():
    humidity = Adafruit_DHT.read_retry(sensor, pin)
    global pompa, total1, count1, rata1, ket1
    pompa=0
    count1=0
    total1=0
    ket1=""
    if humidity > 50:
        #gpio.output(relay1, True)
        pompa=1
        ket1="Terlalu Lembab"
    elif humidity >50 and humidity <=40:
        #gpio.output(relay1, True)
        time.sleep(10)
        #gpio.output(relay1, False)
        pompa=0
        ket1="Normal"
    else:
        #gpio.output(relay1, False)
        pompa=0
        ket1="Terlalu Kering"
    count1+=1
    total1+=humidity
    rata1=total1/count1
    return humidity
        
def baca_suhu():
    temperature = Adafruit_DHT.read_retry(sensor, pin)
    global kipas, count2, total2, rata2, ket2
    kipas=0
    count2=0
    total2=0
    ket2=""
    if temperature >= 30:
        #gpio.output(relay2, True)
        kipas=1
        ket2= "Terlalu Panas"
    elif temperature >30 and temperature <=29:
        #gpio.output(relay1, True)
        time.sleep(10)
        #gpio.output(relay1, False)
        kipas=0
        ket2= "Hangat"
    else:
        #gpio.output(relay2, False)
        kipas=0
        ket2= "Dingin"
    count2+=1
    total2+=temperature
    rata2=total2/count2
    return temperature
              
while True:
    a=baca_kelembaban()
    b=baca_suhu()
    print(a)
    print(b)
    print (ket1)
    print (ket2)

    """database.child("SCAWMON")
    data = {"suhu": temperature,
        "kelembaban":humidity,
        "pH":pH,
        "buzzer":buzz,
        "kipas":kipas,
        "pompa":pompa,
        "pengaduk":pengaduk,
        "rata1":rata1,
        "rata2":rata2,
        "rata3":rata3,
        "ket1":ket1,
        "ket2":ket2,
        "ket3":ket3
        }
    database.set(data)"""
    time.sleep(3)