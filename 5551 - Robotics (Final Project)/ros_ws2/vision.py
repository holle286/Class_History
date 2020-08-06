import rospy
import baxter_interface
from IKSolver import solveIK
from Camera import CameraSubscriber
from baxter_interface import CHECK_VERSION
from RobotVision import SearchTool
from Hanoi import Hanoi
import time

rospy.init_node("vision")

print("Getting robot state... ")
rs = baxter_interface.RobotEnable(CHECK_VERSION)
init_state = rs.state().enabled
rightArm = baxter_interface.Limb("right")
leftArm = baxter_interface.Limb("left")
leftGripper = baxter_interface.Gripper('left', CHECK_VERSION)
rightGripper = baxter_interface.Gripper('right', CHECK_VERSION)
camera = CameraSubscriber()

hanoi = Hanoi(3)

searchTool = SearchTool("camera_img.png")


def goToOrigin():
	rightJoints = {'right_s0': 0.0, 'right_s1': .3, 'right_e0': 0,'right_e1': 1,'right_w0': 0,'right_w1': 0.2, 'right_w2': 0}
	leftJoints = {'left_s0': 0.0, 'left_s1': .3, 'left_e0': 0,'left_e1': 1,'left_w0': 0,'left_w1': 0.2, 'left_w2': 0}
	rightArm.move_to_joint_positions(rightJoints)
	leftArm.move_to_joint_positions(leftJoints)

def calibrateGrippers():
	rightGripper.calibrate();


def topPose():
	pos = solveIK('right',0.7, -0.4, -0.1, 0.44, 0.9, 0, 0);
	rightArm.move_to_joint_positions(pos);

def setupInitialPose():
	pos1 = solveIK('right',0.4, -0.4, 0, 0.44, 0.9, 0, 0);
	# pos2 = solveIK('right',0.7, -0.2, -0.2, 0.44, 0.9, 0, 0);
	# pos2 = solveIK('right',0.7, -0.2, 0.2, 0.44, 0.9, 0, 0);
	pos3 = solveIK('right',0.7, -0.4, -0.1, 0.44, 0.9, 0, 0);

	pos = [pos1, pos3]

	for i in range(len(pos)):
		if(pos[i]):
			rightArm.move_to_joint_positions(pos[i]);
		else:
			print "invalid position"

def rotateGripper(theta):
	pose = rightArm.joint_angles()
	pose['right_w2'] = pose['right_w2'] + theta
	rightArm.move_to_joint_positions(pose);

def moveTo(stack1):
		aligned = False

		while not aligned:
			camera.getNewImage()
			#align camera with board

			colors = [hanoi.getStackTopColor(0), hanoi.getStackTopColor(1), hanoi.getStackTopColor(2)] # get color of stacks
			print colors
			pixelPoints = []

			for i in xrange(3):
				pixelArray = searchTool.DBScan(colors[i])
				print i, " ", pixelArray
				for j in xrange(len(pixelArray)):
					pixelPoints += [pixelArray[j]]
				if len(pixelPoints) > 1:
					break

			# [((x1,y1),r1), ((x2,y2),r2)] = searchTool.DBScan("gold")
			print pixelPoints
			if len(pixelPoints) < 2:
				print "not enough points to reorient"
				continue

			[((x1,y1),r1), ((x2,y2),r2)] = [pixelPoints[0], pixelPoints[1]]

			theta = searchTool.calculateAngle((x1,y1), (x2, y2))
			print theta
			rotateGripper(theta)

			#find position
			camera.getNewImage()

			current_pos = rightArm.endpoint_pose()

			(cx, cy, cz) = current_pos['position']

			pixelArray = searchTool.DBScan(hanoi.getStackTopColor(stack1))
			point_x = None
			point_y = None
			point_r = None

			if len(pixelArray) > 0:
				((point_x, point_y), point_r) = pixelArray[0]
				print ((point_x, point_y), point_r)
			else:
				print "point not recognized"
				exit()

			target_y = float(cy - ((point_x - 364) * 0.000432))

			if point_x < 370+10 and point_x > 370-10:
				aligned = True
				z_distance = (38-point_r)*-0.0105
				pos3 = solveIK('right', cx, target_y, z_distance, 0.44, 0.9, 0, 0);
				rightArm.move_to_joint_positions(pos3);
			else:
				# target_y = float(cy - ((point_x - 364) * 0.000432))

				print " ", target_y, " ", cz

				target_pos = solveIK('right', cx, target_y, cz, 0.44, 0.9, 0, 0);
				rightArm.move_to_joint_positions(target_pos);

