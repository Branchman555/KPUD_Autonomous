import argparse
import cv2
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import model_from_json
import serial

import helper

Optimize_number = 0.14
print("Camera Initializing...")
cap = cv2.VideoCapture(0)
if (cap.isOpened() == False):
    print("Unable to read camera feed")
key = 0
print("Ready... Go?")
input()
print("Program Started...!")

ser = serial.Serial("COM5", 115200)

parser = argparse.ArgumentParser(description='Remote Driving')
parser.add_argument('model', type=str,
                    help='Path to model definition json. Model weights should be on the same path.')
args = parser.parse_args()
with open(args.model, 'r') as jfile:
    model = model_from_json(json.load(jfile))

model.compile("adam", "mse")
weights_file = args.model.replace('json', 'h5')
model.load_weights(weights_file)

for i in range(30):
    dataFormat = "<250,255,0>"
    ser.write(dataFormat.encode())
    print(dataFormat)
    key = cv2.waitKey(30)
while True:
    ret, frame = cap.read()
    key = cv2.waitKey(30)
    image_array = np.asarray(frame)
    image_array = helper.crop(image_array, 0.3, 0.35)
    image_array = helper.resize(image_array, new_dim=(64, 64))
    transformed_image_array = image_array[None, :, :, :]
    transformed_image_array = tf.cast(transformed_image_array, tf.float32)
    steering_angle = float(model.predict(transformed_image_array, batch_size=1))
    cv2.imshow("keytest", frame)
    INT_steering = 0
    INT_steering = int(steering_angle * 250)
    if INT_steering > 250:
        INT_steering = 250
    elif INT_steering < -250:
        INT_steering = -250
    INT_steering += 250
    dataFormat = "<{},510,1>".format(INT_steering)
    ser.write(dataFormat.encode())
    print(dataFormat)

    if key is 120:
        dataFormat = "<250,255,3>"
        ser.write(dataFormat.encode())
        print(dataFormat)
        break
    print(steering_angle)
print("Program Exit...")




