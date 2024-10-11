# RealSense Robot Alignment and Control : Pen Grabber Robot

## Overview

This project integrates Intel RealSense cameras with an Interbotix robotic manipulator to perform precise alignment and object manipulation tasks. Utilizing computer vision techniques with OpenCV and leveraging RealSense's depth sensing capabilities, the system can detect objects, calculate their positions in three-dimensional space, and control the robot arm to interact with them accurately.

## Features

- **RealSense Integration**: Captures color and depth data using Intel RealSense cameras.
- **Computer Vision Processing**: Utilizes OpenCV for image processing tasks such as HSV masking, contour detection, and adaptive thresholding.
- **Robotic Control**: Controls an Interbotix Manipulator XS robot arm, allowing for precise movements and gripper operations.
- **Calibration Support**: Applies calibration data to align the camera and robot coordinate systems for accurate positioning.
- **Interactive Control**: Provides a command-line interface to control the robot's movements and gripper.
- **Unit Testing**: Enables unit testing of the robot through command-line interactions to ensure reliable operations.
- **Pen Manipulation**: Capable of detecting and grasping objects like pens using depth information and precise robotic control.

## Table of Contents

- Overview
- Features
- Table of Contents
- Usage
  - Running the Program
  - Unit Testing the Robot
  - Calculating Calibration Points
  - Grabbing the Pen
- OpenCV Integration
- Code Structure

## Usage

### Running the Program

To start the alignment and control process, execute the main script. The script initializes the RealSense camera, starts the robot arm, captures and processes video frames to detect objects, calculates their 3D positions, and moves the robot arm to interact with detected objects.

### Unit Testing the Robot

Before performing actual tasks, it's crucial to ensure that the robot operates as expected. This project provides a command-line interface for unit testing the robot's functionalities. You can test individual joint movements, gripper operations, and end-effector positioning without engaging in full-scale object manipulation. This helps in verifying the robot's responsiveness and accuracy.

**Example Commands:**

- **Move to Home Position**:  
  Enter `h` to move the robot arm to its home position.
  
- **Move to Sleep Position**:  
  Enter `s` to move the robot arm to its sleep position.
  
- **Open Gripper**:  
  Enter `o` to open the robot's gripper.
  
- **Close Gripper**:  
  Enter `c` to close the robot's gripper.
  
- **Move Forward**:  
  Enter `f` followed by a value to move the shoulder joint forward.
  
- **Move Backward**:  
  Enter `b` followed by a value to move the shoulder joint backward.
  
- **Move Up**:  
  Enter `u` followed by a value to move the elbow joint up.
  
- **Move Down**:  
  Enter `d` followed by a value to move the elbow joint down.
  
- **Rotate Waist**:  
  Enter `r` followed by a value to rotate the waist joint.

### Calculating Calibration Points

Accurate calibration is essential for aligning the camera's coordinate system with that of the robot. This ensures that the 3D positions calculated from depth data accurately correspond to real-world coordinates for robotic manipulation.

**Steps to Calculate Calibration Points:**

1. **Capture Calibration Images**:  
   Use the RealSense camera to capture images of known reference points in the environment.

2. **Determine Rotation and Translation**:  
   Analyze the captured images to compute the rotation matrix and translation vector that align the camera's view with the robot's coordinate system.

3. **Store Calibration Data**:  
   Save the calculated rotation matrix and translation vector in a calibration.json file. This file is used by the system to apply the necessary transformations during operation.

**Example calibration.json:**

{
    "rotation_matrix": [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ],
    "translation_vector": [0.0, 0.0, 0.0]
}

Ensure that the calibration data accurately reflects the physical setup to maintain precision in robotic movements.

### Grabbing the Pen

One of the primary functionalities of this system is to detect and manipulate objects, such as grabbing a pen. The process involves several steps:

1. **Object Detection**:  
   The system processes the color and depth data to identify the target object based on color masks and contour detection.

2. **3D Position Calculation**:  
   Once the object is detected, its centroid is calculated, and the corresponding 3D coordinates are determined using the depth information and calibration data.

3. **Robot Arm Movement**:  
   The robot arm is commanded to move its end-effector to the calculated 3D position. The gripper is then closed to grasp the pen.

4. **Feedback and Adjustment**:  
   Visual feedback is provided through OpenCV windows, displaying the detected object, its position, and the robot's movements. This allows for real-time monitoring and adjustments if necessary.

**Workflow Example:**

- The system detects a pen in the camera's view using HSV masking and contour detection.
- It calculates the pen's 3D coordinates relative to the robot.
- The robot arm moves to the pen's location.
- The gripper closes to grasp the pen.
- The robot lifts the pen and moves it to the designated location.

## OpenCV Integration

OpenCV is a core component of this project, providing robust computer vision capabilities that facilitate object detection, image processing, and visual feedback. Key OpenCV functionalities used include:

- **HSV Masking**:  
  Converts RGB images to HSV color space to create masks that isolate specific color ranges. This is essential for detecting objects based on color.

- **Contour Detection**:  
  Identifies the outlines of detected objects within the masked images. Contours are used to find the largest object, calculate its centroid, and determine its position.

- **Adaptive Thresholding**:  
  Applies adaptive thresholding techniques to convert grayscale images to binary images, enhancing feature detection under varying lighting conditions.

- **Trackbars for Parameter Tuning**:  
  Implements interactive trackbars that allow users to adjust HSV thresholds in real-time. This facilitates fine-tuning the object detection process based on different environments and lighting.

- **Visual Feedback**:  
  Renders processed images with overlays such as contours and centroids, providing visual confirmation of detection and robotic actions.

**Example OpenCV Operations:**

- **Creating a Mask**:
  
  The system creates a mask to isolate the color range of the target object:
  
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      mask = cv2.inRange(hsv, lower, upper)

- **Finding Contours**:
  
  After masking, contours of the objects are detected:
  
      contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      largest_contour = max(contours, key=cv2.contourArea)

- **Drawing Contours and Centroids**:
  
  Visual indicators are drawn on the image to show detection:
  
      cv2.drawContours(color_image, largest_contour, -1, (0, 255, 0), 3)
      cv2.circle(color_image, (cx, cy), 5, (0, 0, 255), -1)

These OpenCV operations are integrated seamlessly with the robot control logic to enable accurate and responsive manipulation based on visual input.

## Code Structure

- **Alignment Class**  
  Handles RealSense camera streams, image processing, and coordinate conversions. It manages the capture of RGB and depth data, applies image processing techniques, and computes 3D positions of detected objects.

- **Robot Class**  
  Manages robot control, including joint movements, gripper operations, and end-effector positioning. It provides methods to move individual joints, control the gripper, and execute complex movement sequences based on input commands.

- **Trackbar Module**  
  Implements the Trackbar class for creating and managing OpenCV trackbars used in HSV masking. This class facilitates real-time adjustment of color thresholds, enhancing the flexibility and adaptability of the object detection process.

- **Main Script**  
  Orchestrates the initialization of the camera and robot, processes frames, and executes robot movements based on visual input. It handles the main workflow, including calibration, object detection, and robotic manipulation.

- **Calibration Data (calibration.json)**  
  Stores calibration data including the rotation matrix and translation vector necessary for aligning camera and robot coordinates. This file is essential for accurate 3D positioning and robotic control.


