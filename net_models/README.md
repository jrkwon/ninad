# Neural Network Model Analysis for E2E

## Assumptions

- `ros` and `neural_net` environments are already created.
- `ros-$ROS_DISTRO-joystick-drivers` is installed.

```
$ sudo apt install ros-$ROS_DISTRO-joystick-drivers
```
### Setup Logitech G920
```
$ cd catkin_ws
$ bash src/car_demo/car_demo/nodes/setup_driving_simulator.sh
```

## How to build

Start `ros` environmnet.
```
$ conda activate ros
```

Go to `catkin_ws` and build it.
```
(ros) $ cd catkin_ws
(ros) $ catkin_make
```

## How to start 

If you have not activated `ros` environment, do so with the following command.
```
$ conda activate ros
```

First enable your workspace environment.
```
(ros) $ . devel/setup.bash
```
Then, you will be able to start *rviz* and *Gazebo*.
```
(ros) $ roslaunch car_demo track.launch
```

## How to collect data

If you have not activated `ros` environment, do so with the following command.
```
$ conda activate ros
```

Open a new terminal and run the following commands.
```
(ros) $ . devel/setup.bash
(ros) $ cd catkin_ws
(ros) $ rosrun data_collection data_collection.py your_data_name
```
Your data will be saved at `data/your_data_name/year_month_date_time/*.jpg`. All image file names with corresponding steering angle and throttle value will be saved in the same folder.

## How to train

Activate `neural_net` environment.

```
$ conda activate neural_net
```

Go to `neural_net` folder.

```
(neural_net) $ python train.py ../data/your_data_name/year_month_date_time/
```

After the training is done, you will have .h5 and .json file in the `../data/your_data_name/` folder.

## How to run the trained ANN controller

Activate `neural_net` environment if you haven't yet.

```
$ conda activate neural_net
```

```
(neural_net) $ cd catkin_ws
(neural_net) $ rosrun run_neural run_neural.py ../data/your_data_name/year_month_date_time_n?
```
Note that `?` is a number indicating a network structure ID defined at `neural_net/config.py`

Then it will load the trained weight `your_data_name/year_month_date_time_n?.h5` and run it to generate the steering angle.
## Salient Features Visualization

Salient features is a very useful tool which shows how much is the responsibility of which part of the image in predicting the current predicted output. Basically, it draws a heat map on the input image which color codes the image in different segments. Red color being the most responsible and blue color being the least responsible. More details on the salient features is provided in my thesis.

There are two main files for observing the salient features of two networks 1) Nvidia `salient_Nvidia.py` and 2) Transfer Learning - ResNet `salient_ResNet.py`

The only thing that needs to be done before running this scripts is changing the path of network model (Line 21), path of input image (Line 28) and path of output image (Line 44)

Unfortunately, this salient feature only works with input of 3 channels and LSTM inputs 4 channels, so we cannot visulize LSTM using this feature.
