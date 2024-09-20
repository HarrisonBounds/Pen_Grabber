from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
import random

class Robot():
    def __init__(self):
        
        # The robot object is what you use to control the robot
        self.robot = InterbotixManipulatorXS("px100", "arm", "gripper")
        self.joint_names = ["waist, shoulder, elbow"]
        self.mode = 's'
        robot_startup()
        
    def set_random_joints(self):
        return self.robot.arm.set_joint_positions([random.uniform(-0.8, 0.8), random.uniform(-0.5, 0.5), random.uniform(-0.4, 0.4), random.uniform(-0.4, 0.4)])
    
    
    def get_joint_positions(self):
        return self.robot.arm.get_joint_commands()
    
    def get_ee_pose(self):
        return self.robot.arm.get_ee_pose()
    
    def set_ee_pose(self, x, y, z):
        return self.robot.arm.set_ee_pose_components(x, y, z)
     
    def test(self):
        while self.mode != "q":
            self.mode = self.get_mode()
            if self.mode == "h":
                self.move_to_home()
            if self.mode == "s":
                self.move_to_sleep()
            if self.mode == "q":
                self.shutdown()
            if self.mode == "o":
                self.open_gripper
            if self.mode == "c":
                self.close_gripper()
            if self.mode == "f":
                self.move_forward(0.2)
            if self.mode == "b":
                self.move_backward(0.2)
            if self.mode == "u":
                self.move_up(0.2)
            if self.mode == "d":
                self.move_down(0.2)
            if self.mode == "r":
                self.rotate(0.2)
            
            
    def get_mode(self):
        self.mode=input("[h]ome, [s]leep, [q]uit, [o]pen, [c]lose, [f]orward, [b]ackward, [u]p, [d]own, [r]otate: ")
        return self.mode
    
    def move_to_home(self):
        self.robot.arm.go_to_home_pose()
    
    def move_to_sleep(self):
        self.robot.arm.go_to_sleep_pose()
        
    def open_gripper(self):
        self.robot.gripper.release()
        
    def close_gripper(self):
        self.robot.gripper.grasp()
        
    def move_forward(self, val):
        self.robot.arm.set_single_joint_position("shoulder", val)
        
    def move_backward(self, val):
        self.robot.arm.set_single_joint_position("shoulder", val)
    
    #negative to move up
    def move_up(self, val):
        self.robot.arm.set_single_joint_position("elbow", val)
    
    #positive move up 
    def move_down(self, val):
        self.robot.arm.set_single_joint_position("elbow", val)
        
    def rotate(self, val):
        self.robot.arm.set_single_joint_position("waist", val)
        
    def shutdown(self):
        return robot_shutdown()
    
        
        
