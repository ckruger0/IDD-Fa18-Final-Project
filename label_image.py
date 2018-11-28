# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

#!/usr/bin/python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
from picamera import PiCamera

import argparse
import sys
import time

import numpy as np
import tensorflow as tf

# Camera Setup
camera = PiCamera()
camera.vflip = True

# Picture capture button setup
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

DIRECTORY_TO_WATCH = "images/"

def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph

def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
				input_mean=0, input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(file_reader, channels = 3,
                                       name='png_reader')
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                  name='gif_reader'))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
  else:
    image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                        name='jpeg_reader')
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0);
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

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
                    lcd.clear()
                    lcd.message("Taking Picture...")
                    time.sleep(0.1)
                    timestr = time.strftime("%Y%m%d-%H%M%S")
                    camera.capture('images/' + timestr + '.jpg')
                    lcd.clear()
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            lcd.clear()
            lcd.message("Analyzing...")
            file_name = event.src_path
            model_file = "tf_files/retrained_graph.pb"
            label_file = "tf_files/retrained_labels.txt"
            input_height = 224
            input_width = 224
            input_mean = 128
            input_std = 128
            input_layer = "input"
            output_layer = "final_result"

            graph = load_graph(model_file)
            t = read_tensor_from_image_file(file_name,
                                            input_height=input_height,
                                            input_width=input_width,
                                            input_mean=input_mean,
                                            input_std=input_std)

            input_name = "import/" + input_layer
            output_name = "import/" + output_layer
            input_operation = graph.get_operation_by_name(input_name);
            output_operation = graph.get_operation_by_name(output_name);

            with tf.Session(graph=graph) as sess:
              start = time.time()
              results = sess.run(output_operation.outputs[0],
                                {input_operation.outputs[0]: t})
              end=time.time()
            results = np.squeeze(results)

            top_k = results.argsort()[-5:][::-1]
            labels = load_labels(label_file)

            lcd.clear()
            lcd.message(labels[top_k[0]])

if __name__ == "__main__":
  w = Watcher()
  w.run()
