import os
import time
import picamera
import telepot

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram Bot API token
TELEGRAM_BOT_TOKEN = '6042159900:AAFFx5fpvbbgR1eYfTjgW7DRxqn0b9VzA5A'

# Replace 'YOUR_CHAT_ID' with your actual Telegram chat ID
TELEGRAM_CHAT_ID = '6393037362'

# Initialize the Telegram Bot
bot = telepot.Bot(TELEGRAM_BOT_TOKEN)

def send_photo(photo_path):
    with open(photo_path, 'rb') as photo:
        bot.sendPhoto(TELEGRAM_CHAT_ID, photo)

def capture_and_send_photo():
    with picamera.PiCamera() as camera:
        # Adjust camera settings if needed
        camera.resolution = (1024, 768)
        camera.start_preview()
        time.sleep(2)  # Allow the camera to adjust to lighting conditions
        photo_path = '/tmp/captured_photo.jpg'
        camera.capture(photo_path)
        camera.stop_preview()
    return photo_path

if __name__ == '__main__':
    try:
        photo_path = capture_and_send_photo()
        send_photo(photo_path)
    except Exception as e:
        print(f"An error occurred: {e}")
