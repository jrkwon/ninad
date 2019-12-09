# -*- coding: utf-8 -*-
"""
Created on Wed May 23 13:55:21 2018

@author: mir-lab
"""

from PIL import Image
from config import Config

path = "/home/ghor9797/NCD_Github/test/ResNet/right.jpg"

#Before using this code, remove the .csv or .txt files from that folder

def crop():
    im = Image.open(path)
    imCrop = im.crop((0,370,800,620)) #corrected
    imCrop.save('right_crop.jpg')

crop()
