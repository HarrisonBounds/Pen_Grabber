from control import Robot
from alignment import Alignment
import json
import numpy as np
from scipy.spatial.transform import Rotation


filename = "test"
record = True
playback = False

robot = Robot()
video = Alignment(filename, record, playback)
video.getRGB()
ds = video.getDepth()
cd = video.clip(ds)
align = video.align()

with open("calibration.json", "r") as file:
    data = json.load(file)
    rotation_matrix = data["rotation_matrix"]  # Convert list back to NumPy array
    translation_vector = np.array(data["translation_vector"])
    
rotation_matrix = Rotation.from_matrix(rotation_matrix)
    
#Grab the pen
robot.move_to_home()
robot.open_gripper()

x, y, z = video.stream(align, cd, ds)

q = rotation_matrix.apply([x, y, z]) + translation_vector

print("Main Q: ", q)
print("Main translation: ", translation_vector)
print("Main rotation: ", rotation_matrix.as_matrix())

try:
    robot.set_ee_pose(q[0], q[1], q[2])
    robot.close_gripper()
    robot.move_to_sleep()
except:
    robot.shutdown()
    
robot.shutdown()


