#import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten, Lambda, Activation, MaxPooling2D
from tensorflow.keras.layers import Conv2D, Dropout
from tensorflow.keras import Sequential
from tensorflow.keras.optimizers import Adam

import helper

#tf.python.control_flow_ops = tf

number_of_epochs = 6
number_of_samples_per_epoch = 4992
number_of_validation_samples = 512
learning_rate = 1e-4
activation_relu = 'relu'

# Our model is based on NVIDIA's "End to End Learning for Self-Driving Cars" paper
# Source:  https://images.nvidia.com/content/tegra/automotive/images/2016/solutions/pdf/end-to-end-dl-using-px.pdf
model = Sequential()

model.add(Lambda(lambda x: x / 127.5 - 1.0, input_shape=(64, 64, 3)))

# border_mode = padding
# subsample == stride
# starts with five convolutional and maxpooling layers
model.add(Conv2D(24, 5, padding='same', strides=2, activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=1))
model.add(Dropout(0.2))
model.add(Conv2D(36, 5, padding='same', strides=2, activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=1))

model.add(Conv2D(48, 5, padding='same', strides=2, activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=1))

model.add(Conv2D(64, 3, padding='same', strides=1, activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=1))
model.add(Dropout(0.2))
model.add(Conv2D(64, 3, padding='same', strides=1, activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=1))

model.add(Flatten())

# Next, five fully connected layers
model.add(Dense(1164, activation='relu'))

model.add(Dense(100, activation='relu'))

model.add(Dense(50, activation='relu'))

model.add(Dense(10, activation='relu'))

model.add(Dense(1))

model.summary()

model.compile(optimizer=Adam(learning_rate), loss="mse", )

# create two generators for training and validation
train_gen = helper.generate_next_batch()
validation_gen = helper.generate_next_batch()

history = model.fit(train_gen,
                    steps_per_epoch=number_of_samples_per_epoch,
                    epochs=number_of_epochs,
                    validation_data=validation_gen,
                    validation_steps=number_of_validation_samples,
                    verbose=1)

# finally save our model and weights
helper.save_model(model)
