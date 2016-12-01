How to install education robotics
=================================

In order to use this project, we must install first ROS (tested on Jade and kinectic),
then compile the project and finally run some simulations and tests.

you can choose between two options:

- Use virtual machine which has already everything ready (windows users)
- Install ROS and dependencies in your own ubuntu computer

Prepare virtual machine
^^^^^^^^^^^^^^^^^^^^^^^

- Download virtual machine from: http://goo.gl/vyQSGy

- Install VMware player (free for non-commercial application) from: http://www.vmware.com/products/player/playerpro-evaluation.html

- Uncompress virtual machine and open it using VMware workstation player

- Please disable 3D acceleration graphics, it is not supported by gazebo simulator

- the user is : **ubuntu** and password: **ubuntu**

If you get access to virtual machine successfully, then you can go to last section "Test project".

If you have an ubuntu PC and want to install the project locally, please follow the next tutorial:

Install ROS and dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Follow ros installation procedure:

http://wiki.ros.org/kinetic/Installation/Ubuntu

we can summarize the steps:

Open a command windows on ubuntu and run the following commands:

- Prepare ubuntu for installation:

.. code-block:: none

    sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
    sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 0xB01FA116
    sudo apt-get update

- Install ROS

For PC/Laptop we should install full desktop version:

.. code-block:: none

    sudo apt-get install ros-kinetic-desktop-full

For Raspberry PI 2 and Odroid we can install ROS-Base:

.. code-block:: none

    sudo apt-get install ros-kinetic-ros-base

Install rosdep:

.. code-block:: none

    sudo rosdep init
    rosdep update

And finally prepare environment:

.. code-block:: none

    echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
    source ~/.bashrc

Compile project (Only for local installation)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This step is only required if you install the project locally, please skip it if you use virtual machine.

First we need to install some dependencies and ROS packages:

.. code-block:: none

    sudo apt-get install libqwt-dev ros-kinetic-teleop-twist-joy  ros-kinetic-rviz-imu-plugin python-smbus ros-kinetic-rqt-multiplot


Finally we create a workspace for project, clone github repository, install dependencies and compile it:

.. code-block:: none

    mkdir -p ~/catkin_ws/src
    cd ~/catkin_ws/src
    git clone https://github.com/francisc0garcia/education_robotics
    cd ..
    source devel/setup.bash
    rosdep install education_robotics
    catkin_make


Test project
^^^^^^^^^^^^

Once the project has been compiled successfully,
we can run a simulation that includes a simple robot + environment.

.. code-block:: none

    cd ~/catkin_ws
    source devel/setup.bash
    roslaunch education_robotics demo_robot_simple.launch

if everything is correct, you should see a robot moving with predefined steps.

Now you are ready to play and extend the project, let's go to section Tutorials and extensions.