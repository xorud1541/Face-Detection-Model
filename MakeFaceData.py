import cv2
import numpy as np
import os
from PIL import Image
import scipy.misc

base_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(base_dir, "temp")

face_cascade = cv2.CascadeClassifier('./OpenCV-Python-Series/src/cascades/data/haarcascade_frontalface_default.xml')
count = 0
for root, dirs, files in os.walk(images_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file) #이미지의 경로
            count = count + 1
            pil_image = Image.open(path).convert("L") #grayscale
            image_array = np.array(pil_image, "uint8")
            face = face_cascade.detectMultiScale(image_array, scaleFactor=1.1, minNeighbors=5)


            for (x, y, w, h) in face:
                roi = image_array[y:y+h, x:x+w]

            final_image = Image.fromarray(roi)
            newsize = (96, 96)
            final_image = final_image.resize(newsize)
            image_name = "images/%d.jpg" % count
            final_image.save(image_name)
print('end')