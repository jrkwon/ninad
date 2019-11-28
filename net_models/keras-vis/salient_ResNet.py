#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Wed Nov 20 09:19 2019

@author: doshininad
"""
import numpy as np
from matplotlib import pyplot as plt
from keras.preprocessing.image import img_to_array
from vis.utils import utils
from keras.models import model_from_json
from keras.models import Sequential, Model
from keras.layers import Lambda, Dropout, Flatten, Dense, Activation, Concatenate
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Input
from keras import losses, optimizers
from vis.visualization import visualize_cam, overlay
import matplotlib.cm as cm
import cv2

model_path = '/home/ghor9797/NCD_Github/python/pretrained_weights/Transfer_Learning_ResNet_3/2019-04-29-20-07-40'

model = model_from_json(open(model_path+'.json').read())
model.load_weights(model_path+'.h5')
model.compile(loss=losses.mean_squared_error, optimizer=optimizers.Adam())
model.summary()

img = utils.load_img('/home/ghor9797/NCD_Github/test/ResNet/straight_crop.jpg', target_size=(200,400))

bgr_img = utils.bgr2rgb(img)
img_input = np.expand_dims(img_to_array(bgr_img), axis=0)
pred = model.predict(img_input)[0][0]
print('Predicted {}'.format(pred))

titles = ['right_steering', 'left_steering', 'maintain_steering']
modifiers = [None, 'negate', 'small_values']
for i, modifier in enumerate(modifiers):
    heatmap = visualize_cam(model, layer_idx=-1, filter_indices=0, seed_input=bgr_img, grad_modifier=modifier)
    #plt.figure()
    #plt.title(titles[i])
    jet_heatmap = np.uint8(cm.jet(heatmap)[..., :3] * 255)
    #plt.imshow(overlay(img, jet_heatmap, alpha=0.7))
    out_img = overlay(img, jet_heatmap, alpha=0.8)
    cv2.imwrite('/home/ghor9797/NCD_Github/test/ResNet/' + 'straight_' + str(i) + '.jpg', out_img)
