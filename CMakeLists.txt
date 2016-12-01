cmake_minimum_required(VERSION 2.8.3)
project(education_robotics)

# C++14:
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++1y")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${GAZEBO_CXX_FLAGS}")

find_package(catkin REQUIRED COMPONENTS
        roscpp
        rospy
        std_msgs
        gazebo_ros
        )


# Depend on system install of Gazebo
find_package(gazebo REQUIRED)

catkin_package(
        INCLUDE_DIRS include
        LIBRARIES education_robotics gazebo_ros_diff_drive
        CATKIN_DEPENDS roscpp rospy std_msgs
        DEPENDS  roscpp gazebo_ros gazebo  SDF
)

include_directories(
        include
        ${catkin_INCLUDE_DIRS}
)

link_directories(${GAZEBO_LIBRARY_DIRS})
include_directories(${Boost_INCLUDE_DIR} ${catkin_INCLUDE_DIRS} ${GAZEBO_INCLUDE_DIRS})

add_library(robot_ros_utils src/gazebo_plugins/robot_ros_utils.cpp)
target_link_libraries(robot_ros_utils ${GAZEBO_LIBRARIES} ${catkin_LIBRARIES} ${Boost_LIBRARIES})

add_library(robot_ros_diff_drive src/gazebo_plugins/robot_ros_diff_drive.cpp)
target_link_libraries(robot_ros_diff_drive gazebo_ros_utils ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES} ${Boost_LIBRARIES})