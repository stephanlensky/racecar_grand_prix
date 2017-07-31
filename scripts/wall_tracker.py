#!/usr/bin/python
import rospy
import numpy as np
import time
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32

class wallController:
	def __init__(self):
		# Subscription and Publication
		rospy.Subscriber("/scan", LaserScan, self.wall_controller)
		self.cmd_pub = rospy.Publisher("/wall_error", Float32, queue_size=10)
		
		# Desired distance from the wall
		self.d_des = 0.4 #left_.4 right_.9
		self.speed_des = 0

		# Controller gains
		self.Kp = .04
		self.Kd = .03

		# Error variables
		self.error = 0

		# Right(0) or left(1)
		self.wall_orientation = 0

	def wall_controller(self, scan):

 		smallestDistance = 300

		if self.wall_orientation == 0:
			a = 172
			b = 300
		elif self.wall_orientation == 1:
			a = 780
			b = 908

		for i in range(a, b):
			if scan.ranges[i] < smallestDistance:
				smallestDistance = scan.ranges[i]
 				smallestIndex = i
		self.error = self.d_des - smallestDistance
		print 'error: ', self.error
		self.cmd_pub.publish(self.error)

if __name__ == "__main__":
    rospy.init_node("wall_controller")
    node = wallController()
    rospy.spin()