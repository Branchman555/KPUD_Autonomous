import argparse
import base64
import json
from io import BytesIO

import eventlet.wsgi
import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask
from keras.models import model_from_json

import helper

import os
model = None


def crop(image, top_cropping_percent):
    assert 0 <= top_cropping_percent < 1.0, 'top_cropping_percent should be between zero and one'
    percent = int(np.ceil(image.shape[0] * top_cropping_percent))
    return image[percent:, :, :]


@sio.on('telemetry')
def telemetry(sid, data):

    image_array = np.asarray(image)

    image_array = helper.crop(image_array, 0.35, 0.1)
    image_array = helper.resize(image_array, new_dim=(64, 64))

    transformed_image_array = image_array[None, :, :, :]

    # This model currently assumes that the features of the model are just the images. Feel free to change this.

    steering_angle = float(model.predict(transformed_image_array, batch_size=1))
    # The driving model currently just outputs a constant throttle. Feel free to edit this.
    throttle = 0.3

    print('{:.5f}, {:.1f}'.format(steering_angle, throttle))

    send_control(steering_angle, throttle)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remote Driving')
    parser.add_argument('model', type=str,
                        help='Path to model definition json. Model weights should be on the same path.')
    args = parser.parse_args()
    with open(args.model, 'r') as jfile:
        model = model_from_json(json.load(jfile))

    model.compile("adam", "mse")
    weights_file = args.model.replace('json', 'h5')
    model.load_weights(weights_file)

    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)