def moveToDrop(stack1):
		aligned = False
		adjustment = 0

		while adjustment < 3:
			camera.getNewImage()
			#align camera with board

			colors = [hanoi.getStackTopColor(0), hanoi.getStackTopColor(1), hanoi.getStackTopColor(2)] # get color of stacks
			print colors
			pixelPoints = []

			for i in xrange(3):
				pixelArray = searchTool.DBScan(colors[i])
				print i, " ", pixelArray
				for j in xrange(len(pixelArray)):
					pixelPoints += [pixelArray[j]]
				if len(pixelPoints) > 1:
					break

			# [((x1,y1),r1), ((x2,y2),r2)] = searchTool.DBScan("gold")
			print pixelPoints
			if len(pixelPoints) < 2:
				print "not enough points to reorient"
				continue

			[((x1,y1),r1), ((x2,y2),r2)] = [pixelPoints[0], pixelPoints[1]]

			theta = searchTool.calculateAngle((x1,y1), (x2, y2))
			print theta
			rotateGripper(theta)

			#find position
			camera.getNewImage()

			current_pos = rightArm.endpoint_pose()

			(cx, cy, cz) = current_pos['position']

			pixelArray = searchTool.DBScan(hanoi.getStackTopColor(stack1))
			point_x = None
			point_y = None
			point_r = None

			if len(pixelArray) > 0:
				((point_x, point_y), point_r) = pixelArray[0]
				print ((point_x, point_y), point_r)
			else:
				print "point not recognized"
				exit()

			target_y = float(cy - ((point_x - 364) * 0.000432))

			# if point_x < 370+15 and point_x > 370-15:
			if adjustment == 2:
				z_distance = (38-point_r)*-0.010
				pos3 = solveIK('right', cx, target_y, z_distance, 0.44, 0.9, 0, 0);
				rightArm.move_to_joint_positions(pos3);
			else:
				# target_y = float(cy - ((point_x - 364) * 0.000432))
				print " ", target_y, " ", cz
				target_pos = solveIK('right', cx, target_y, cz, 0.44, 0.9, 0, 0);
				rightArm.move_to_joint_positions(target_pos)
			adjustment += 1

