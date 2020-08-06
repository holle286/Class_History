import argparse
import struct
import sys

import rospy
import baxter_interface
from baxter_interface import CHECK_VERSION

from geometry_msgs.msg import (
	PoseStamped,
	Pose,
	Point,
	Quaternion,
)
from std_msgs.msg import Header

from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)

def goToOrigin(limb):
	joints = {'right_s0': 0.0, 'right_s1': .45, 'right_e0': 0,'right_e1': 1,'right_w0': 0,'right_w1': 0.2, 'right_w2': 0}
	limb.move_to_joint_positions(joints)

# Solves ik
def solveIK(arm, x1, y1, z1, q1, q2, q3, q4):

	ns = "ExternalTools/" + arm + "/PositionKinematicsNode/IKService"
	iksvc = rospy.ServiceProxy(ns, SolvePositionIK)
	ikreq = SolvePositionIKRequest()
	hdr = Header(stamp=rospy.Time.now(), frame_id='base')

	pose = PoseStamped(
		header=hdr,
		pose=Pose(
			position=Point(
				x=x1,
				y=y1,
				z=z1,
			),
			orientation=Quaternion(
				x=q1,
				y=q2,
				z=q3,
				w=q4,
			),
		)
	)

	ikreq.pose_stamp.append(pose)
	try:
		rospy.wait_for_service(ns, 5.0)
		resp = iksvc(ikreq)
	except (rospy.ServiceException, rospy.ROSException), e:
		rospy.logerr("Service call failed: %s" % (e,))
		return 1

    # Check if result valid, and type of seed ultimately used to get solution
    # convert rospy's string representation of uint8[]'s to int's
	resp_seeds = struct.unpack('<%dB' % len(resp.result_type), resp.result_type)
	if (resp_seeds[0] != resp.RESULT_INVALID):
		seed_str = {
					ikreq.SEED_USER: 'User Provided Seed',
					ikreq.SEED_CURRENT: 'Current Joint Angles',
					ikreq.SEED_NS_MAP: 'Nullspace Setpoints',
					}.get(resp_seeds[0], 'None')
		print("SUCCESS - Valid Joint Solution Found from Seed Type: %s" % (seed_str,))
		# Format solution into Limb API-compatible dictionary
		limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
		print "\nIK Joint Solution:\n", limb_joints
		return limb_joints
	else:
		print("INVALID POSE - No Valid Joint Solution Found.")

	return None

def main():

    # arg_fmt = argparse.RawDescriptionHelpFormatter
    # parser = argparse.ArgumentParser(formatter_class=arg_fmt,
    #                                  description=main.__doc__)
    # parser.add_argument(
    #     '-l', '--limb', choices=['left', 'right'], required=True,
    #     help="the limb to test"
    # )
    # args = parser.parse_args(rospy.myargv()[1:])

	print("Getting robot state... ")
	rospy.init_node("IKSolver")
	rs = baxter_interface.RobotEnable(CHECK_VERSION)
	init_state = rs.state().enabled
	limb = baxter_interface.Limb("right")
	right = baxter_interface.Gripper('right', CHECK_VERSION)

    # return ik_test(args.limb)

	goToOrigin(limb)
	current_pose = limb.endpoint_pose()
	print current_pose

	print limb.joint_angles()

	running = True
	while(running):
			x = raw_input("X Value?\n")
			y = raw_input("Y Value?\n")
			z = raw_input("Z Value?\n")

			joints = solveIK('right', float(x), float(y), float(z), current_pose['orientation'].x, current_pose['orientation'].y, current_pose['orientation'].z, current_pose['orientation'].w);

			if(x == " " or y == " " or z == " "):
				running = False
			else:
				if(joints):
					print "moving"
					limb.move_to_joint_positions(joints)


if __name__ == '__main__':
	main()
