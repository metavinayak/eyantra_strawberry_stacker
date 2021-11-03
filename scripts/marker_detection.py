#!/usr/bin/env python3


'''
This is a boiler plate script that contains an example on how to subscribe a rostopic containing camera frames 
and store it into an OpenCV image to use it further for image processing tasks.
Use this code snippet in your code or you can also continue adding your code in the same file


This python file runs a ROS-node of name marker_detection which detects a moving ArUco marker.
This node publishes and subsribes the following topics:

	Subsriptions					Publications
	/camera/camera/image_raw			/marker_info
'''
from sensor_msgs.msg import Image
from task_1.msg import Marker
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import rospy
from aruco_library import *


class image_proc():

    # Initialise everything
    def __init__(self):
        rospy.init_node('marker_detection')  # Initialise rosnode

        # Making a publisher

        self.marker_pub = rospy.Publisher('/marker_info', Marker, queue_size=1)

        # ------------------------Add other ROS Publishers here-----------------------------------------------------

        # Subscribing to /camera/camera/image_raw

        # Subscribing to the camera topic
        self.image_sub = rospy.Subscriber(
            "/camera/camera/image_raw", Image, self.image_callback)

        # -------------------------Add other ROS Subscribers here----------------------------------------------------

        # This will contain your image frame from camera
        self.img = np.empty([])
        self.bridge = CvBridge()
        self.rate = rospy.Rate(10)
        # This will contain the message structure of message type task_1/Marker
        self.marker_msg = Marker()
        self.publish_data()

    # Callback function of amera topic

    def image_callback(self, data):
        # Note: Do not make this function lenghty, do all the processing outside this callback function
        try:
            # Converting the image to OpenCV standard image
            self.img = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
            return

    def publish_data(self):
        while not rospy.is_shutdown():
            if len(self.img.shape) > 0:
                Detected_ArUco_Markers = detect_ArUco(self.img)
                angles = Calculate_orientation_in_degree(
                    Detected_ArUco_Markers)
                idm, center_x, center_y, angle = -1, 0, 0, 0
                for id_, pos in Detected_ArUco_Markers.items():
                    idm = id_
                    center_x, center_y = np.int32((pos[0][0]+pos[0][2])/2)
                    angle = angles[id_]
                    rospy.loginfo(str(idm)+" "+str(center_x)+" "+str(center_y)+" "+str(angle))
                    self.marker_msg = Marker(
                        id_, center_x, center_y, 0, 0, 0, angle)
                    self.marker_pub.publish(self.marker_msg)
            self.rate.sleep()


if __name__ == '__main__':
    try:
        image_proc_obj = image_proc()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
