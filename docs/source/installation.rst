How to install education robotics
=================================

In order to use this project, we must install first ROS (tested on Jade and kinectic),
then compile the project and finally run some simulations and tests.


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

Compile project
^^^^^^^^^^^^^^^

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


Now you are ready to play and extend the project, let's go to section Tutorials and extensions.