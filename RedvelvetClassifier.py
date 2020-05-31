import tensorflow as tf
import pathlib
import numpy as np
import sys
import os
from tensorflow.keras import datasets, layers, models
import IPython.display as display

def decode_img(img):
    img = tf.image.decode_jpeg(img, channels=1)
    img = tf.image.convert_image_dtype(img, tf.float32)
    return img

def function(image, label):
    print(image.shape)
    print(label.shape)
    return image, label

class Classifier:
    modelPath = ''
    saved_model = None
    def __init__(self):
        self.modelPath = './Model/dataset/model/MyModel.h5' #학습된 모델 경로

    def loadModel(self):
        print('model has loaded...')
        self.saved_model = tf.keras.models.load_model(self.modelPath, compile=True)

    def predictImage(self, array):
        image = tf.convert_to_tensor(array / 255)
        image = tf.image.convert_image_dtype(image, tf.float32)
        image = np.reshape(image, ((1,) + image.shape))
        predict_one_hot_array = self.saved_model.predict(image)
        predict_label = np.argmax(predict_one_hot_array)

        if predict_label == 0:
            predict_label = 'irene'
        elif predict_label == 1:
            predict_label = 'joy'
        elif predict_label == 2:
            predict_label = 'seulgi'
        elif predict_label == 3:
            predict_label = 'wendy'
        else:
            predict_label = 'yeri'

        return predict_label

    def retrainModel(self, imageArray, label):
        CLASS_NAMES = np.array(['irene', 'joy', 'seulgi', 'wendy', 'yeri'])
        imageArray = imageArray / 255.0
        imageLabel = np.array(label == CLASS_NAMES)

        imageArray = tf.convert_to_tensor(imageArray)
        imageLabel = tf.convert_to_tensor(imageLabel)

        imageArray = tf.expand_dims(imageArray, 0)
        images = tf.tile(imageArray, [500, 1, 1, 1])

        imageLabel = tf.expand_dims(imageLabel, 0)
        labels = tf.tile(imageLabel, [500, 1])

        train_ds = tf.data.Dataset.from_tensor_slices((images, labels))
        train_ds = train_ds.map(function)
        train_ds = train_ds.repeat()
        train_ds = train_ds.batch(10)

        self.saved_model.fit(train_ds, epochs=10, steps_per_epoch=50)

        print('finish')


"""
#input_path = sys.argv[1]
input_path = 'Model\\dataset\\test\\irene\\1.jpg'
print('input path:', input_path)

image = tf.io.read_file(input_path)
image = decode_img(image)

label = input_path.split('\\')[-2]
print('label', label)
model_pb_dir = './Model/dataset/model' #학습된 모델 경로

print('model has loaded...')

saved_model = tf.keras.models.load_model(model_pb_dir)

image = np.reshape(image, ((1,) + image.shape))
predict_one_hot_array = saved_model.predict(image)
predict_label = np.argmax(predict_one_hot_array)

if predict_label == 0:
    predict_label = 'irene'
elif predict_label == 1:
    predict_label = 'joy'
elif predict_label == 2:
    predict_label = 'seulgi'
elif predict_label == 3:
    predict_label = 'wendy'
else:
    predict_label = 'yeri'

print('predict: ', predict_label)
if predict_label == label:
    print('correct!')
else:
    print('incorrect!')
"""


