#!/usr/bin/env python

import rospy

from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from std_msgs.msg import String

from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import cv2
import os
import requests

import PIL
from io import BytesIO
import base64


class inloc_wrapper(object):

    def __init__(self):

        # we can subscribe to any image data
        # for example: /torso_back_camera/fisheye1/image_raw
        self.image_sub = rospy.Subscriber("/torso_back_camera/fisheye1/image_raw", Image, self.camera_callback)
        self.bridge_object = CvBridge()

    def camera_callback(self, data):
        # if subscribed to ARI image data we can modify and show image here :
        try:
            cv_image = self.bridge_object.imgmsg_to_cv2(
                data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)

        # show image
        cv2.imshow('original_image', cv_image)
        cv2.waitKey()
        
        # # save images and exit
        # cv2.imwrite('original_image.jpg', cv_image)
        # cv2.destroyAllWindows()

        # save images if pressed by s, or wait for ESC key to exit
        k=cv2.waitKey(1) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()
        elif k == ord('s'):    
            cv2.imwrite('fisheye_image.jpg', cv_image)
            cv2.destroyAllWindows()
    

    def send_image(self, image):
        # sends image data to server and returns it after modification :
        url = "http://127.0.1.1:9099/api/matlab_run_cmd"
       
        img = base64.b64encode(image.read())
        response = requests.post(url, data=img)
        
        if response.ok:
            rospy.loginfo("It workes!")
            rospy.loginfo(response.content)
        else:
            rospy.loginfo("Something went wrong!")



def main():

    serv = inloc_wrapper()
    rospy.init_node('communication', anonymous=True)
    rospy.loginfo("ROS server communication layer is now started ...")


    image = open('/home/user/ari_public_ws/src/ros_server_communication/src/original_image.jpg', 'rb')

    # to loop the process :
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        serv.send_image(image)
        rate.sleep()
    
    # serv.send_image(image)


if __name__ == '__main__':
    main()
