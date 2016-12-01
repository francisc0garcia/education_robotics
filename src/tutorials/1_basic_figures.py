#!/usr/bin/env python

import sys
import time
import roslib
import rospy
import math
import tf
from geometry_msgs.msg import Twist

class robot_move_test:

    def __init__(self):
        # Init ros node
        rospy.init_node('basicFigures')

        # create a publisher for command velocity
        self.cmd_vel_pub = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)

        # define rate of transmission: 10 hz
        self.rate = rospy.Rate(10.0)

        # send commands at 10 hz
        while not rospy.is_shutdown():

            # ---------------------
            # Place your code here:
            # remember you should create a set of figures with the robot
            # if you have problems, you can use robot_move_example.py as a example.

            # circle:

            # triangle:

            # square:


            # others?:



            # ----------------------

            self.rate.sleep()

    # Please Do not change the code below this line --------------------------------------

    # move forward robot
    def move_forward(self):
        # create Twist message
        cmd = Twist()
        cmd.linear.x = 0.3
        cmd.angular.z = 0.0

        # Send command
        self.cmd_vel_pub.publish(cmd)

    # move backward robot
    def move_backward(self):
        # create Twist message
        cmd = Twist()
        cmd.linear.x = -0.3
        cmd.angular.z = 0.0

        # Send command
        self.cmd_vel_pub.publish(cmd)

    # rotate to left
    def rotate_left(self):
        # create Twist message
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.6

        # Send command
        self.cmd_vel_pub.publish(cmd)

    # rotate to right
    def rotate_right(self):
        # create Twist message
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = -0.6

        # Send command
        self.cmd_vel_pub.publish(cmd)

    # stop robot: set linear and angular velocity to zero
    def stop_robot(self):
        # create Twist message
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0

        # Send command
        self.cmd_vel_pub.publish(cmd)

def main(args):
    try:
        ic = robot_move_test()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)