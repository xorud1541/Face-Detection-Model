from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import tensorflow as tf
import pathlib
import os
import glob
import matplotlib.pyplot as plt
import datetime
from PIL import Image
from glob import glob
from tensorflow.keras import datasets, layers, models
from tensorflow.keras.layers import Flatten

root_dir = 'dataset'
data_dir = 'dataset/train'
test_dir = 'dataset/test'
log_dir = os.path.abspath('dataset/model/') + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

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

def show_image(image, pred):
    fig, axes = plt.subplots(1, 5, figsize=(20, 20))
    axes = axes.flatten()
    index = 0
    for img, ax in zip(image, axes):
        img = img.numpy().squeeze()
        ax.imshow(img)
        #plt.text(30, 30, 'test')
        print(np.argmax(pred[index]))
        ax.axis('off')
        index = index + 1
    plt.tight_layout()
    plt.show()

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
              loss=tf.keras.losses.categorical_crossentropy,
              metrics=['accuracy'])

steps_per_epoch = TRAIN_COUT / BATCH_SIZE
steps_per_validation = TEST_COUT / BATCH_SIZE
model.fit(train_ds, epochs=30, steps_per_epoch=steps_per_epoch, validation_data=test_ds, validation_steps=steps_per_validation)

path_save = './dataset/model/MyModel.h5'
model.save(path_save)


""" 모델 확인 
print('model has saved ... ')
restored_model = tf.keras.models.load_model(path_save)
print('model has loaded ... ')

evaluate_ds = test_ds.shuffle(130).take(100)
test_loss, test_acc = restored_model.evaluate(evaluate_ds)
print(test_acc)

image, label = next(iter(test_ds))
pred = restored_model.predict(image)
show_image(image[:5], pred[:5])
"""







