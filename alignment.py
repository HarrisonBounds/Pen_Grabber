import pyrealsense2 as rs
import numpy as np
import cv2
from trackbar import Trackbar

class Alignment:
    def __init__(self, fn, record, playback):
        
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        
        self.pipeline_wrapper = rs.config()
        
        self.pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        self.pipeline_profile = self.config.resolve(self.pipeline_wrapper)
        self.device = self.pipeline_profile.get_device()
        self.device_product_line = str(self.device.get_info(rs.camera_info.product_line))
        self.clipping_distance_meters = 1 #In meters

        filename = f'.gitignore/recordings/{fn}'
        
        if record:
            self.config.enable_record_to_file(filename)
        if playback:
            self.config.enable_device_from_file(filename)
        
        #Trackbar
        self.trackbar = Trackbar()
        self.mask_image_name = 'HSV'
        cv2.namedWindow(self.mask_image_name)
        
        cv2.createTrackbar(self.trackbar.low_H_name, self.mask_image_name, self.trackbar.low_H, self.trackbar.max_value_H, self.trackbar_filler)
        cv2.createTrackbar(self.trackbar.high_H_name, self.mask_image_name, self.trackbar.high_H, self.trackbar.max_value_H, self.trackbar_filler)
        
        cv2.createTrackbar(self.trackbar.low_S_name, self.mask_image_name, self.trackbar.low_S, self.trackbar.max_value, self.trackbar_filler)
        cv2.createTrackbar(self.trackbar.high_S_name, self.mask_image_name, self.trackbar.high_S, self.trackbar.max_value, self.trackbar_filler)
        
        cv2.createTrackbar(self.trackbar.low_V_name, self.mask_image_name, self.trackbar.low_V, self.trackbar.max_value, self.trackbar_filler)
        cv2.createTrackbar(self.trackbar.high_V_name, self.mask_image_name, self.trackbar.high_V, self.trackbar.max_value, self.trackbar_filler)
        
    def trackbar_filler():
        pass
        
    def getRGB(self):
        found_rgb = False
        for s in self.device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        
    def getDepth(self):
        profile = self.pipeline.start(self.config)
        # Getting the depth sensor's depth scale (see rs-align example for explanation)
        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        print("Depth Scale is: " , depth_scale)
        
        return depth_scale
        
    def clip(self, depth_scale):
        clipping_distance = self.clipping_distance_meters / depth_scale
        return clipping_distance
    
    def align(self):
        align_to = rs.stream.color
        align = rs.align(align_to)
        return align
    
    
    def convert_to_HSV(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lower_H = self.trackbar.get_low_H_Pos(self.mask_image_name)
        upper_H = self.trackbar.get_high_H_Pos(self.mask_image_name)
        
        lower_S = self.trackbar.get_low_S_Pos(self.mask_image_name)
        upper_S = self.trackbar.get_high_S_Pos(self.mask_image_name)
        
        lower_V = self.trackbar.get_low_V_Pos(self.mask_image_name)
        upper_V = self.trackbar.get_high_V_Pos(self.mask_image_name)
        
        #Black and White
        lower = np.array([112, 76, 65])
        upper= np.array([160, 255, 255])
        
        
        lower = np.array(lower)
        upper = np.array(upper)
        
        mask = cv2.inRange(hsv, lower, upper)

        #res = cv2.bitwise_and(frame, frame, mask=mask)
        
        return mask
    
    def adaptive_thresholding(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        adaptive_threshold = cv2.adaptiveThreshold(gray_frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        return adaptive_threshold
    
    def binary_thresholding(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray_frame,127,255,cv2.THRESH_BINARY)
        return thresh
    
    def findContour(self, frame):
        #gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(frame, 150, 255, 0)
        
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)  # Find the largest contour
            
            M = cv2.moments(largest_contour)
        
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0
                
            return largest_contour, cx, cy
        else:
            return None, 0, 0
            
        
    def convert_Pixels_to_3D(self, px, py, depth_frame, depth_image, depth_scale):
        intrinsics = depth_frame.profile.as_video_stream_profile().get_intrinsics()
        x, y, z = rs.rs2_deproject_pixel_to_point(intrinsics, [px, py], depth_image[py][px] * depth_scale)
        return x, y, z
    
    #Use loop
    def stream(self, align, clipping_distance, ds):
        # Get frameset of color and depth
        frames = self.pipeline.wait_for_frames()
        
        # frames.get_depth_frame() is a 640x360 depth image
        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            pass
        
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        
        # Remove background - Set pixels further than clipping_distance to grey
        grey_color = 153
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)
        
        #HSV - Black and White mask
        mask = self.convert_to_HSV(color_image)
        contour, org_x, org_y = self.findContour(mask)
        
        x, y, z = self.convert_Pixels_to_3D(org_x, org_y, aligned_depth_frame, depth_image, ds)

        
        cv2.drawContours(color_image, contour, -1, (0, 255, 0), 3)
        cv2.circle(color_image, (org_x, org_y), 5, (0, 0, 255), -1)
        text = f"x: {round(x*100, 2)}, y: {round(y*100, 2)}, z: {round(z*100, 2)}"
        cv2.putText(color_image, text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 0, 0), thickness=3)
        
  
        cv2.imshow(self.mask_image_name, color_image)
        
        #Get depth from pixels
 
                
        # #Thresholding
        # binary_threshold = self.binary_thresholding(color_image)
        # self.findContour(binary_threshold)
        # cv2.imshow("Thresholding", binary_threshold)
            
        
        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        # Render images:
        #   depth align to color on left
        #   depth on right
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        images = np.hstack((bg_removed, depth_colormap))
        

        # cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
        # cv2.imshow('Align Example', images)
            
        key = cv2.waitKey(1)
    
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            return False
        
        return x, y, z
    

    def cleanup(self):
        self.pipeline.stop()
