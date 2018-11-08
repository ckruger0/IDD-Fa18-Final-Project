#!/usr/bin/python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
from picamera import PiCamera

camera = PiCamera()

GPIO.setmode(GPIO.BCM)

GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Raspberry Pi pin setup
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 2

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

class Watcher:
    DIRECTORY_TO_WATCH = "images/"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                input_state = GPIO.input(19)
                if input_state == False:
                    camera.start_preview()
                    time.sleep(1.0)
                    timestr = time.strftime("%Y%m%d-%H%M%S")
                    camera.capture('images/' + timestr + '.jpg')
                    camera.stop_preview()
                    lcd.clear()
        except:
            self.observer.stop()
            print "Error"

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            lcd.message(event.src_path)
            time.sleep(0.5)
            lcd.clear()

if __name__ == '__main__':
    w = Watcher()
    w.run()