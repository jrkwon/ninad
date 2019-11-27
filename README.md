# Setting up Gazebo Environment

This section describes how to setup your gazebo environment. This gazebo environment will be used during data collection as well as testing the trained network and driving the vehicle autonomously.

Once you clone the package from Github, it needs to be build in your system in order for it to work. You cannot use it without building. Make sure you have all the dependencies before buliding, otherwise you will encounter errors.

Steps:
Open Terminal
Go to folder `catkin_ws` in the terminal
``$ catkin_make -j$(nproc)``

?? why should libTrafficLightsGUIPlugin.so be copied to devel/lib ?? 
The package will be build in your system


# Opening and using Gazebo

The vehicle in the environment can be ran using Logitech G920, joystick or keyboard. The script were the action of all the buttons on the joystick or simulator are defined is at `./catkin_ws/src/car_demo/car_demo/nodes/joystick_translator`. By default the axis number of Logitech G920 is set. If you are using joystick, then you need to set the axis numbers accordingly. For keyboard, you dont need to change anything in the script.

There are two different types of environments available with this package. 1) track 2) mcity

Once you have the script setup that supports the connected device and you decide the environment to run, then you can use the following commands:
``$ source devel/setup.bash``

## For data collection
``$ roslaunch car_demo track.launch`` (for launching track)
This commands will open the environment with the vehicle and it will also open Rviz where you can visualize the sensor data


# Setting up Anaconda Environment

Anaconda creates a virtual environment which takes care of all the dependencies required for this project. `training.yml` file is provided with the package. The only thing that needs to be done is import this yml file to anaconda navigator on your pc using the following steps.

Make sure you have anaconda installed on your PC. If it is not installed search google and install it.
Open the terminal at the location of `training.yml` file
``$ conda env create -f ninad_training.yml``
Now the virtual environment training.yml is set up in the anaconda of your PC
Whenever required it can be activated using ``$ conda activate ninad_training``
You can also deactivate it using ``$ conda deactivate``

NOTE: Anaconda should not be running at the time of building the `catkin_ws` package; Anaconda should not be running at the time of running the gazebo environment; It is recommended to always use Anaconda while running the python scripts provided in the `python` folder, because it takes care of all the dependencies. 


# Data Collection

 `data_collection` is a package for data collection. 
 
 ``$ rosrun data_collection data_collection.py ../data_path/``

Once you are done collecting data then just press Ctrl+C in the terminal which is collecting data to stop collecting it. At the location defined by you, there would be new folder created with the time stamp containing the images in .jpg format and a text file with the details of steering angle for every image.

All other modules besde data_collection can be found in the `python` folder.

# Training

All the files required for training and testing are provided in the folder `python`.

## txt2csv.py

First of all, when we need to fix a tab separated value file in the Windows text file format, we can use ``txt2csv.py``. This will create a new csv file format in the Linux text file format.

``$ python txt2csv.py path_to_a_txt_file_name``

## config.py

This file has all necessary pieces of information for the training. You may change values when necessary. Note that this file does not need to be run by a user. Important things that needs to be checked in this file before running training or testing is explained below.

Line 23: self.typeofModel = select the model number which you want to use for training

## train.py

After all parameters are properly set in ``config.py``, this ``train.py`` is the ultimate solution for the training. 

``$ python train.py path_to_a_folder_of_a_driving_data``

Note that you must use the path name of a driving data folder. This must not be a csv file name.
If you properly give a driving data folder, you will see followings.

```
Using TensorFlow backend.
100% (29200 of 29200) |###################| Elapsed Time: 0:00:11 Time: 0:00:11
Train samples:  20440
Valid samples:  8760
Epoch 1/5
 716/1277 [===============>..............] - ETA: 1373s - loss: 3.9270 
```


# Testing with collected data

Once a steering model is trained and created, it is time to test the model with another data set, which is often called a test data set.

# test.py

To test a steering model with a test set, two arguments must be specified: a model name and a test set data folder name.

``$ python test.py steering_model_name test_data_folder_name``

The steering model name is a name of the weights (.h5) and the network model (.json) without an extension.

For example, if the weight fiel name is 2017-05-31-20-49-09.h5 and the network model name is 2017-05-31-20-49-09.json and they are at the folder ../mir_torcs_drive_data/, then you can use ``test.py`` as follows.

``$ python test.py ../mir_torcs_drive_data/2017-05-31-20-49-09 ../mir_torcs_drive_data/2017-05-31-17-26-11``

An example outputs is as follows.

```
100% (14866 of 14866) |###################| Elapsed Time: 0:00:05 Time: 0:00:05
  1% (3 of 233) |                          | Elapsed Time: 0:00:00 ETA: 0:00:09
  Test samples:  14866

Evaluating the model with test data sets ...
100% (233 of 233) |#######################| Elapsed Time: 0:00:22 Time: 0:00:22
  3% (8 of 233) |                          | Elapsed Time: 0:00:00 ETA: 0:00:22
Loss:  0.00106151084765
```


# Testing on Gazebo Environment

Follow the steps explained above to open the track of your choice in Gazebo. Once the track is ready in Gazebo and you already have the trained model and weights, then follow the steps below to run the vehicle autonomously.

Open a new Terminal and make sure that you change the directory to `catkin_ws`. This is because `run_neural` package has dependency with python code in `neural_net` folder.

``$ rosrun run_neural run_neural path_to_pretrained_model(excluding .h5 or.json)`` 

Enjoy the ride of autonomous vehicle (at your own risk) :P


# Salient Features Visualization

Salient features is a very useful tool which shows how much is the responsibility of which part of the image in predicting the current predicted output. Basically, it draws a heat map on the input image which color codes the image in different segments. Red color being the most responsible and blue color being the least responsible. More details on the salient features is provided in my thesis.

There are two main files for observing the salient features of two networks 1) Nvidia `salient_Nvidia.py` and 2) Transfer Learning - ResNet `salient_ResNet.py`

The only thing that needs to be done before running this scripts is changing the path of network model (Line 21), path of input image (Line 28) and path of output image (Line 44)

Unfortunately, this salient feature only works with input of 3 channels and LSTM inputs 4 channels, so we cannot visulize LSTM using this feature.
