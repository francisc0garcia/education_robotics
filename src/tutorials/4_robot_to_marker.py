#!/usr/bin/env python

import math
import rospy

# import dependencies
from RobotController import *


class Robot2Marker:
    def __init__(self):
        # Init ros node
        rospy.init_node('Robot2Marker')

        self.robot = RobotController()

        self.robot.marker_id_target = 3
        self.robot.marker_id_robot = 3

        # define rate of  10 hz
        self.rate = rospy.Rate(10.0)

        # infinity loop
        while not rospy.is_shutdown():
            [robot_position_x, robot_position_y, robot_orientation] = self.robot.get_position()
            [target_x, target_y, target_orientation] = self.robot.get_target_position()

            rospy.loginfo("robot position:" + str([robot_position_x, robot_position_y, robot_orientation]))

            self.rate.sleep()


def main(args):
    try:
        ic = Robot2Marker()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)