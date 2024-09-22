from control import Robot

robot = Robot()
positions = [(0, 0, -0.6, 0), (-1.3, 0, 0, 0), (-1.1, -0.1, 0.8, -0.4), (-0.8, 0.7, -0.5, -0.4)]
robot.move_to_home()

for position in positions:
    robot.move_all_joints(position)


# #top right
# robot.move_all_joints(0, 0, -0.6, 0)

# #Top Left
# robot.move_all_joints(-1.7, -0.2, -0.2, 0)

# #Bottom Left
# robot.move_all_joints(-1.7, 0.5, 0.2, -0.4)

# #Bottom Right
# robot.move_all_joints(-0.8, 0.7, -0.5, -0.4)


# #Depth/Center
# robot.move_all_joints(-1.0, 0.3, -0.5, -0.4)

# robot.move_all_joints(-1.3, 0.5, -0.1, 0)

# robot.move_to_home()

# robot.move_to_sleep()




robot.shutdown()