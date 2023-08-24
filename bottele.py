from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import os
import requests
https://www.survivingwithandroid.com/telegram-bot-raspberry-pi-camera/
#tele
TOKEN = '6468751727:AAEtq8oSgf1VKX-0ahwPENaGhV-Ok45MfYA'
chat_id = 6393037362  #chat id pengguna
image_name = os.getcwd() + "/" + "img.jpg"
list_chat_id = ["6393037362"]#chat id pengguna

GPIO.setmode(GPIO.BCM)
GPIO.setup (23, GPIO.IN) #set pin sensor sentuh

def kirim_foto(nama_file):
    for chat_id in list_chat_id:
        image = open(nama_file,'rb')
        #print(chat_id)
        url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}'   #query  
        resp = requests.post(url, files={'photo':image})

        #res = requests.post(url , json=payload)
        print(resp.status_code)
        if int(resp.status_code) == 200:
            print("succes send image")

def tosen() :
    if GPIO.input(23) == 1 :#isipin
        print ("ada orang")
        pirsensor = 1
        AmbilGambar()

    elif GPIO.input (23) == 0 : #isipin
        print ("tidak ada orang")
        pirsensor = 0

    return tosen


def AmbilGambar () :
    print("Ambil Gambar!")
    nama_file = "img.jpg"
    #os.remove(nama_file)
    #print("File Removed")
    camera = PiCamera()
    time.sleep(2)
    camera.resolution = (1600,1600)
    camera.vflip = True
    camera.contrast = 10
    camera.capture(nama_file)
    kirim_foto(nama_file)
    print(nama_file)
    print("Image sent")
    camera.close()

while True :
    a = 'cheese.'
    c = 'espeak -ven+f4 -k5 -s150 --punct="<characters>" "%s" 2>>/dev/null' % a
    tosen()
    
    time.sleep(1)
