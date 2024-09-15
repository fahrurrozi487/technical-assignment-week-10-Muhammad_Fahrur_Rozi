import RPi.GPIO as GPIO
import time
import Adafruit_DHT
from lcd import drivers
import random
display = drivers.Lcd()
#wm.ChangeDutyCycle(7.5)
DHT_SENSOR = Adafruit_DHT.DHT11
servo = 21
buzzer = 26
pompa=20
kipas=16
pengaduk=19
dht=13
echo=6
trigger=12
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(pompa, GPIO.OUT)
GPIO.setup(kipas, GPIO.OUT)
GPIO.setup(pengaduk, GPIO.OUT)
GPIO.setup(dht, GPIO.IN)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(trigger, GPIO.OUT)
GPIO.output(buzzer, False)
GPIO.output(pompa, False)
GPIO.output(kipas, False)
GPIO.output(pengaduk, False)
pwm = GPIO.PWM(servo, 50)
pwm.start(0)
humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, dht)

def ultrasonik2():
    GPIO.output(trigger, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger, GPIO.LOW)

    while GPIO.input(echo) == GPIO.LOW:
        pulse_start_time = time.time()

    while GPIO.input(echo) == GPIO.HIGH:
        pulse_end_time = time.time()
#
    pulse_duration = pulse_end_time-pulse_start_time

    distance_cm = (pulse_duration * 34300) / 2
    distance_cm = round(distance_cm, 2)
    #
    hasil_sensor = distance_cm
    #print(distance_cm)
    return hasil_sensor

def pompa_on():
    if humidity >= 50:
        GPIO.output(pompa, True)
    else:
        GPIO.output(pompa, False)
        
def kipas_on():
    if temperature >=30:
        GPIO.output(kipas, True)
    else:
        GPIO.output(kipas, False)
                 
def pengaduk_on():
    if value_ph <10:
        pwm.ChangeDutyCycle(12)
        GPIO.output(buzzer, True)
        time.sleep(1)
        pwm.ChangeDutyCycle(2)
    else:
        pwm.ChangeDutyCycle(2)
        GPIO.output(buzzer, False)
try:
    while 1:
        kl=round(random.uniform(4.0, 10),2)
        display.lcd_display_string(f"H:{int(humidity)} T:{int(temperature)}", 1)
        value_ph = ultrasonik2()
        ultrasonik2()
        display.lcd_display_string(f"P:{kl}             ", 2)
        print(value_ph)
        pompa_on()
        kipas_on()
        pengaduk_on()
        time.sleep(1)
        print(kl)
except KeyboardInterrupt:
    display.lcd_clear()