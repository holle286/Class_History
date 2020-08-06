import rospy
import baxter_interface
from moveit_python import *

from baxter_interface import CHECK_VERSION

# initialize
rospy.init_node("grip_block")

print("Getting robot state... ")
rs = baxter_interface.RobotEnable(CHECK_VERSION)
init_state = rs.state().enabled
left = baxter_interface.Gripper('left', CHECK_VERSION)
right = baxter_interface.Gripper('right', CHECK_VERSION)


def goToOrigin():
	joints = {'right_s0': 0.0, 'right_s1': .3, 'right_e0': 0,'right_e1': 1,'right_w0': 0,'right_w1': 0.2, 'right_w2': 0}
	limb.move_to_joint_positions(joints)


# rospy.init_node("moveit_python")

# movegroup = MoveGroupInterface("RobotMovement", "base_link")
# plan = PlanningSceneInterface("base_link")
# pick = PickPlaceInterface("arm", "gripper")
#
# g = Grasp()
#
# plan.addCube("my_cube", 0.1, 1, 0, 0.5)
#
# pick.pickup("my_cube", [g, ], support_name = "supporting_surface")
#
# l = PlaceLocation()
#
# p.place("my_cube", [l, ], goal_is_eef = True, support_name = "supporting_surface")

limb = baxter_interface.Limb("right")

goToOrigin()

angles = limb.joint_angles()


print angles

angles['right_s0']=0.0
angles['right_s1']=0.0
angles['right_e0']=0.0
angles['right_e1']=0.0
angles['right_w0']=0.0
angles['right_w1']=0.0
angles['right_w2']=0.0

print angles
right.calibrate();
right.open();
limb.move_to_joint_positions(angles)


joints = ['right_s0', 'right_s1', 'right_e0','right_e1', 'right_w0', 'right_w1', 'right_w2'];

table0 = {'right_s0': 0.9, 'right_s1': 0, 'right_e0': 0,'right_e1': 0.4,'right_w0': 0,'right_w1': 0.1, 'right_w2': 0}
table1 = {'right_s0': 0.9, 'right_s1': 0, 'right_e0': 0,'right_e1': 0.710,'right_w0': 0,'right_w1': 0.175, 'right_w2': 0}
limb.move_to_joint_positions(table0)
limb.move_to_joint_positions(table1)

right.close();
table2 = {'right_s0': 1.2, 'right_s1': 0, 'right_e0': 0,'right_e1': 0.610,'right_w0': 0,'right_w1': 0.175, 'right_w2': 0}
table3 = {'right_s0': 1.2, 'right_s1': 0.1, 'right_e0': 0,'right_e1': 0.550,'right_w0': 0,'right_w1': 0.175, 'right_w2': 0}
table4 = {'right_s0': 1.2, 'right_s1': -0.1, 'right_e0': 0,'right_e1': 0.35,'right_w0': 0,'right_w1': 0.175, 'right_w2': 0}
table5 = {'right_s0': 0.5, 'right_s1': -0.1, 'right_e0': 0,'right_e1': 0.35,'right_w0': 0,'right_w1': 0.175, 'right_w2': 0}
limb.move_to_joint_positions(table2)
limb.move_to_joint_positions(table3)
right.open();
limb.move_to_joint_positions(table4)
limb.move_to_joint_positions(table5)




goToOrigin()

# for i in range(0, len(joints)):
# 	flag = True
# 	while(flag):
# 		print "Moving joint " + joints[i]
# 		change = raw_input("Choose an angle (rad)\n")
#
# 		y = "y"
#
# 		if change == y:
# 			flag = False
# 		else:
# 			table[joints[i]] = float(change)
# 			limb.move_to_joint_positions(table)



# wave_1 = {'right_s0': -0.459, 'right_s1': -0.202, 'right_e0': 1.807,'right_e1': 1.714,'right_w0': -0.906,'right_w1': -1.545, 'right_w2': -0.276}
# wave_2 = {'right_s0': -0.395, 'right_s1': -0.202, 'right_e0': 1.831,'right_e1': 1.981,'right_w0': -1.979,'right_w1': -1.100, 'right_w2': -0.448}
#
# for _move in range(3):
# 	limb.move_to_joint_positions(wave_1)
# 	limb.move_to_joint_positions(wave_2)

quit()
