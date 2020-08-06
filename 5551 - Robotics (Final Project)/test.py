import cProfile, pstats
import time
import rospy
import sys
import roslib; #roslib.load_manifest("moveit_python")
import moveit_commander
import moveit_msgs.msg
import baxter_interface
import geometry_msgs.msg
# from moveit_python import PlanningSceneInterface, MoveGroupInterface
from geometry_msgs.msg import PoseStamped, PoseArray
from sensor_msgs.msg import Range

print "== Initializing Tutorial Setup =="

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)

robot = moveit_commander.RobotCommander()

scene = moveit_commander.PlanningSceneInterface()

group = moveit_commander.MoveGroupCommander("left_arm")

display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory)

print "== Waiting for RVIZ =="
rospy.sleep(10)
print "== Starting =="

print "  - Reference Frame: %s" % group.get_planning_frame()
print "  - Reference Frame: %s" % group.get_end_effector_link()
print "== Robot Groups =="
print robot.get_group_names()
print ""
print "== Robot State =="
print robot.get_current_state()
print "=================="





# # Define initial parameters.
# rospy.init_node('pnp', anonymous=True)
# # Initialize the move_group API.

# # Connect the arms to the move group.
# # both_arms = moveit_commander.MoveGroupCommander('both_arms')
# right_arm = moveit_commander.MoveGroupCommander('right_arm')
# # left_arm = moveit_commander.MoveGroupCommander('left_arm')
# # Allow replanning to increase the odds of a solution.
# right_arm.allow_replanning(True)
# left_arm.allow_replanning(True)
# # Set the arms reference frames.
# right_arm.set_pose_reference_frame('base')
# left_arm.set_pose_reference_frame('base')
# # Create baxter_interface limb instance.
# leftarm = baxter_interface.limb.Limb('left')
# rightarm = baxter_interface.limb.Limb('right')
# # Initialize the planning scene interface.
# p = PlanningSceneInterface("base")
# # Create baxter_interface gripper instance.
# leftgripper = baxter_interface.Gripper('left')
# rightgripper = baxter_interface.Gripper('right')
# leftgripper.calibrate()
# rightgripper.calibrate()
# leftgripper.open()
# rightgripper.open()


if __name__=='__main__':
    try:
        # rospy.init_node('pnp', anonymous=True)
        # measure_zero_point()
		measureZeroPoint();
    except rospy.ROSInterruptException:
        pass
