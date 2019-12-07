#!/usr/bin/env python

import datetime
import os
import cv2
import time
import rospy
import numpy as np
from bolt_msgs.msg import Control
from std_msgs.msg import Int32
from sensor_msgs.msg import Image

import sys

sys.path.append('../neural_net/')

import const
from image_converter import ImageConverter
from drive_run import DriveRun
from config import Config
from image_process import ImageProcess


class NeuralControl:
    def __init__(self, weight_file_name, default_speed):
        rospy.init_node('run_neural')
        self.ic = ImageConverter()
        self.image_process = ImageProcess()
        self.rate = rospy.Rate(30)
        self.drive= DriveRun(weight_file_name)
        rospy.Subscriber('/bolt/front_camera/image_raw', Image, self.controller_cb)
        self.image = None
        self.image_processed = False
        self.config = Config()
        self.default_speed = default_speed

    def controller_cb(self, image): 
        img = self.ic.imgmsg_to_opencv(image)
        cropped = img[const.CROP_Y1:const.CROP_Y2,
                      const.CROP_X1:const.CROP_X2]

        img = cv2.resize(cropped,(const.IMAGE_WIDTH, const.IMAGE_HEIGHT))

        self.image = self.image_process.process(img)

        if self.config.net_model_type == const.NET_TYPE_LSTM_FC6 \
            or self.config.net_model_type == const.NET_TYPE_LSTM_FC7:
            self.image = np.array(self.image).reshape(1, self.config.image_size[1],
                                                         self.config.image_size[0],
                                                         self.config.image_size[2])
        self.image_processed = True

def main():
    if len(sys.argv) != 3:
        exit('Usage:\n$ rosrun run_neural run_neural.py weight_file_name default_speed(0~1)')

    neural_control = NeuralControl(sys.argv[1], float(sys.argv[2]))
    print('\nStart running. Vroom. Vroom. Vroooooom......')
  
    joy_pub = rospy.Publisher('/bolt', Control, queue_size = 10)
    joy_data = Control()
  
    while not rospy.is_shutdown():
        if neural_control.image_processed is False:
            continue
        
        prediction = neural_control.drive.run(neural_control.image)
        joy_data.steer = prediction
        joy_data.throttle = neural_control.default_speed
        joy_pub.publish(joy_data)

        ## print out
        sys.stdout.write('steer: ' + str(joy_data.steer) +' throttle: ' + str(joy_data.throttle) + '\r')
        sys.stdout.flush()

        ## ready for processing a new input image
        neural_control.image_processed = False
        neural_control.rate.sleep()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print ('\nShutdown requested. Exiting...')
