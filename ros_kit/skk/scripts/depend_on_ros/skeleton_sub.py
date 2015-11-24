import cv2 
import rospy
import os
import sys 
import roslib
import rospkg
import time
from std_msgs.msg import Bool
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
#from skk.msg import UserTracker
#from skk.msg import UserTrackerArray
from skk.msg import UserTrackerPoseArray

class Skeleton():
    def __init__(self):
        nite2.initialized()
        self.nt = nite2.UserTracker.open_any()
        pub = rospy.Publisher('skeleton', UserTrackerPoseArray, queue_size=10)
        self.uta = UserTrackerPoseArray()
        rate = rospy.Rate(100)

    def skeleton_tracker(self):
        while not rospy.is_shutdown():
            frame = ut.read_frame()
            depth_frame = frame.get_depth_frame()
            count = 0
            for fu in frame.users:
                user = fu
                if user.is_new():
                    ut.start_skeleton_tracking(fu.id)
                    print 'get new user:', fu.id
                    print 'user skeleton state:',user.skeleton.state
                # 2 means skeleton ok, if its a new user don't need to get state.
                elif user.skeleton.state == 2:
                    #head flag
                    head = users.skeleton.joints[0]
                    if(head.positionConfidence > 0.5):
                        print 'user id:', fu.id, 'head pose:', head.position
                        self.uta.users[count].uid = fu.id
                        #Just detect the head, so projective array index can be same as users' 
                        self.uta.users[count].uid.projective[count].x = head.position.x
                        self.uta.users[count].uid.projective[count].y = head.position.y
                        self.uta.users[count].uid.projective[count].z = head.position.z
                        self.uta.numUsers = len(frame.users)
                        pub.publish()

if __name__ == '__main__':
    rospy.init_node('skeleton_server')
    sk = Skeleton()
    rospy.spin()
