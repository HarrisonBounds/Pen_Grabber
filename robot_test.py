from control import Robot

robot = Robot()
robot.move_to_sleep()
robot.set_ee_pose(0.15, 0.02, 0.006)

robot.shutdown()