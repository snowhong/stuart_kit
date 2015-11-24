import cv2 
import rospy
import os
import sys 
import roslib
import time
from std_msgs.msg import Bool
from geometry_msgs.mgs import Vector3
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class Face_Service():
        def __init__(self):
                self.bridge = CvBridge()
                self.head_sub = rospy.Subscriber("/skeleton",UserTrackerPoseArray, self.utpa_callback, queue_size = 10)
                self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.image_callback, queue_size = 1)
                self.head_pose = Vector3()

                self.cascPath = os.path.join("/home/robot/Robot/src/backup/ros_kit/skk/config/","haarcascade_frontalface_default.xml")
                self.faceCascade = cv2.CascadeClassifier(self.cascPath)

        def utpa_callback(self, user_pose_array):
            

        def image_callback(self, image):
                try:
                    cv_image = self.bridge.imgmsg_to_cv2(image, "bgr8")
                    detection = self.detect_faces(cv_image)
                    for (x, y, w, h) in detection:
                        cv2.rectangle(cv_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

                    cv2.imshow("Face", cv_image)
                    cv2.waitKey(1)
                except CvBridgeError, e:
                    print e

        def detect_faces(self, image):
                _scale_Factor=1.2
                _min_Neighbor=5
                _min_Size=(30,30)
                flags = cv2.cv.CV_HAAR_SCALE_IMAGE
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                #faces=self.faceCascade.detectMultiScale(gray, _scale_Factor, _min_Neighbor, flags, _min_Size)

                faces = self.faceCascade.detectMultiScale(
                        gray,
                        scaleFactor=1.1,
                        minNeighbors=5,
                        minSize=(30, 30),
                        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                        )

                return faces

if __name__ == '__main__':
        rospy.init_node('face_srv')
        fd = Face_Service()
        rospy.spin()
                         
