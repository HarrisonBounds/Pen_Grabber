from alignment import Alignment
from control import Robot
from scipy.spatial.transform import Rotation
import numpy as np
import json

#MAIN
filename = "test_recording"
calibration_file = "calibration.txt"
record = True
playback = False
streaming = True
moved = False
num_calibration_points = 15
total_cam_x, total_cam_y, total_cam_z, total_rob_x, total_rob_y, total_rob_z  = [], [], [], [], [], []
set_cam_centroids, set_rob_centroids = [], []

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

for i in range(num_calibration_points):
    robot.set_random_joints()
    alignment.stream(align, cd, ds)

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

translation = [rob_centroid[0]-cam_centroid[0], rob_centroid[1]-cam_centroid[1], rob_centroid[2]-cam_centroid[2]]
rotation, rmsd = Rotation.align_vectors(set_rob_centroids, set_cam_centroids)
# rp = np.matmul(rotation.as_matrix(), cam_centroid.T)
# translation = np.subtract(rob_centroid, rp)

with open("calibration.txt", "a") as file:
    file.write(f"Rotation: {rotation.as_matrix()}\n")
    file.write(f"Translation Vector: x: {translation[0]}, y: {translation[1]}, z: {translation[2]}\n")


            
data = {
    "rotation_matrix": rotation.as_matrix().tolist(),
    "translation_vector": translation
} 

with open("calibration.json", "w") as file:
    json.dump(data, file)
    

#x: 0.22425638935305184, y: -0.05289413087599007, z: 0.1690208030825802
q = (rotation.apply([0.22, -0.05, 0.16])) + translation

print("Calibration Q: ", q)
print("Calibration translation: ", translation)
print("Calibration rotation: ", rotation.as_matrix())

#print("Q: ", q)
    
robot.move_to_sleep()
robot.open_gripper()
robot.close_gripper() 
robot.shutdown()
alignment.cleanup()






