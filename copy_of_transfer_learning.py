# -*- coding: utf-8 -*-
"""Copy of Transfer_Learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IQNdAJf3N6kFwrDwvq4o3p0-qtK9WyF2
"""

# Load the Drive helper and mount
from google.colab import drive
 
# This will prompt for authorization.
drive.mount('/content/drive')



#import libaries
from tensorflow.keras.models import Sequential,Model
from keras.layers import Dense,Flatten,Dropout
from keras.applications.resnet50 import ResNet50

"""Transfer Learning - Fine Tunning"""

# use pretrained model
base_model = ResNet50(weights = 'imagenet',include_top = False,input_shape=(64,64,3))
#base_model = VGG19(include_top = True)
base_model.summary()

# freze the layer 
for layer in base_model.layers[:5]:
  layer.trainable = False

# Build our custom layer
x = base_model.output
x = Flatten()(x)

# new Fc layer 
x = Dense(512,activation='relu')(x)
x = Dropout(0.4)(x)
x = Dense(512,activation='relu')(x)
x = Dropout(0.4)(x)
x = Dense(128,activation='relu')(x)
x = Dropout(0.2)(x)
x = Dense(32,activation='relu')(x)
x = Dropout(0.2)(x)

# final layer 
final_layer = Dense(1,activation='softmax' )(x)

#combine the model
finetune_model = Model(inputs= base_model.input,outputs = final_layer)
finetune_model.summary()



# Part2 : Fitting the images to CNN model

from keras.preprocessing.image import  ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1./255,shear_range=0.2,
                                  horizontal_flip=True)


valid_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory('/content/drive/My Drive/Hackathon/train',target_size=(64,64),class_mode='categorical',batch_size=30,classes=['10_INR','20_INR', '50_INR', '100_INR','200_INR', '1000_Yen', '2000_Yen', '5000_Yen', '10000_Yen', '1_RM', '2_RM', '5 RM', '10_RM', '5_NZD', '10_NZD', '20_NZD', '50_NZD', '100_NZD'])


valid_generator = valid_datagen.flow_from_directory('/content/drive/My Drive/Hackathon/validate',target_size=(64,64),class_mode='categorical',batch_size=10,classes=['10_INR','20_INR', '50_INR', '100_INR','200_INR', '1000_Yen', '2000_Yen', '5000_Yen', '10000_Yen', '1_RM', '2_RM', '5 RM', '10_RM', '5_NZD', '10_NZD', '20_NZD', '50_NZD', '100_NZD'])

# compile the model 
finetune_model.compile(optimizer='Adam',loss='categorical_crossentropy',metrics=['accuracy'])

! pwd

# fit the model
finetune_model.fit(train_generator,steps_per_epoch=30,epochs=50,verbose=2,validation_data=valid_generator,validation_steps=10)

"""# Evaluating the Results """

# check what are the class indies
train_generator.class_indices

import tensorflow as tf
import cv2

category = ['10_INR','20_INR', '50_INR', '100_INR','200_INR', '1000_Yen', '2000_Yen', '5000_Yen', '10000_Yen', '1_RM', '2_RM', '5 RM', '10_RM', '5_NZD', '10_NZD', '20_NZD', '50_NZD', '100_NZD']

def prepare(filepath):
    img_size = 64
    img_arr = cv2.imread(filepath)
    new_arr = cv2.resize(img_arr,(img_size,img_size))
    return new_arr.reshape(-1, img_size,img_size,3)
    

def get_prediction(img_src):
   prediction = finetune_model.predict(prepare(src))
   #print("prediction :",prediction)
   for i in range(cateogory.length):  
    if prediction[0][0] == i :
      return cateogory[i]

import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

rootdir = '/content/drive/My Drive/Hackathon/test'
images = []
predictions = []

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        src = os.path.join(subdir, file)
        images.append(mpimg.imread(src))
        pred = get_prediction(src)
        predictions.append(pred)

plt.figure(figsize=(30,30))
columns = 3

for i, image in enumerate(images):
    plt.title(predictions[i])
    plt.subplot(len(images) / columns + 1, columns, i + 1)
    plt.imshow(image)

# Commented out IPython magic to ensure Python compatibility.
# single value prediction 

import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
# %matplotlib inline

category = ["dog","cat"'10_INR','20_INR', '50_INR', '100_INR','200_INR', '1000_Yen', '2000_Yen', '5000_Yen', '10000_Yen', '1_RM', '2_RM', '5 RM', '10_RM', '5_NZD', '10_NZD', '20_NZD', '50_NZD', '100_NZD'])
img_path = '/content/drive/My Drive/Colab Notebooks/Thakur_Session_CNN/CNN/dataset/dog2.jpg'
prediction = model.predict(prepare(img_path))
index = prediction[0][0]
im = cv2.imread(img_path,0)
plt.imshow(im,cmap='gray')
plt.title(category[int(index)])
plt.show()
