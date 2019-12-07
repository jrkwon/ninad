#!/usr/bin/env python

import rospy
import cv2
import os
import numpy as np
import datetime
import time
import sys
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from std_msgs.msg import String
from bolt_msgs.msg import Control

sys.path.append('../neural_net/')
from image_converter import ImageConverter
import const

vehicle_steer = 0
vehicle_vel = 0

ic = ImageConverter()

##
# data will be saved in your_project_home/data/data_id/

if len(sys.argv) != 2:
    print('Usage: ')
    exit('$ rosrun data_collection data_collection.py your_data_id')

name_datatime = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
path = '../data/' + sys.argv[1] + '/' + name_datatime + '/'
if os.path.exists(path):
    print('path exists. continuing...')
else:
    print('new folder created: ' + path)
    os.makedirs(path)

text = open(str(path) + name_datatime + const.DATA_EXT, "w+")

def vehicle_param(value):
    global vehicle_vel, vehicle_steer
    vehicle_vel = value.throttle
    vehicle_steer = value.steer
    #return (vehicle_vel, vehicle_steer)

def recorder(data):
    img = ic.imgmsg_to_opencv(data)

    # crop
    cropped = img[const.CROP_Y1:const.CROP_Y2,
                  const.CROP_X1:const.CROP_X2]

    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    file_full_path = str(path) + str(time_stamp) + const.IMAGE_EXT
    cv2.imwrite(file_full_path, cropped)
    sys.stdout.write(file_full_path + ' created.\r')
    text.write(str(time_stamp) + const.IMAGE_EXT + ',' + str(vehicle_steer) + ',' + str(vehicle_vel) + "\r\n")
    

def main():
   rospy.init_node('data_collection')
   rospy.Subscriber('/bolt', Control, vehicle_param)
   rospy.Subscriber('/bolt/front_camera/image_raw', Image, recorder)
   rospy.spin()

if __name__ == '__main__':
    main()
