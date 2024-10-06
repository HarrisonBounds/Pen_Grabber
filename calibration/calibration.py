from alignment import Alignment
from control import Robot
from scipy.spatial.transform import Rotation
import numpy as np
import json
import random 

#MAIN
filename = "test_recording"
calibration_file = "calibration.txt"
record = True
playback = False
streaming = True
moved = False
total_cam_x, total_cam_y, total_cam_z, total_rob_x, total_rob_y, total_rob_z  = [], [], [], [], [], []
set_cam_centroids, set_rob_centroids = [], []

calibration_positions = [(0, 0, -0.6, 0), (-1.3, 0, 0, 0), (-1.1, -0.1, 0.8, -0.4), (-0.8, 0.7, -0.5, -0.4), (random.uniform(-1.5, -0.7), 0, 0, 0), (random.uniform(-1.5, -0.4), random.uniform(-0.4, 0.4), 0, 0), (-0.5, 0.5, -0.2, -0.3), (0, 0, 0, 0)]
num_calibration_points = len(calibration_positions)

alignment = Alignment(filename, record, playback)
robot = Robot()

alignment.getRGB()
ds = alignment.getDepth()
cd = alignment.clip(ds)
align = alignment.align()

with open("calibration.txt", "w") as file:
    file.write("Calibration for Robot and Camera\n\n")
    

robot.move_to_home()
robot.open_gripper()
robot.close_gripper()

for i, position in enumerate(calibration_positions):
    robot.move_all_joints(position)
    
    cam_x, cam_y, cam_z = alignment.stream(align, cd, ds)
    rob_x, rob_y, rob_z = robot.get_ee_pose()[0][-1], robot.get_ee_pose()[1][-1], robot.get_ee_pose()[2][-1]

    with open("calibration.txt", "a") as file:
        file.write(f"Calibration Robot Position {i+1}: x: {rob_x}, y: {rob_y}, z: {rob_z}\n")
        file.write(f"Calibration Camera Position {i+1}: x: {cam_x}, y: {cam_y}, z: {cam_z} \n\n")

    total_cam_x.append(cam_x)
    total_cam_y.append(cam_y)
    total_cam_z.append(cam_z)
    total_rob_x.append(rob_x)
    total_rob_y.append(rob_y)
    total_rob_z.append(rob_z)

    
cam_centroid = [(1 / num_calibration_points) * sum(total_cam_x), (1 / num_calibration_points) * sum(total_cam_y), (1 / num_calibration_points) * sum(total_cam_z)]
rob_centroid = [(1 / num_calibration_points) * sum(total_rob_x), (1 / num_calibration_points) * sum(total_rob_y), (1 / num_calibration_points) * sum(total_rob_z)]

for i in range(num_calibration_points):
    cam_norm_x = total_cam_x[i] - cam_centroid[0]
    cam_norm_y = total_cam_y[i] - cam_centroid[1]
    cam_norm_z = total_cam_z[i] - cam_centroid[2]
    
    rob_norm_x = total_rob_x[i] - rob_centroid[0]
    rob_norm_y = total_rob_y[i] - rob_centroid[1]
    rob_norm_z = total_rob_z[i] - rob_centroid[2]
    
    set_cam_centroids.append((cam_norm_x, cam_norm_y, cam_norm_z))
    set_rob_centroids.append((rob_norm_x, rob_norm_y, rob_norm_z))

rotation, rmsd = Rotation.align_vectors(set_rob_centroids, set_cam_centroids)
translation = rob_centroid - rotation.apply(cam_centroid)

with open("calibration.txt", "a") as file:
    file.write(f"Rotation: {rotation.as_matrix()}\n")
    file.write(f"Translation Vector: x: {translation[0]}, y: {translation[1]}, z: {translation[2]}\n")
            
data = {
    "rotation_matrix": rotation.as_matrix().tolist(),
    "translation_vector": translation.tolist()
} 

with open("calibration.json", "w") as file:
    json.dump(data, file)
    

robot.move_to_sleep()
robot.open_gripper()
robot.close_gripper() 
robot.shutdown()
alignment.cleanup()






