import rospy
import time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

image_topic = 'cameras/right_hand_camera/image'

class CameraSubscriber:

	def __init__(self):
		self.acceptingImages = False
		self.isNewImage = False
		self.bridge = CvBridge()
		rospy.Subscriber(image_topic, Image, self.image_callback)

	def getNewImage(self):
		self.isNewImage = False
		self.acceptingImages = True
		timeStarted = int(time.time() * 1000)
		while(not self.isNewImage):
			timeNow = int(time.time() * 1000)
			# will time out after 10 seconds
			if(timeNow-timeStarted > 10000):
				print "Image request timed out"
				break;

	def image_callback(self, msg):
		if(self.acceptingImages):
			try:
				cv2_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
			except CvBridgeError, e:
				print e
			else:
				cv2.imwrite('camera_img.png', cv2_img)
				print "Camera Subscriber has recieved a new image"
				self.isNewImage = True
				self.acceptingImages = False

def main():
	rospy.init_node('image_listener')

	camera = CameraSubscriber()
	camera.getNewImage()
	print "Image 1 recieved"

if __name__ == '__main__':
	main()
