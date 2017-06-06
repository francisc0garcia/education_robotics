#!/usr/bin/env python

import math
import rospy
# import dependencies
import sys
import time

from RobotController import *

rad2degrees = 180.0/math.pi


class RobotMapExample:
    def __init__(self):
        # Init ros node
        rospy.init_node('RobotMapExample')

        self.robot = RobotController()

        # define rate of  10 hz
        self.rate = rospy.Rate(10.0)

        # infinity loop
        while not rospy.is_shutdown():
            # extract dimension of map
            (total_rows, total_cols) = self.robot.map.shape

            # if map is ready:
            if total_rows > 0 and total_cols > 0:
                # start moving robot
                self.robot.move(0.2)

                # define a safety boundary region around robot
                boundary = 50  # +/- 50 pixels (1 meter = 100 pixels)

                # get position of the robot
                [robot_position_x, robot_position_y, robot_orientation] = self.robot.get_position()

                # loop inside boundary, check if there are obstacles
                lower_range_y = robot_position_y - boundary
                higher_range_y = robot_position_y + boundary

                lower_range_x = robot_position_x - boundary
                higher_range_x = robot_position_x + boundary

                # for y starting at "lower_range_y" until "higher_range_y"
                for y in range(lower_range_y, higher_range_y):

                    # for y starting at "lower_range_x" until "higher_range_x"
                    for x in range(lower_range_x, higher_range_x):
                        # get map point
                        # map_point = 255 means free space, zero is obstacle
                        map_point = self.robot.map[x, y]

                        # if map_point value = 0, an obstacle is detected
                        if map_point == 0:
                            # stop robot
                            self.robot.move(0.0)

                            # obstacle detected, rotate and continue
                            self.robot.rotate(0.3)
                            time.sleep(1.5)
                            self.robot.rotate(0.0)

                            # move forward
                            self.robot.move(0.2)
                            time.sleep(0.5)

                            # for logging: visualize using console plugin in rqt.
                            rospy.loginfo("close to obstacle y %f  x %f p %f", y , x, map_point)
                            break

            self.rate.sleep()


def main(args):
    try:
        ic = RobotMapExample()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)