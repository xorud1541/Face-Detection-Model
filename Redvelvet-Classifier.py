import tensorflow as tf
import pathlib
import numpy as np
import os
from tensorflow.keras import datasets, layers, models

#input-dir: /irene/1.png
#image: 1.png
#label: irene

model_pb_dir = './dataset/model/saved_model.pb' #학습된 모델 경로
model_pb_dir = pathlib.Path(model_pb_dir)

print('model has loaded...')

saved_model = tf.keras.models.load_model(model_pb_dir)
predict_one_hot_array = saved_model.predict(#image)
predict_label = np.argmax(predict_one_hot_array)



