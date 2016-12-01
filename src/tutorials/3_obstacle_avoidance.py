#!/usr/bin/env python

#import dependencies
import sys
import roslib
import rospy
import math
import tf
import cv2
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

rad2degrees = 180.0/math.pi

class robot_map_example:

    def __init__(self):
        # Init ros node
        rospy.init_node('robot_map_example')

        # create a publisher for command velocity
        self.cmd_vel_pub = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)

        # initialize variables for position and orientation of robot
        [self.robot_position_x, self.robot_position_y, self.robot_orientation,
         self.robot_roll, self.robot_pitch, self.robot_yaw] = [0, 0, 0, 0, 0, 0]

        self.map = np.zeros( (0, 0), dtype=np.uint8)
        self.bridge = CvBridge()

        # define rate of  10 hz
        self.rate = rospy.Rate(10.0)

        # create subscriber for robot odometry
        self.sub_odometry = rospy.Subscriber('/robot/odom', Odometry, self.process_odometry_message, queue_size=1)

        # create subscriber for map
        self.image_sub = rospy.Subscriber("/robot/map/image_raw", Image, self.callback_map)

        # infinity loop
        while not rospy.is_shutdown():

            # extract dimension of map
            (total_rows, total_cols) = self.map.shape

            # if map is valid:
            if total_rows > 0 and total_cols > 0:
                # define a safety boundary region around robot
                boundary = 40 # +/- 40 pixels (1 meter = 100 pixels)
                detected_obstacle = False

                # loop inside boundary, check if there are obstacles

                # for y starting at (robot_position_y - boundary) until (robot_position_y + boundary)
                for y in range( int((self.robot_position_y*100) - boundary), int((self.robot_position_y*100) + boundary) ):

                    # for x starting at (robot_position_x - boundary) until (robot_position_x + boundary)
                    for x in range( int((self.robot_position_x*100) - boundary), int((self.robot_position_x*100) + boundary) ):
                        map_point = self.map[x, y]
                        if map_point < 1:
                            # Obstacle detected!
                            detected_obstacle = True

                            # Here design your own routine for obstacle avoidance and navigation!
                            # remember you should send command velocities using self.cmd_vel_pub
                            # if you have questions, please check previous examples.

                            # for logging: visualize using console plugin in rqt.
                            # rospy.loginfo("close to obstacle y %f  x %f p %f", y , x, map_point)

                            break

            self.rate.sleep()

    # Update map
    def callback_map(self, data):
        try:
            temp_map = self.bridge.imgmsg_to_cv2(data, "bgr8")

            # convert into gray scale
            (rows, cols, channels) = temp_map.shape
            if cols > 0 and rows > 0 :
                self.map = cv2.cvtColor(temp_map,cv2.COLOR_RGB2GRAY)

        except CvBridgeError as e:
            print(e)

    # update position and orientation of robot (odometry)
    def process_odometry_message(self, odometry_msg):
        self.robot_position_x = odometry_msg.pose.pose.position.x
        self.robot_position_y = odometry_msg.pose.pose.position.y
        self.robot_orientation = odometry_msg.pose.pose.orientation.y

        quaternion = (
            odometry_msg.pose.pose.orientation.x,
            odometry_msg.pose.pose.orientation.y,
            odometry_msg.pose.pose.orientation.z,
            odometry_msg.pose.pose.orientation.w)

        (self.robot_roll, self.robot_pitch, self.robot_yaw) = euler_from_quaternion(quaternion)

def main(args):
    try:
        ic = robot_map_example()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)