def main():
	print "vision test"
	# goToOrigin()
	print "origin set"
	calibrateGrippers()
	print "calibrating grippers"
	setupInitialPose()

	time.sleep(0.5)
	camera.getNewImage()
	hanoi.printState()

	# rotate the arm
	# [((x1,y1),r1), ((x2,y2),r2)] = searchTool.DBScan("gold")
	#
	# theta = searchTool.calculateAngle((x1,y1), (x2, y2))
	# print theta
	# rotateGripper(theta)
	#
	# initial_pos = rightArm.endpoint_pose()

	# move(stack1, stack2)

	# stack1 = 0
	# stack2 = 2
	#
	# while not aligned:
	# 	camera.getNewImage()
	# 	#align camera with board
	#
	# 	colors = [hanoi.getStackTopColor(0), hanoi.getStackTopColor(1), hanoi.getStackTopColor(2)] # get color of stacks
	# 	print colors
	# 	pixelPoints = []
	#
	# 	for i in xrange(3):
	# 		pixelArray = searchTool.DBScan(colors[i])
	# 		print i, " ", pixelArray
	# 		for j in xrange(len(pixelArray)):
	# 			pixelPoints += [pixelArray[j]]
	# 		if len(pixelPoints) > 1:
	# 			break
	#
	# 	# [((x1,y1),r1), ((x2,y2),r2)] = searchTool.DBScan("gold")
	# 	print pixelPoints
	# 	if len(pixelPoints) < 2:
	# 		print "not enough points to reorient"
	# 		continue
	#
	# 	[((x1,y1),r1), ((x2,y2),r2)] = [pixelPoints[0], pixelPoints[1]]
	#
	# 	theta = searchTool.calculateAngle((x1,y1), (x2, y2))
	# 	print theta
	# 	rotateGripper(theta)
	#
	# 	#find position
	# 	camera.getNewImage()
	#
	# 	current_pos = rightArm.endpoint_pose()
	#
	# 	(cx, cy, cz) = current_pos['position']
	#
	# 	pixelArray = searchTool.DBScan(hanoi.getStackTopColor(stack1))
	# 	point_x = None
	# 	point_y = None
	# 	point_r = None
	#
	# 	if len(pixelArray) > 0:
	# 		((point_x, point_y), point_r) = pixelArray[0]
	# 		print ((point_x, point_y), point_r)
	# 	else:
	# 		print "point not recognized"
	# 		exit()
	#
	# 	# pos4 = solveIK('right', target_x, target_y, target_z, 0.44, 0.9, 0, 0);
	#
	# 	# pos4 = solveIK('right',0.705, -0.47, -.1, 0.44, 0.9, 0, 0);
	# 	# pose = rightArm.joint_angles()
	# 	# rightArm.move_to_joint_positions(pos4);
	#
	# 	# rightGripper.close()
	# 	# rightArm.move_to_joint_positions(pose);
	#
	# 	if point_x < 370+5 and point_x > 370-5:
	# 		aligned = True
	# 		z_distance = (38-point_r)*-0.0105
	# 		pos3 = solveIK('right', cx, target_y, z_distance, 0.44, 0.9, 0, 0);
	# 		rightArm.move_to_joint_positions(pos3);
	# 	else:
	# 		target_y = float(cy - ((point_x - 364) * 0.000432))
	# 		# target_y = float(cy - ((point_y - 63) * 0.0022))
	# 		# target_x = float(cx - ((point_y - 134) * -0.01666))
	# 		print " ", target_y, " ", cz
	#
	# 		target_pos = solveIK('right', cx, target_y, cz, 0.44, 0.9, 0, 0);
	# 		rightArm.move_to_joint_positions(target_pos);

		# print ((point_x, point_y), point_r)
		# if point_x < 134+5 and point_x > 134-5 and point_y < 364+5 and point_y > 364-5:
		# 	aligned = True
		# else:
		# 	target_x = float(cx - ((point_x - 134) * -0.01666))
		# 	# target_y = float(cy - ((point_y - 63) * 0.0022))
		# 	target_y = float(cy - ((point_y - 364) * 0.000432))
		# 	print target_x," ", target_y, " ", cz
		#
		# 	target_pos = solveIK('right', target_x, target_y, cz, 0.44, 0.9, 0, 0);
		# 	rightArm.move_to_joint_positions(target_pos);

	moveTo(0)
	rightGripper.close()
	topPose()
	moveToDrop(2)
	rightGripper.open()
	topPose()

	exit()
	aligned = False


	while not aligned:
		camera.getNewImage()
		#align camera with board

		colors = [hanoi.getStackTopColor(0), hanoi.getStackTopColor(1), hanoi.getStackTopColor(2)] # get color of stacks
		print colors
		pixelPoints = []

		for i in xrange(3):
			pixelArray = searchTool.DBScan(colors[i])
			print i, " ", pixelArray
			for j in xrange(len(pixelArray)):
				pixelPoints += [pixelArray[j]]
			if len(pixelPoints) > 1:
				break

		# [((x1,y1),r1), ((x2,y2),r2)] = searchTool.DBScan("gold")
		print pixelPoints
		if len(pixelPoints) < 3:
			print "not enough points to reorient"
			continue

		[((x1,y1),r1), ((x2,y2),r2)] = [pixelPoints[0], pixelPoints[1]]

		theta = searchTool.calculateAngle((x1,y1), (x2, y2))
		print theta
		rotateGripper(theta)

		#find position
		camera.getNewImage()

		current_pos = rightArm.endpoint_pose()

		(cx, cy, cz) = current_pos['position']

		pixelArray = searchTool.DBScan(hanoi.getStackTopColor(stack2))
		point_x = None
		point_y = None
		point_r = None
		#
		if len(pixelArray) == 1:
			((point_x, point_y), point_r) = pixelArray[0]
			print ((point_x, point_y), point_r)

		if len(pixelArray) > 1:
			((point_x, point_y), point_r) = pixelPoints[stack2]

		else:
			print "point not recognized"
			exit()

		# pos4 = solveIK('right', target_x, target_y, target_z, 0.44, 0.9, 0, 0);

		# pos4 = solveIK('right',0.705, -0.47, -.1, 0.44, 0.9, 0, 0);
		# pose = rightArm.joint_angles()
		# rightArm.move_to_joint_positions(pos4);

		# rightGripper.close()
		# rightArm.move_to_joint_positions(pose);

		if point_x < 370+5 and point_x > 370-5:
			aligned = True
			z_distance = (38-point_r)*-0.0105
			pos3 = solveIK('right', cx, target_y, z_distance, 0.44, 0.9, 0, 0);
			rightArm.move_to_joint_positions(pos3);
		else:
			target_y = float(cy - ((point_x - 364) * 0.000432))
			# target_y = float(cy - ((point_y - 63) * 0.0022))
			# target_x = float(cx - ((point_y - 134) * -0.01666))
			print " ", target_y, " ", cz

			target_pos = solveIK('right', cx, target_y, cz, 0.44, 0.9, 0, 0);
			rightArm.move_to_joint_positions(target_pos);

	exit()

	print (cx, cy, cz)


	target_x = float(cx - ((point_x - 385) * -0.0002))
	target_y = float(cy - ((point_y - 63) * -0.0022))
	target_z = float((38-point_r)*-0.012)
	print target_x, target_y, target_z
	pos4 = solveIK('right', target_x, target_y, target_z, 0.44, 0.9, 0, 0);

	# pos4 = solveIK('right',0.725, -0.495, -0.185, 0.44, 0.9, 0, 0);
	pose = rightArm.joint_angles()
	rightArm.move_to_joint_positions(pos4);

	rightGripper.close()
	rightArm.move_to_joint_positions(pose);



	z_distance = (38-point_r)*-0.0076
	# pos3 = solveIK('right',0.8, -0.1, z_distance, 0.44, 0.9, 0, 0);
	# rightArm.move_to_joint_positions(pos3);
	rightGripper.close()


	# # rotate the arm
	# [((x1,y1),r1), ((x2,y2),r2)] = searchTool.DBScan("pink")
	#
	# theta = searchTool.calculateAngle((x1,y1), (x2, y2))
	# print theta
	# rotateGripper(theta)
	# camera.getNewImage()
	#
	# [((point_x, point_y), point_r)] = searchTool.DBScan("blue")
	# print (point_x, " ", point_y)





if __name__ == '__main__':
	main()
	exit()
