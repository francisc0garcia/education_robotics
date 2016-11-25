#!/usr/bin/env python

import sys
import roslib
import rospy
import math
import tf
from geometry_msgs.msg import Twist


class move_robot_test:

    def __init__(self):

        # Init ros node
        rospy.init_node('robot_cmd_vel')

        # create a publisher for command velocity
        self.cmd_vel_pub = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)

        # define rate of transmission
        self.rate = rospy.Rate(10.0)

        # send commands at 10 hz
        while not rospy.is_shutdown():
            # create Twist message
            cmd = Twist()
            cmd.linear.x = 0.1
            cmd.angular.z = 0.2

            # Send command
            self.cmd_vel_pub.publish(cmd)

            self.rate.sleep()

def main(args):

    ic = move_robot_test()
    rospy.init_node('move_robot_test', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)