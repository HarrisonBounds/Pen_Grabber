from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup

class Robot():
    def __init__(self):
        
        # The robot object is what you use to control the robot
        self.robot = InterbotixManipulatorXS("px100", "arm", "gripper")
        self.joint_names = ["waist, shoulder, elbow"]
        self.mode = 'h'
        robot_startup()
        
    def calibration(self):
        mode = self.get_mode()
        
        while mode != "q":
            if mode == "h":
                self.move_to_home()
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
        
    def shutdown(self,val):
        return robot_shutdown()
        
        
        
