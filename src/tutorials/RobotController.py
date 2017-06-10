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
from visualization_msgs.msg import Marker
from tf.transformations import euler_from_quaternion

rad2degrees = 180.0/math.pi


class RobotController:
    def __init__(self):
        # initialize variables for position and orientation of robot
        [self.robot_position_x, self.robot_position_y, self.robot_orientation,
         self.robot_roll, self.robot_pitch, self.robot_yaw] = [0, 0, 0, 0, 0, 0]

        self.map = np.zeros((0, 0), dtype=np.uint8)
        self.bridge = CvBridge()

        self.marker_id_robot = 0
        self.marker_id_target = 0
        self.scale_marker = 1.5

        self.target_position_x = 0.0
        self.target_position_y = 0.0
        (self.target_roll, self.target_pitch, self.target_yaw) = [0.0, 0.0, 0.0]

        # create a publisher for command velocity
        self.cmd_vel_pub = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)

        # create subscriber for robot odometry
        self.sub_odometry = rospy.Subscriber('/robot/odom', Odometry, self.process_odometry_message, queue_size=1)

        # create subscriber for map
        self.image_sub = rospy.Subscriber("/robot/map/image_raw", Image, self.callback_map)

        # create subscriber marker for robot
        self.marker_sub = rospy.Subscriber("/aruco_system_viewer/visualization_marker", Marker, self.callback_marker)

    def get_position(self):
        pos_x = int(self.robot_position_x*100)
        pos_y = int(self.robot_position_y*100)

        return [pos_x, pos_y, self.robot_yaw]

    def get_target_position(self):
        pos_x = int(self.target_position_x*100)
        pos_y = int(self.target_position_y*100)

        return [pos_x, pos_y, self.target_yaw]

    def move(self, linear_velocity):
        # create Twist message
        cmd = Twist()
        cmd.linear.x = linear_velocity
        cmd.angular.z = 0.0

        # Send command
        self.cmd_vel_pub.publish(cmd)

    def rotate(self, angular_velocity):
        # create Twist message
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = angular_velocity

        # Send command
        self.cmd_vel_pub.publish(cmd)

    # Update map
    def callback_map(self, data):
        try:
            temp_map = self.bridge.imgmsg_to_cv2(data, "bgr8")

            # convert into gray scale
            (rows, cols, channels) = temp_map.shape
            if cols > 0 and rows > 0:
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

    def callback_marker(self, msg):
        if msg.id == self.marker_id_robot:
            self.robot_position_x = msg.pose.position.x * self.scale_marker
            self.robot_position_y = msg.pose.position.y * self.scale_marker

            quaternion = (
                msg.pose.orientation.x,
                msg.pose.orientation.y,
                msg.pose.orientation.z,
                msg.pose.orientation.w)

            (self.robot_roll, self.robot_pitch, self.robot_yaw) = euler_from_quaternion(quaternion)

        if msg.id == self.marker_id_target:
            self.target_position_x = msg.pose.position.x
            self.target_position_y = msg.pose.position.y

            quaternion = (
                msg.pose.orientation.x,
                msg.pose.orientation.y,
                msg.pose.orientation.z,
                msg.pose.orientation.w)

            (self.target_roll, self.target_pitch, self.target_yaw) = euler_from_quaternion(quaternion)
