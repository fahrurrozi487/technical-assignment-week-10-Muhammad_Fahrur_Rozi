import telepot
#import RPi.GPIO as GPIO
import time

# Define your Telegram bot's API token
TELEGRAM_TOKEN = '6042159900:AAFFx5fpvbbgR1eYfTjgW7DRxqn0b9VzA5A'

# Define the servo GPIO pin
SERVO_PIN = 17  # Change this to your servo's GPIO pin

# Initialize the Telegram bot
bot = telepot.Bot(TELEGRAM_TOKEN)

# Initialize the GPIO library
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(SERVO_PIN, GPIO.OUT)

# Create a function to control the servo
def set_servo_angle(awngle):
    pulse_width = (awngle * 10) + 500
    GPIO.output(SERVO_PIN, True)
    time.sleep(pulse_width / 1000000.0)
    GPIO.output(SERVO_PIN, False)

# Handle Telegram messages
def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        command = msg['text']
        if '/move' in command:
            try:
                angle = int(command.split(' ')[1])
                if 0 <= angle <= 180:
                    #set_servo_angle(angle)
                    bot.sendMessage(chat_id, f'servo bergerak ke arah {angle} derajat.')
                else:
                    bot.sendMessage(chat_id, 'error. tolong masukkan nilai antara 0 - 180.')
            except Exception as e:
                bot.sendMessage(chat_id, 'Invalid command format. Use /move [angle].')

# Set up the message handler
bot.message_loop(handle_message)

# Keep the program running
try:
    while True:
        time.sleep(10)
# Clean up when the program is stopped
except KeyboardInterrupt:
    GPIO.cleanup()
