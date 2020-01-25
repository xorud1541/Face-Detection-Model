from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import tensorflow as tf
import pathlib
import os
import glob
import matplotlib.pyplot as plt
from PIL import Image
from glob import glob
from tensorflow.keras import datasets, layers, models

root_dir = 'dataset'
data_dir = 'dataset/train'
test_dir = 'dataset/test'

root_dir = pathlib.Path(root_dir)
data_dir = pathlib.Path(data_dir)
test_dir = pathlib.Path(test_dir)

AUTOTUNE = tf.data.experimental.AUTOTUNE
BATCH_SIZE = 10
TEST_COUT = 130
TRAIN_COUT = 500
CLASS_NAMES = np.array([item.name for item in data_dir.glob("*")])

def get_label(file_path):
    parts = tf.strings.split(file_path, os.path.sep)
    return parts[-2] == CLASS_NAMES

def decode_img(img):
    img = tf.image.decode_jpeg(img, channels=1)
    img = tf.image.convert_image_dtype(img, tf.float32)
    return img

def process_path(file_path):
    label = get_label(file_path)
    img = tf.io.read_file(file_path)
    img = decode_img(img)
    return img, label

def prepare_for_training(ds, cache=True, shuffle_buffer_size=5):
    ds = ds.shuffle(buffer_size=100)

    # Repeat forever
    ds = ds.repeat()
    ds = ds.batch(BATCH_SIZE)
    ds = ds.prefetch(buffer_size=AUTOTUNE)

    return ds

train_list_ds = tf.data.Dataset.list_files(str(data_dir/'*/*'))
test_list_ds = tf.data.Dataset.list_files(str(test_dir/'*/*'))

labeled_ds = train_list_ds.map(process_path, num_parallel_calls=AUTOTUNE)
train_ds = prepare_for_training(labeled_ds)

labeled_test_ds = test_list_ds.map(process_path, num_parallel_calls=AUTOTUNE)
test_ds = prepare_for_training(labeled_test_ds)

model = models.Sequential()
model.add(layers.Conv2D(16, (3, 3), activation='relu', input_shape=(96, 96, 1)))
model.add(layers.MaxPool2D((2, 2)))
model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.MaxPool2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPool2D((2, 2)))
model.add(layers.Conv2D(128, (5, 5),activation='relu'))
model.add(layers.MaxPool2D((2, 2)))

model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(5, activation='softmax'))
model.summary()

model.compile(optimizer=tf.optimizers.Adam(),
              loss=tf.keras.losses.binary_crossentropy,
              metrics=['accuracy'])

steps_per_epoch = TRAIN_COUT / BATCH_SIZE
steps_per_validation = TEST_COUT / BATCH_SIZE
model.fit(train_ds, epochs=20, steps_per_epoch=steps_per_epoch, validation_data=test_ds, validation_steps=steps_per_validation)

evaluate_ds = test_ds.take(100)
test_loss, test_acc = model.evaluate(evaluate_ds)
print(test_acc)

"""
image, label = next(iter(train_ds))
pred = model.predict(image)
print(np.argmax(pred[0]))
print(label[0])

image = image.numpy()
label = label.numpy()
plt.figure(figsize=(10, 10))
for n in range(10):
    ax = plt.subplot(5, 5, n+1)
    img = tf.reshape(image[n], [96, 96])
    plt.imshow(img)
    plt.title(CLASS_NAMES[label[n] == 1][0].title())
    plt.axis('off')
    plt.show()
"""






