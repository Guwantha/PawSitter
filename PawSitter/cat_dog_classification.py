import cv2 as cv
import numpy as np
import os
from sklearn.model_selection import train_test_split
import glob
import tensorflow as tf
import tensorflow_hub as hub

path, dirs, files = next(os.walk('E:\Competitions\SLIOT - PawSitter\Dog vs Cat identify\Train\Both'))
file_count = len(files)

# os.mkdir('E:/Competitions/SLIOT - PawSitter/Dog vs Cat identify/Train/Resized')

original_path = 'E:/Competitions/SLIOT - PawSitter/Dog vs Cat identify/Train/Both/'
resized_path = 'E:/Competitions/SLIOT - PawSitter/Dog vs Cat identify/Train/Resized/'

# Resize the images
'''for i in range(file_count):
    file_name = os.listdir(original_path)[i]
    img_path = original_path + file_name

    img = Image.open(img_path)
    img = img.resize((224,224))
    img = img.convert('RGB')

    newImgPath = resized_path+file_name
    img.save(newImgPath) '''

# Creating Lables
filenames = os.listdir(resized_path)
labels = []

for i in range(file_count):
    file_name = filenames[i]
    label = file_name[0:3]

    if label == 'dog':
        labels.append(1)
    else:
        labels.append(0)

# Convert all the resized imgs to numpy array

img_extension = ['png', 'jpg']
files = []

files = []

[files.extend(glob.glob(resized_path+'*.'+ e)) for e in img_extension]

dog_cat_imgs = np.asarray([cv.imread(file) for file in files])
# print(dog_cat_imgs.shape)

x = dog_cat_imgs
y = np.asarray(labels)

 # Train Test Split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)
# print(x.shape, x_train.shape, x_test.shape)

# Scaling the data
x_train_scale = x_train/255
x_test_scale = x_test/255

# print(x_train_scale)

# Building the neural Network
mobilenet_model = 'https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4'
pretrained_model = hub.KerasLayer(mobilenet_model, input_shape= (224,224,3), trainable=False )

num_of_classes = 2
model = tf.keras.Sequential([

    pretrained_model,
    tf.keras.layers.Dense(num_of_classes)
])

# model.summary()

model.compile(
    optimizer = 'adam',
    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['acc']
)

model.fit(x_train_scale, y_train, epochs=5)

model.save('pet_trained.keras')