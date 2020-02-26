import argparse
import cv2
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import model_from_json

import helper

Optimize_number = 0.14

cap = cv2.VideoCapture(0)
if (cap.isOpened() == False):
    print("Unable to read camera feed")
key = 0
print("Started...")

parser = argparse.ArgumentParser(description='Remote Driving')
parser.add_argument('model', type=str,
                    help='Path to model definition json. Model weights should be on the same path.')
args = parser.parse_args()
with open(args.model, 'r') as jfile:
    model = model_from_json(json.load(jfile))

model.compile("adam", "mse")
weights_file = args.model.replace('json', 'h5')
model.load_weights(weights_file)

while True:
    ret, frame = cap.read()
    key = cv2.waitKey(50)
    image_array = np.asarray(frame)
    image_array = helper.crop(image_array, 0.35, 0.1)
    image_array = helper.resize(image_array, new_dim=(64, 64))
    transformed_image_array = image_array[None, :, :, :]
    transformed_image_array = tf.cast(transformed_image_array, tf.float32)
    steering_angle = float(model.predict(transformed_image_array, batch_size=1))
    cv2.imshow("keytest", frame)

    if key is 120:
        break
    # print(steering_angle)

    if steering_angle > Optimize_number:
        print("TURN RIGHT!!!")
    elif steering_angle < Optimize_number and steering_angle > -1 * Optimize_number:
        print("STRAIGHT")
    elif steering_angle < -Optimize_number:
        print("TURN LEFT!!!")



