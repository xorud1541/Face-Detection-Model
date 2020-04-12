import tensorflow as tf
import pathlib
import numpy as np
import sys
import os
from tensorflow.keras import datasets, layers, models

def decode_img(img):
    img = tf.image.decode_jpeg(img, channels=1)
    img = tf.image.convert_image_dtype(img, tf.float32)
    return img

class RedvelvetClassifier:
    modelPath = ''
    saved_model = 0
    def __init__(self):
        self.modelPath = './dataset/model' #학습된 모델 경로

    def loadModel(self):
        self.saved_model = tf.keras.models.load_model(self.modelPath)

    def predictImage(self, image):
        image = decode_img(image)
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
input_path = sys.argv[1]
print('input path:', input_path)

image = tf.io.read_file(input_path)
image = decode_img(image)

label = input_path.split('\\')[-2]
print('label', label)
model_pb_dir = './dataset/model' #학습된 모델 경로

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


