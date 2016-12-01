#!/usr/bin/env python

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

rad2degrees = 180.0/math.pi

class robot_update_map:

    def __init__(self):
        # Init ros node
        rospy.init_node('robot_update_map')

        # Read input parameters from launch file
        self.map_path_file = rospy.get_param('~map_path_file', 'map_image.png')

        [self.robot_position_x, self.robot_position_y, self.robot_orientation,
         self.robot_roll, self.robot_pitch, self.robot_yaw] = [0, 0, 0, 0, 0, 0]

        #create publisher for map
        self.map_pub = rospy.Publisher("/robot/map/image_raw", Image, queue_size=1)
        self.map_robot_pub = rospy.Publisher("/robot/map_robot_pub/image_raw", Image, queue_size=1)
        self.map = []

        self.bridge = CvBridge()

        # Load map into image
        self.load_map()

        # define rate of transmission: 10 hz
        self.rate = rospy.Rate(10.0)

        # create subscriber  for odometry
        self.sub_odometry = rospy.Subscriber('/robot/odom', Odometry, self.process_odometry_message, queue_size=1)

        # send commands at 10 hz
        while not rospy.is_shutdown():
            self.publish_map()
            self.rate.sleep()

    def load_map(self):
        self.map = cv2.imread(self.map_path_file, 0)

    def publish_map(self):
        map_temp = self.map
        map_original = cv2.cvtColor(self.map, cv2.COLOR_GRAY2RGB)

        #Add robot position into map
        map_temp = cv2.cvtColor(map_temp, cv2.COLOR_GRAY2RGB)
        cv2.ellipse(map_temp, (int(self.robot_position_y*100) , int(self.robot_position_x*100)),
                    (20, 20),
                    -(self.robot_yaw * rad2degrees),
                    0, 180, 255, -1)

        #cv2.imshow('map_temp', map_temp)
        #cv2.waitKey(10)

        # publish map with robot as image
        self.map_robot_pub.publish(self.bridge.cv2_to_imgmsg(map_temp, "bgr8"))

        # publish original map as image (no robot)
        self.map_pub.publish(self.bridge.cv2_to_imgmsg(map_original, "bgr8"))

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
        ic = robot_update_map()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)