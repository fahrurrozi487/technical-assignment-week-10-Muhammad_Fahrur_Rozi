import RPi.GPIO as GPIO
import time
import datetime
import pandas as pd
import random
from lcd import drivers
import Adafruit_DHT
import pyrebase
import spidev

# Fungsi untuk menginisialisasi SPI

servo = 21
buzzerr = 26
pompaa=20
kipass=16
pengadukk=19
dht=13
echo=6
trigger=12
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(servo, GPIO.OUT)
GPIO.setup(buzzerr, GPIO.OUT)
GPIO.setup(pompaa, GPIO.OUT)
GPIO.setup(kipass, GPIO.OUT)
GPIO.setup(pengadukk, GPIO.OUT)
GPIO.setup(dht, GPIO.IN)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(trigger, GPIO.OUT)
GPIO.output(buzzerr, False)
GPIO.output(pompaa, False)
GPIO.output(kipass, False)
GPIO.output(pengadukk, False)
pwm = GPIO.PWM(servo, 50)
pwm.start(0)
DHT_SENSOR = Adafruit_DHT.DHT11
#humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, dht)

display = drivers.Lcd()
firebase_config = {
  "apiKey": "AIzaSyDOAexY2dAs4tuZzMaPw327eXCdOFHcK0U",
  "authDomain": "scawmon.firebaseapp.com",
  "databaseURL": "https://scawmon-default-rtdb.firebaseio.com",
  "projectId": "scawmon",
  "storageBucket": "scawmon.appspot.com",
  "messagingSenderId": "364445818829",
  "appId": "1:364445818829:web:d085c6979eab9e87b8ae84",
  "measurementId": "G-PG5399LPX9"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

def init_spi():
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1350000
    return spi

# Fungsi untuk membaca data dari channel MCP3008
def read_channel(spi, channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Fungsi untuk mengkonversi nilai ADC ke voltase
def convert_volts(adc_value, vref=3.3):
    return (adc_value * vref) / 1024.0

# Fungsi untuk menghitung pH dari voltase
def calculate_ph(voltage):
    # Slope (m) dan Intercept (b) dari kalibrasi
    m = 1.07
    b = 3.79
    # Menghitung pH berdasarkan voltase
    ph = m * voltage + b
    return ph

def read_dht11():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, dht)
    if humidity is not None and temperature is not None:
        pompa_on(humidity)
        kipas_on(temperature)
        ket_suhu(temperature)
        return temperature, humidity

    else:
        return None, None
    #temperature = random.randint(1,100)
    #humidity = random.randint(1,100)
    #return  temperature, humidity

def read_ph():
    spi = init_spi()
    ph_channel = 0  # Channel MCP3008 yang terhubung ke sensor pH
            # Membaca nilai ADC dari channel sensor pH
    adc_value = read_channel(spi, ph_channel)
            # Mengkonversi nilai ADC ke voltase
    voltage = convert_volts(adc_value)
            # Menghitung pH dari voltase
    ph_value = calculate_ph(voltage)+ 2.2
    keterangan_ph(ph_value)
    pengaduk_on(ph_value)
            # Menampilkan nilai voltase dan pH
    print(f"Voltage: {voltage:.2f}V, pH: {ph_value:.2f}")
    
    return ph_value

def read_sensor():
    temp, humidity = read_dht11()
    ph = read_ph()
    display.lcd_display_string(f"H:{str(humidity)} T:{str(temp)}", 1)
    display.lcd_display_string(f"P:{ph:.2f}           ",2)
    return {'temp': temp, 'humidity': humidity, 'ph': ph}

def calculate_average(data, resample_rule):
    df = pd.DataFrame(data, columns=['timestamp', 'temp', 'humidity', 'ph'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    return df.resample(resample_rule).mean()

def upload_to_firebase(path, data):
    db.child(path).set(data)

def pompa_on(yak):
    global pompa, keterangan_kelembaban
    if yak > 50:
        pompa=0
        keterangan_kelembaban=2
        GPIO.output(pompaa, False)
    elif yak>=40 and yak<50:
        pompa=0
        keterangan_kelembaban=1
        GPIO.output(pompaa, False) 
    else:
        pompa=1
        keterangan_kelembaban=0
        GPIO.output(pompaa, True)

def ket_suhu(pak):
    global keterangan_suhu
    if pak>=30:
        keterangan_suhu=2
    elif pak<30 and pak>=29:
        keterangan_suhu=1
    else:
        keterangan_suhu=0
def keterangan_ph(ph):
    global ket_ph
    if ph>=7.5:
        ket_ph=2
    elif ph>6.5 and ph<7.5:
        ket_ph=1
    else:
        ket_ph=0      
def kipas_on(yosh):
    global kipas, keterangan_suhu
    if yosh >=30:
        kipas=1
        keterangan_suhu=1
        GPIO.output(kipass, True)
    else:
        keterangan_suhu=0
        kipas=0
        GPIO.output(kipass, False)
                 
def pengaduk_on(val):
    global buzzer, pengaduk
    if val>6:
        buzzer=1
        pengaduk=1
        pwm.ChangeDutyCycle(12)
        time.sleep(1)
        GPIO.output(buzzerr, True)
        pwm.ChangeDutyCycle(2)
    elif val>4 and val<6:
        buzzer=0
        pengaduk=0
        pwm.ChangeDutyCycle(2)
        GPIO.output(buzzerr, False)
    else:
        buzzer=0
        pengaduk=0
        pwm.ChangeDutyCycle(2)
        GPIO.output(buzzerr, False)

def main():
    data_list = []
    total_sum = {'temp': 0, 'humidity': 0, 'ph': 0}
    total_count = {'temp': 0, 'humidity': 0, 'ph': 0}

    start_time = datetime.datetime.now()
    interval = {
        'minute': 60,
        'hour': 3600,
        'day': 86400,
        'month': 2592000
    }

    try:
        while True:
            sensor_data = read_sensor()
            timestamp = datetime.datetime.now()
            data_list.append([timestamp, sensor_data['temp'], sensor_data['humidity'], sensor_data['ph']])
            
            # Kirim data sensor langsung ke Firebase
            if sensor_data['temp'] is not None:
                db.child('data_sensor/suhu/').set({'suhu': sensor_data['temp']})
            if sensor_data['humidity'] is not None:
                db.child('data_sensor/kelembaban/').set({'kelembaban': sensor_data['humidity']})
            if sensor_data['ph'] is not None:
                db.child('data_sensor/ph/').set({'ph': sensor_data['ph']})
            
            db.child('data_keterangan/').set({
                'keterangan_suhu':keterangan_suhu,
                'keterangan_kelembaban':keterangan_kelembaban,
                'keterangan_ph':ket_ph
            })
            
            db.child('data_kontrol/').set({
                'buzzer': buzzer,
                'pompa': pompa,
                'kipas': kipas,
                'pengaduk': pengaduk
            })
            
            # Update total sums and counts
            for key in total_sum.keys():
                value = sensor_data[key]
                if value is not None:
                    total_sum[key] += value
                    total_count[key] += 1

            avg_overall = {k: (total_sum[k] / total_count[k] if total_count[k] > 0 else 0) for k in total_sum}
            #print(f"Rata-rata keseluruhan real-time - Suhu: {avg_overall['temp']:.2f} C, Kelembapan: {avg_overall['humidity']:.2f} %, pH: {avg_overall['ph']:.2f}")

            current_time = datetime.datetime.now()
            elapsed_time = (current_time - start_time).total_seconds()

            if elapsed_time >= interval['minute']:
                avg_minutely = calculate_average(data_list, 'min').tail(1)
                avg_minutely_values = avg_minutely.iloc[0].to_dict()
                upload_to_firebase('data_rata_menit/', avg_minutely_values)
                #print(f"Rata-rata untuk menit terakhir:\n{avg_minutely}")
                start_time = current_time
                data_list = [d for d in data_list if (current_time - d[0]).total_seconds() < interval['minute']]

            if elapsed_time >= interval['hour']:
                avg_hourly = calculate_average(data_list, 'H').tail(1)
                avg_hourly_values = avg_hourly.iloc[0].to_dict()
                upload_to_firebase('data_rata_jam/', avg_hourly_values)
                #print(f"Rata-rata untuk jam terakhir:\n{avg_hourly}")
                start_time = current_time
                data_list = [d for d in data_list if (current_time - d[0]).total_seconds() < interval['hour']]

            if elapsed_time >= interval['day']:
                avg_daily = calculate_average(data_list, 'D').tail(1)
                avg_daily_values = avg_daily.iloc[0].to_dict()
                upload_to_firebase('data_rata_hari/', avg_daily_values)
                #print(f"Rata-rata untuk hari terakhir:\n{avg_daily}")
                start_time = current_time
                data_list = [d for d in data_list if (current_time - d[0]).total_seconds() < interval['day']]

            if elapsed_time >= interval['month']:
                avg_monthly = calculate_average(data_list, 'M').tail(1)
                avg_monthly_values = avg_monthly.iloc[0].to_dict()
                upload_to_firebase('data_rata_bulan/', avg_monthly_values)
                #print(f"Rata-rata untuk bulan terakhir:\n{avg_monthly}")
                start_time = current_time
                data_list = [d for d in data_list if (current_time - d[0]).total_seconds() < interval['month']]

            overall_data = {
                'temp': avg_overall['temp'],
                'humidity': avg_overall['humidity'],
                'ph': avg_overall['ph']
            }
            upload_to_firebase('data_rata/', overall_data)

            time.sleep(1)

    except KeyboardInterrupt:
        print("Program dihentikan oleh pengguna")
        display.lcd_clear()

if __name__ == "__main__":
    main()